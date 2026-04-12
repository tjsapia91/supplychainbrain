from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils import timezone
from accounts.mixins import ReceivingRequiredMixin, ViewerOrAboveMixin
from .models import GoodsReceiptPO, GRPOLineItem
from .forms import GoodsReceiptPOForm


class GoodsReceiptPOListView(ViewerOrAboveMixin, ListView):
    model = GoodsReceiptPO
    template_name = 'receiving/goodsreceiptpo_list.html'
    context_object_name = 'grpos'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related('ppo', 'vendor', 'warehouse', 'received_by')

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(grpo_number__icontains=q) |
                Q(ppo__ppo_number__icontains=q) |
                Q(vendor__name__icontains=q) |
                Q(reference__icontains=q)
            )

        status = self.request.GET.get('status', '').strip()
        if status:
            qs = qs.filter(status=status)

        date_from = self.request.GET.get('date_from', '').strip()
        if date_from:
            qs = qs.filter(receipt_date__gte=date_from)

        date_to = self.request.GET.get('date_to', '').strip()
        if date_to:
            qs = qs.filter(receipt_date__lte=date_to)

        return qs


class GoodsReceiptPODetailView(ViewerOrAboveMixin, DetailView):
    model = GoodsReceiptPO
    template_name = 'receiving/goodsreceiptpo_detail.html'
    context_object_name = 'grpo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = self.object.lines.select_related('item', 'ppo_line').all()
        return context


class GoodsReceiptPOCreateView(ReceivingRequiredMixin, CreateView):
    model = GoodsReceiptPO
    form_class = GoodsReceiptPOForm
    template_name = 'receiving/goodsreceiptpo_form.html'

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.received_by = self.request.user
            form.instance.grpo_number = GoodsReceiptPO.get_next_grpo_number()
            self.object = form.save()

            # Save line items from POST data
            ppo = self.object.ppo
            if ppo:
                for line in ppo.lines.select_related('item').all():
                    qty_key = f'qty_received_{line.pk}'
                    dmg_key = f'qty_damaged_{line.pk}'
                    qty_received = _parse_int(self.request.POST.get(qty_key, '0'))
                    qty_damaged = _parse_int(self.request.POST.get(dmg_key, '0'))

                    GRPOLineItem.objects.create(
                        grpo=self.object,
                        ppo_line=line,
                        item=line.item,
                        description=line.description or (line.item.description if line.item else ''),
                        destination=line.destination or '',
                        quantity_expected=line.quantity or 0,
                        quantity_received=qty_received,
                        quantity_damaged=qty_damaged,
                    )

                # Update PPO line received totals and PPO status
                _update_ppo_receiving(ppo, self.request.user)

        messages.success(self.request, f'GRPO-{self.object.grpo_number} created successfully.')
        return redirect('receiving:grpo_detail', pk=self.object.pk)


class GoodsReceiptPOUpdateView(ReceivingRequiredMixin, UpdateView):
    model = GoodsReceiptPO
    form_class = GoodsReceiptPOForm
    template_name = 'receiving/goodsreceiptpo_form.html'

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

            # Update line item quantities from POST data
            for line in self.object.lines.all():
                qty_key = f'qty_received_{line.ppo_line_id}'
                dmg_key = f'qty_damaged_{line.ppo_line_id}'
                line.quantity_received = _parse_int(self.request.POST.get(qty_key, '0'))
                line.quantity_damaged = _parse_int(self.request.POST.get(dmg_key, '0'))
                line.save()

            # Re-sync PPO line received totals and PPO status
            if self.object.ppo:
                _update_ppo_receiving(self.object.ppo, self.request.user)

            # Auto-cascade: check if any containers linked to this PPO should be completed
            _check_related_containers(self.object.ppo, self.request.user)

        messages.success(self.request, f'GRPO-{self.object.grpo_number} updated.')
        return redirect('receiving:grpo_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grpo_lines'] = self.object.lines.select_related('item', 'ppo_line').all()
        return context


# =============================================================================
# Helper functions
# =============================================================================

def _parse_int(value):
    """Safely parse an integer from form input."""
    try:
        return int(value) if value else 0
    except (ValueError, TypeError):
        return 0


