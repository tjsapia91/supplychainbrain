from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, Q
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import LandedCostDocument, LandedCostLine, LandedCostItemAllocation, CostComponent
from .forms import LandedCostDocumentForm


class LandedCostListView(LoginRequiredMixin, ListView):
    model = LandedCostDocument
    template_name = 'landedcosts/landedcost_list.html'
    context_object_name = 'documents'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related('ppo', 'vendor', 'branch', 'container', 'grpo', 'created_by')

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(lc_number__icontains=q) |
                Q(ppo__ppo_number__icontains=q) |
                Q(vendor__name__icontains=q)
            )

        status = self.request.GET.get('status', '').strip()
        if status:
            qs = qs.filter(status=status)

        return qs


class LandedCostDetailView(LoginRequiredMixin, DetailView):
    model = LandedCostDocument
    template_name = 'landedcosts/landedcost_detail.html'
    context_object_name = 'doc'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_lines'] = self.object.cost_lines.select_related('cost_component').all()
        context['item_lines'] = self.object.item_allocations.select_related('item', 'ppo_line', 'warehouse').all()
        return context


class LandedCostCreateView(LoginRequiredMixin, CreateView):
    model = LandedCostDocument
    form_class = LandedCostDocumentForm
    template_name = 'landedcosts/landedcost_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_components'] = CostComponent.objects.filter(is_active=True)
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.created_by = self.request.user
            form.instance.lc_number = LandedCostDocument.get_next_lc_number()
            self.object = form.save()

            # Save cost lines from POST
            self._save_cost_lines()

            # Auto-populate items from PO
            self.object.populate_items_from_ppo()

            messages.success(self.request, f'Landed Cost LC-{self.object.lc_number} created.')
        return redirect(reverse('landedcosts:lc_detail', kwargs={'pk': self.object.pk}))

    def _save_cost_lines(self):
        components = CostComponent.objects.filter(is_active=True)
        for comp in components:
            amount_key = f'cost_amount_{comp.pk}'
            alloc_key = f'cost_alloc_{comp.pk}'
            customs_key = f'cost_customs_{comp.pk}'
            amount = self.request.POST.get(amount_key, '0').replace(',', '')
            try:
                amount = Decimal(amount)
            except Exception:
                amount = Decimal('0')

            allocation = self.request.POST.get(alloc_key, comp.default_allocation)
            include_customs = customs_key in self.request.POST

            LandedCostLine.objects.create(
                document=self.object,
                cost_component=comp,
                allocation_by=allocation,
                amount=amount,
                include_for_customs=include_customs,
            )


class LandedCostUpdateView(LoginRequiredMixin, UpdateView):
    model = LandedCostDocument
    form_class = LandedCostDocumentForm
    template_name = 'landedcosts/landedcost_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cost_components'] = CostComponent.objects.filter(is_active=True)
        context['existing_cost_lines'] = {
            cl.cost_component_id: cl for cl in self.object.cost_lines.select_related('cost_component').all()
        }
        context['item_lines'] = self.object.item_allocations.select_related('item', 'ppo_line', 'warehouse').all()
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

            # Update cost lines
            self.object.cost_lines.all().delete()
            self._save_cost_lines()

            # Re-populate items if needed
            self.object.populate_items_from_ppo()

            messages.success(self.request, f'Landed Cost LC-{self.object.lc_number} updated.')
        return redirect(reverse('landedcosts:lc_detail', kwargs={'pk': self.object.pk}))

    def _save_cost_lines(self):
        components = CostComponent.objects.filter(is_active=True)
        for comp in components:
            amount_key = f'cost_amount_{comp.pk}'
            alloc_key = f'cost_alloc_{comp.pk}'
            customs_key = f'cost_customs_{comp.pk}'
            amount = self.request.POST.get(amount_key, '0').replace(',', '')
            try:
                amount = Decimal(amount)
            except Exception:
                amount = Decimal('0')

            allocation = self.request.POST.get(alloc_key, comp.default_allocation)
            include_customs = customs_key in self.request.POST

            LandedCostLine.objects.create(
                document=self.object,
                cost_component=comp,
                allocation_by=allocation,
                amount=amount,
                include_for_customs=include_customs,
            )


@login_required
def calculate_allocations(request, pk):
    """Run the allocation engine for a landed cost document."""
    doc = get_object_or_404(LandedCostDocument, pk=pk)
    if request.method == 'POST':
        doc.calculate_allocations()
        messages.success(request, f'Allocations calculated for LC-{doc.lc_number}.')
    return redirect(reverse('landedcosts:lc_detail', kwargs={'pk': pk}))


@login_required
def post_document(request, pk):
    """Post a landed cost document (finalize)."""
    doc = get_object_or_404(LandedCostDocument, pk=pk)
    if request.method == 'POST':
        if doc.status != 'calculated':
            messages.error(request, 'Document must be calculated before posting.')
        else:
            doc.status = 'posted'
            doc.posting_date = timezone.now().date()
            doc.posted_by = request.user
            doc.save()
            messages.success(request, f'LC-{doc.lc_number} posted successfully.')
    return redirect(reverse('landedcosts:lc_detail', kwargs={'pk': pk}))


@login_required
def ppo_lookup_for_lc(request):
    """API: look up a PPO by number for the landed cost form."""
    from procurement.models import PlannedPurchaseOrder
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'error': 'No query'}, status=400)

    try:
        ppo = PlannedPurchaseOrder.objects.select_related('vendor', 'branch', 'ship_to_3pl').get(ppo_number=q)
    except PlannedPurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'PO not found'}, status=404)

    lines = []
    for line in ppo.lines.select_related('item').all():
        lines.append({
            'ppo_line_id': line.pk,
            'item_no': line.item.item_no,
            'item_id': line.item_id,
            'description': line.description or line.item.description,
            'quantity': line.quantity or 0,
            'unit_price': str(line.unit_price or 0),
            'line_total': str(line.line_total or 0),
            'cbm': str(line.cbm or 0),
            'destination': line.destination or '',
        })

    # Get available containers for this PO
    from containers.models import ContainerPlan, ContainerItem
    container_ids = ContainerItem.objects.filter(
        ppo_line__ppo=ppo
    ).values_list('container_id', flat=True).distinct()
    containers = ContainerPlan.objects.filter(id__in=container_ids).values('id', 'plan_number', 'container_number')

    # Get GRPOs for this PO
    from receiving.models import GoodsReceiptPO
    grpos = GoodsReceiptPO.objects.filter(ppo=ppo).values('id', 'grpo_number', 'status')

    return JsonResponse({
        'ppo_id': ppo.pk,
        'ppo_number': ppo.ppo_number,
        'vendor_id': ppo.vendor_id,
        'vendor_name': ppo.vendor.name,
        'branch_id': ppo.branch_id if ppo.branch else None,
        'branch_name': ppo.branch.name if ppo.branch else '',
        'incoterms': ppo.incoterms,
        'total': str(ppo.total),
        'total_cbm': str(ppo.total_cbm),
        'lines': lines,
        'containers': list(containers),
        'grpos': list(grpos),
    })