def _update_ppo_receiving(ppo, user):
    """
    After a GRPO is saved, recalculate cumulative qty_received on each PPO line
    from ALL GRPOs against this PPO, then update the PPO status accordingly.

    Flow:
        - Sum qty_received across all GRPO line items for each PPO line
        - Update PPOLineItem.qty_received
        - Determine if PPO is fully received, partially received, or unchanged
        - Auto-update PPO status with audit log
    """
    from procurement.models import PPOLineItem

    ppo_lines = ppo.lines.all()
    if not ppo_lines.exists():
        return

    all_fully_received = True
    any_received = False

    for ppo_line in ppo_lines:
        # Sum qty_received from all GRPO line items pointing to this PPO line
        total_received = GRPOLineItem.objects.filter(
            ppo_line=ppo_line,
            grpo__status__in=['draft', 'posted'],  # exclude cancelled GRPOs
        ).aggregate(total=Sum('quantity_received'))['total'] or 0

        # Update the PPO line's cumulative received qty
        ppo_line.qty_received = total_received
        ppo_line.save(update_fields=['qty_received'])

        ordered_qty = ppo_line.quantity or 0
        if total_received > 0:
            any_received = True
        if total_received < ordered_qty:
            all_fully_received = False

    # Determine new PPO status
    old_status = ppo.status

    # Only auto-update if PPO is in a receivable state
    receivable_statuses = [
        'confirmed', 'in_transit', 'partially_received', 'fully_received'
    ]
    if old_status not in receivable_statuses:
        return

    if all_fully_received and any_received:
        new_status = 'fully_received'
    elif any_received:
        new_status = 'partially_received'
    else:
        return  # No change needed

    if new_status != old_status:
        try:
            ppo.change_status(
                new_status,
                user,
                notes=f'Auto-updated: goods receipt recorded'
            )
        except ValueError:
            pass  # Transition not allowed from current state; skip auto-update


def _check_related_containers(ppo, user):
    """
    After a PPO's receiving status is updated, check if any containers
    that contain items from this PPO should be auto-completed.
    """
    if not ppo:
        return
    try:
        from containers.models import ContainerPlan, ContainerItem, ContainerStatusLog
        # Find all containers that have items from this PPO's lines
        container_ids = ContainerItem.objects.filter(
            ppo_line__ppo=ppo
        ).values_list('container_id', flat=True).distinct()

        for container in ContainerPlan.objects.filter(pk__in=container_ids):
            if container.status in ('completed', 'cancelled'):
                continue
            # Check if ALL PPOs linked to this container are fully received
            items = container.items.select_related('ppo_line__ppo').all()
            linked_ppos = {}
            for ci in items:
                if ci.ppo_line and ci.ppo_line.ppo:
                    linked_ppos[ci.ppo_line.ppo.pk] = ci.ppo_line.ppo

            if linked_ppos and all(
                p.status in ('fully_received', 'closed')
                for p in linked_ppos.values()
            ):
                old_status = container.status
                container.status = 'completed'
                container.save()
                ContainerStatusLog.objects.create(
                    container=container,
                    from_status=old_status,
                    to_status='completed',
                    changed_by=user,
                    notes='Auto-completed: all linked PPOs fully received',
                )
    except Exception:
        pass  # Don't break GRPO save if cascade fails


# =============================================================================
# API Endpoints
# =============================================================================

@login_required
def ppo_lookup_api(request):
    """Return PPO details (vendor, line items with qty/destination) for GRPO auto-populate."""
    ppo_number = request.GET.get('ppo_number', '').strip()
    if not ppo_number:
        return JsonResponse({'error': 'No PPO number provided'}, status=400)

    from procurement.models import PlannedPurchaseOrder
    try:
        ppo = PlannedPurchaseOrder.objects.select_related('vendor').get(ppo_number=ppo_number)
    except PlannedPurchaseOrder.DoesNotExist:
        return JsonResponse({'error': f'PO #{ppo_number} not found'}, status=404)

    lines = []
    for line in ppo.lines.select_related('item').all():
        # Calculate how much has already been received across existing GRPOs
        already_received = GRPOLineItem.objects.filter(
            ppo_line=line,
            grpo__status__in=['draft', 'posted'],
        ).aggregate(total=Sum('quantity_received'))['total'] or 0

        lines.append({
            'ppo_line_id': line.pk,
            'item_no': line.item.item_no if line.item else '',
            'description': line.description or (line.item.description if line.item else ''),
            'quantity': line.quantity or 0,
            'qty_already_received': already_received,
            'destination': line.destination or '',
            'cartons': line.cartons or 0,
            'cbm': float(line.cbm or 0),
        })

    return JsonResponse({
        'ppo_id': ppo.pk,
        'ppo_number': ppo.ppo_number,
        'ppo_status': ppo.status,
        'vendor_id': ppo.vendor_id,
        'vendor_name': ppo.vendor.name if ppo.vendor else '',
        'awb_bl': ppo.awb_bl_number or '',
        'lines': lines,
    })
