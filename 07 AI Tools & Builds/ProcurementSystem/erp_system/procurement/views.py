from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils import timezone
from django_filters.views import FilterView
from django.db import models, transaction
from django.db.models import Q
import json

from accounts.mixins import (
    ProcurementRequiredMixin,
    ApprovalRequiredMixin,
    AdminRequiredMixin,
    ViewerOrAboveMixin,
    permission_check,
    role_required,
)

from .models import (
    PurchaseRequisition,
    PurchaseRequisitionLine,
    PlannedPurchaseOrder,
    PPOLineItem,
    ProformaInvoice,
    PPOAttachment,
    PPOStatusLog,
)
from items.models import Item
from vendors.models import Vendor
from .forms import (
    PurchaseRequisitionForm,
    PurchaseRequisitionLineFormSet,
    PlannedPurchaseOrderForm,
    PPOLineItemFormSet,
    ProformaInvoiceForm,
    PPOAttachmentForm,
    CEOApprovalForm,
)
import django_filters


# ============================================================================
# PURCHASE REQUISITION VIEWS
# ============================================================================

class PurchaseRequisitionFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseRequisition
        fields = {
            'status': ['exact'],
            'priority': ['exact'],
            'date': ['gte', 'lte'],
        }


class PurchaseRequisitionListView(LoginRequiredMixin, FilterView):
    model = PurchaseRequisition
    template_name = 'procurement/purchaserequisition_list.html'
    context_object_name = 'requisitions'
    paginate_by = 50
    filterset_class = PurchaseRequisitionFilter


class PurchaseRequisitionDetailView(LoginRequiredMixin, DetailView):
    model = PurchaseRequisition
    template_name = 'procurement/purchaserequisition_detail.html'
    context_object_name = 'requisition'


class PurchaseRequisitionCreateView(ProcurementRequiredMixin, CreateView):
    model = PurchaseRequisition
    form_class = PurchaseRequisitionForm
    template_name = 'procurement/purchaserequisition_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PurchaseRequisitionLineFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PurchaseRequisitionLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            form.instance.requested_by = self.request.user
            form.instance.pr_number = PurchaseRequisition.get_next_pr_number()
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)
        return redirect('procurement:pr_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('procurement:pr_detail', kwargs={'pk': self.object.pk})


@login_required
@permission_check('can_approve_pr')
def approve_requisition(request, pk):
    requisition = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        requisition.status = 'approved'
        requisition.approved_by = request.user
        requisition.approved_date = timezone.now()
        requisition.save()
        messages.success(request, f'Requisition PR-{requisition.pr_number} has been approved.')
        return redirect('procurement:pr_detail', pk=requisition.pk)
    return redirect('procurement:pr_detail', pk=requisition.pk)


# ============================================================================
# PLANNED PURCHASE ORDER VIEWS
# ============================================================================

class PlannedPurchaseOrderFilter(django_filters.FilterSet):
    ppo_number = django_filters.CharFilter(lookup_expr='icontains', label='PPO #')

    class Meta:
        model = PlannedPurchaseOrder
        fields = {
            'status': ['exact'],
            'vendor': ['exact'],
            'branch': ['exact'],
        }


class PlannedPurchaseOrderListView(LoginRequiredMixin, FilterView):
    model = PlannedPurchaseOrder
    template_name = 'procurement/plannedpurchaseorder_list.html'
    context_object_name = 'ppos'
    paginate_by = 50
    filterset_class = PlannedPurchaseOrderFilter

    # Allowed sort columns → model field mapping
    SORT_FIELDS = {
        'ppo_number': 'ppo_number',
        'date': 'date',
        'vendor': 'vendor__name',
        'branch': 'branch__name',
        'status': 'status',
        'ship_date': 'estimated_ship_date',
        'transport': 'mode_of_transport',
        'total': 'total',
    }

    def get_queryset(self):
        qs = PlannedPurchaseOrder.objects.select_related('vendor', 'branch', 'ship_to_3pl').all()

        # --- Free-text search (PPO #, vendor, AWB, etc.) ---
        search = self.request.GET.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(ppo_number__icontains=search) |
                Q(vendor__name__icontains=search) |
                Q(branch__name__icontains=search) |
                Q(awb_bl_number__icontains=search) |
                Q(vendor_pi_number__icontains=search)
            )

        # --- Destination filter (searches line-item destinations) ---
        destination = self.request.GET.get('destination', '').strip()
        if destination:
            qs = qs.filter(lines__destination__icontains=destination).distinct()

        # --- Date range filter (on PPO date) ---
        date_from = self.request.GET.get('date_from', '').strip()
        date_to = self.request.GET.get('date_to', '').strip()
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        # --- Ship date range filter ---
        ship_from = self.request.GET.get('ship_from', '').strip()
        ship_to = self.request.GET.get('ship_to', '').strip()
        if ship_from:
            qs = qs.filter(estimated_ship_date__gte=ship_from)
        if ship_to:
            qs = qs.filter(estimated_ship_date__lte=ship_to)

        # --- Sorting ---
        sort = self.request.GET.get('sort', '')
        direction = self.request.GET.get('dir', 'desc')
        if sort in self.SORT_FIELDS:
            order_field = self.SORT_FIELDS[sort]
            if direction == 'desc':
                order_field = '-' + order_field
            qs = qs.order_by(order_field)
        else:
            qs = qs.order_by('-date', '-ppo_number')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from vendors.models import Vendor, Branch
        context['all_vendors'] = Vendor.objects.filter(is_active=True).order_by('name')
        context['all_branches'] = Branch.objects.filter(is_active=True).order_by('name')
        # Gather distinct destinations from line items for the dropdown
        from procurement.models import PPOLineItem
        context['all_destinations'] = (
            PPOLineItem.objects.exclude(destination='')
            .values_list('destination', flat=True)
            .distinct()
            .order_by('destination')
        )
        # Pass current sort info to template
        context['current_sort'] = self.request.GET.get('sort', '')
        context['current_dir'] = self.request.GET.get('dir', 'desc')
        return context


class PlannedPurchaseOrderDetailView(LoginRequiredMixin, DetailView):
    model = PlannedPurchaseOrder
    template_name = 'procurement/plannedpurchaseorder_detail.html'
    context_object_name = 'ppo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lines'] = self.object.lines.all()
        context['proforma_invoices'] = self.object.proforma_invoices.all()
        context['status_logs'] = self.object.status_logs.all()
        context['attachments'] = self.object.attachments.all()
        return context


class PlannedPurchaseOrderCreateView(ProcurementRequiredMixin, CreateView):
    model = PlannedPurchaseOrder
    form_class = PlannedPurchaseOrderForm
    template_name = 'procurement/plannedpurchaseorder_form.html'

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill vendor from URL parameter (e.g., ?vendor=5)
        vendor_id = self.request.GET.get('vendor')
        if vendor_id:
            try:
                from vendors.models import Vendor
                vendor = Vendor.objects.get(pk=vendor_id)
                initial['vendor'] = vendor.pk
                # Also pre-fill defaults from vendor
                if vendor.payment_terms:
                    initial['payment_terms'] = vendor.payment_terms
                if vendor.lead_time_days:
                    initial['lead_time_days'] = vendor.lead_time_days
                if vendor.currency:
                    initial['currency'] = vendor.currency
            except Vendor.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PPOLineItemFormSet(self.request.POST)
        else:
            context['formset'] = PPOLineItemFormSet()
        # Pass vendor info for breadcrumb/back link
        vendor_id = self.request.GET.get('vendor')
        if vendor_id:
            try:
                from vendors.models import Vendor
                context['from_vendor'] = Vendor.objects.get(pk=vendor_id)
            except Vendor.DoesNotExist:
                pass
        # Port of discharge autocomplete options from existing PPOs
        context['ports_of_discharge'] = (
            PlannedPurchaseOrder.objects
            .exclude(port_of_discharge='')
            .values_list('port_of_discharge', flat=True)
            .distinct()
            .order_by('port_of_discharge')
        )
        return context

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.created_by = self.request.user
            # Only auto-assign PPO number if user didn't provide one
            if not form.instance.ppo_number:
                form.instance.ppo_number = PlannedPurchaseOrder.get_next_ppo_number()
            form.instance.date = timezone.now().date()
            self.object = form.save()

            formset = PPOLineItemFormSet(self.request.POST, instance=self.object)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                line_num = 1
                for instance in instances:
                    if not instance.item_id:
                        continue  # Skip empty rows with no item
                    instance.ppo = self.object
                    instance.line_number = line_num
                    instance.save()
                    line_num += 1
                formset.save_m2m()
                self.object.recalculate_totals()
            else:
                # If formset invalid, delete the PPO we just created and show errors
                self.object.delete()
                return self.render_to_response(self.get_context_data(form=form))
        messages.success(self.request, f'Purchase Order {self.object.ppo_number} saved successfully.')
        # Redirect back to create a new PO, preserving vendor context if present
        vendor_id = self.request.POST.get('vendor') or self.request.GET.get('vendor')
        if vendor_id:
            return redirect(f"{reverse('procurement:ppo_create')}?vendor={vendor_id}")
        return redirect('procurement:ppo_create')

    def get_success_url(self):
        return reverse('procurement:ppo_create')


class PlannedPurchaseOrderUpdateView(ProcurementRequiredMixin, UpdateView):
    model = PlannedPurchaseOrder
    form_class = PlannedPurchaseOrderForm
    template_name = 'procurement/plannedpurchaseorder_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PPOLineItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PPOLineItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()

            formset = PPOLineItemFormSet(self.request.POST, instance=self.object)
            if formset.is_valid():
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                line_num = 1
                for instance in instances:
                    if not instance.item_id:
                        continue  # Skip empty rows with no item
                    instance.ppo = self.object
                    instance.line_number = line_num
                    instance.save()
                    line_num += 1
                formset.save_m2m()
                self.object.recalculate_totals()
            else:
                return self.render_to_response(self.get_context_data(form=form))
        return redirect('procurement:ppo_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('procurement:ppo_detail', kwargs={'pk': self.object.pk})


# ============================================================================
# PPO BATCH SEND VIEWS
# ============================================================================

@login_required
@permission_check('can_create_ppo')
def ppo_batch_send(request):
    """Step 1: Show batch send confirmation page with email preview."""
    if request.method != 'POST':
        return redirect('procurement:ppo_list')

    raw_ids = request.POST.get('ppo_ids', '')
    ppo_ids = [int(x) for x in raw_ids.split(',') if x.strip().isdigit()]

    if not ppo_ids:
        messages.error(request, 'No PPOs selected for batch send.')
        return redirect('procurement:ppo_list')

    ppos = PlannedPurchaseOrder.objects.filter(pk__in=ppo_ids).select_related('vendor').order_by('vendor__name', 'ppo_number')

    warnings = []
    eligible = []
    for ppo in ppos:
        if ppo.status != 'draft':
            warnings.append(f'PPO-{ppo.ppo_number} is "{ppo.get_status_display()}" — only Draft PPOs can be sent. It will be skipped.')
        else:
            eligible.append(ppo)

    if not eligible:
        messages.error(request, 'None of the selected PPOs are in Draft status.')
        return redirect('procurement:ppo_list')

    from .email_service import get_sender_choices
    return render(request, 'procurement/ppo_batch_send.html', {
        'ppos': eligible,
        'ppo_pks': [p.pk for p in eligible],
        'warnings': warnings,
        'sender_choices': get_sender_choices(),
    })


@login_required
@permission_check('can_create_ppo')
def ppo_batch_send_confirm(request):
    """Step 2: Actually transition the PPOs and send emails via Microsoft 365."""
    if request.method != 'POST':
        return redirect('procurement:ppo_list')

    ppo_ids = request.POST.getlist('ppo_ids')
    ppo_ids = [int(x) for x in ppo_ids if x.strip().isdigit()]
    message_body = request.POST.get('message', '').strip()
    sender_key = request.POST.get('sender', 'tom')

    if not ppo_ids:
        messages.error(request, 'No PPOs selected.')
        return redirect('procurement:ppo_list')

    ppos = list(PlannedPurchaseOrder.objects.filter(pk__in=ppo_ids, status='draft').select_related('vendor'))
    sent_count = 0
    errors = []

    # Transition all PPOs to sent_to_vendor
    for ppo in ppos:
        try:
            from .email_service import AUTHORIZED_SENDERS
            sender = AUTHORIZED_SENDERS.get(sender_key, {})
            sender_name = sender.get('name', 'Unknown')
            notes = f'Batch sent to vendor by {sender_name}'
            if message_body:
                notes += f' | Message: {message_body[:200]}'
            ppo.change_status('sent_to_vendor', request.user, notes)
            ppo.vendor_email_sent_date = timezone.now()
            ppo.save()
            sent_count += 1
        except ValueError as e:
            errors.append(f'PPO-{ppo.ppo_number}: {e}')

    # Send actual email via Microsoft 365 (if configured)
    from .email_service import batch_send_ppos, is_email_configured
    if is_email_configured():
        email_result = batch_send_ppos(ppos, sender_key, message_body)
        if email_result['sent'] > 0:
            messages.success(request, f'{sent_count} PPO{"s" if sent_count != 1 else ""} sent to vendor and emailed successfully.')
        if email_result['errors']:
            for err in email_result['errors']:
                messages.warning(request, f'Email issue: {err}')
    else:
        if sent_count:
            messages.success(request, f'{sent_count} PPO{"s" if sent_count != 1 else ""} marked as sent to vendor. (Email not configured yet — set up Azure AD to enable automatic emails.)')

    for err in errors:
        messages.error(request, err)

    return redirect('procurement:ppo_list')


# ============================================================================
# PPO WORKFLOW ACTION VIEWS
# ============================================================================

@login_required
@permission_check('can_create_ppo')
def ppo_send_to_vendor(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        sender_key = request.POST.get('sender', 'tom')
        try:
            from .email_service import AUTHORIZED_SENDERS
            sender = AUTHORIZED_SENDERS.get(sender_key, {})
            sender_name = sender.get('name', 'Unknown')
            ppo.change_status('sent_to_vendor', request.user, f'PPO sent to vendor by {sender_name}')
            ppo.vendor_email_sent_date = timezone.now()
            ppo.save()

            # Send actual email (if configured)
            from .email_service import send_ppo_to_vendor, is_email_configured
            if is_email_configured():
                result = send_ppo_to_vendor(ppo, sender_key)
                if result:
                    messages.success(request, f'PPO-{ppo.ppo_number} emailed to {ppo.vendor.name} successfully.')
                else:
                    messages.warning(request, f'PPO-{ppo.ppo_number} marked as sent, but email delivery failed.')
            else:
                messages.success(request, f'PPO-{ppo.ppo_number} marked as sent to vendor.')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
@permission_check('can_create_ppo')
def ppo_mark_pi_received(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)

    if request.method == 'POST':
        pi_number = request.POST.get('pi_number', '').strip()
        pi_file = request.FILES.get('pi_file')
        notes = request.POST.get('notes', '').strip()
        pi_amount = request.POST.get('pi_amount', '').strip()

        if not pi_number:
            messages.error(request, 'Please enter the vendor PI number.')
            return render(request, 'procurement/ppo_record_pi.html', {'ppo': ppo})

        # Save PI number on the PPO
        ppo.vendor_pi_number = pi_number
        ppo.save()

        # Save the uploaded file as a PPO attachment
        if pi_file:
            desc = f"Proforma Invoice {pi_number}"
            if pi_amount:
                desc += f" — ${pi_amount}"
            PPOAttachment.objects.create(
                ppo=ppo,
                file=pi_file,
                file_type='pi_document',
                description=desc,
                uploaded_by=request.user,
            )

        # Transition status
        try:
            status_notes = f'Proforma Invoice received: {pi_number}'
            if notes:
                status_notes += f' | {notes}'
            ppo.change_status('pi_received', request.user, status_notes)
            messages.success(request, f'PPO-{ppo.ppo_number} — Proforma Invoice recorded successfully.')
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('procurement:ppo_detail', pk=ppo.pk)

    # GET — show the PI entry form
    return render(request, 'procurement/ppo_record_pi.html', {'ppo': ppo})


@login_required
@permission_check('can_create_ppo')
def ppo_request_ceo_approval(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        try:
            ppo.change_status('pending_ceo_approval', request.user, 'CEO approval requested')
            ppo.ceo_approval_requested_date = timezone.now()
            ppo.save()
            messages.success(request, f'PPO-{ppo.ppo_number} sent for CEO approval.')

            # Send CEO notification email (if configured)
            from .email_service import send_ceo_approval_request, is_email_configured
            if is_email_configured():
                requester_name = request.user.get_full_name() or request.user.username
                send_ceo_approval_request(ppo, requester_name)
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
@role_required('admin')
def ppo_ceo_approve(request, pk):
    """CEO approval — restricted to admin role only."""
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = CEOApprovalForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['action'] == 'approve':
                with transaction.atomic():
                    # Save signature
                    sig_type = form.cleaned_data.get('signature_type', '')
                    ppo.ceo_signature_type = sig_type
                    if sig_type == 'typed':
                        ppo.ceo_signature_text = form.cleaned_data.get('signature_text', '')
                    elif sig_type == 'image':
                        ppo.ceo_signature_image = form.cleaned_data.get('signature_image')

                    ppo.ceo_approved_by = request.user
                    ppo.ceo_approval_date = timezone.now()
                    ppo.save()
                    ppo.change_status('ceo_approved', request.user, form.cleaned_data.get('notes', ''))
                    ppo.change_status('confirmed', request.user, 'Auto-confirmed after CEO approval')
                messages.success(request, f'PPO-{ppo.ppo_number} approved and confirmed.')
                return redirect('procurement:ppo_detail', pk=ppo.pk)
            else:
                with transaction.atomic():
                    ppo.change_status('ceo_rejected', request.user, form.cleaned_data.get('notes', ''))
                    ppo.ceo_rejection_reason = form.cleaned_data.get('notes', '')
                    ppo.save()
                messages.error(request, f'PPO-{ppo.ppo_number} has been rejected.')
                return redirect('procurement:ppo_detail', pk=ppo.pk)
    else:
        form = CEOApprovalForm()
    return render(request, 'procurement/ppo_ceo_approval.html', {'ppo': ppo, 'form': form})


@login_required
@role_required('admin')
def ppo_ceo_reject(request, pk):
    """CEO rejection — restricted to admin role only."""
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        ppo.change_status('ceo_rejected', request.user, rejection_reason)
        ppo.ceo_rejection_reason = rejection_reason
        ppo.save()
        messages.error(request, f'PPO-{ppo.ppo_number} has been rejected.')
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
@permission_check('can_create_ppo')
def ppo_cancel(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        cancel_reason = request.POST.get('cancel_reason', '')
        try:
            ppo.change_status('cancelled', request.user, cancel_reason)
            ppo.save()
            messages.info(request, f'PPO-{ppo.ppo_number} has been cancelled.')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
def ppo_mark_in_transit(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        try:
            ppo.change_status('in_transit', request.user, 'Shipment in transit')
            ppo.save()
            messages.success(request, f'PPO-{ppo.ppo_number} marked as In Transit.')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
def ppo_close(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        try:
            ppo.change_status('closed', request.user, 'PPO closed')
            ppo.save()
            messages.success(request, f'PPO-{ppo.ppo_number} has been closed.')
        except ValueError as e:
            messages.error(request, str(e))
        return redirect('procurement:ppo_detail', pk=ppo.pk)
    return redirect('procurement:ppo_detail', pk=ppo.pk)


@login_required
def ppo_generate_pdf(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    from django.http import HttpResponse
    from .pdf_generator import generate_ppo_pdf

    # Always generate fresh PDF
    pdf_buffer = generate_ppo_pdf(ppo)
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="PPO-{ppo.ppo_number}.pdf"'
    return response


@login_required
@permission_check('can_create_ppo')
def ppo_duplicate(request, pk):
    """Create a new draft PPO pre-filled with all data from an existing PPO."""
    source = get_object_or_404(PlannedPurchaseOrder, pk=pk)

    with transaction.atomic():
        new_ppo_number = PlannedPurchaseOrder.get_next_ppo_number()

        # Copy all relevant fields (skip pk, auto-dates, approval fields, signatures)
        new_ppo = PlannedPurchaseOrder(
            ppo_number=new_ppo_number,
            date=timezone.now().date(),
            branch=source.branch,
            bill_to=source.bill_to,
            vendor=source.vendor,
            ship_to_3pl=source.ship_to_3pl,
            ship_to=source.ship_to,
            status='draft',
            requested_ship_date=source.requested_ship_date,
            payment_terms=source.payment_terms,
            mode_of_transport=source.mode_of_transport,
            port_of_loading=source.port_of_loading,
            port_of_discharge=source.port_of_discharge,
            country_of_origin=source.country_of_origin,
            incoterms=source.incoterms,
            lead_time_days=source.lead_time_days,
            currency=source.currency,
            special_notes=source.special_notes,
            wire_info=source.wire_info,
            deposit=source.deposit,
            created_by=request.user,
        )
        new_ppo.save()

        # Copy all line items
        source_lines = source.lines.all().order_by('line_number')
        for line in source_lines:
            PPOLineItem.objects.create(
                ppo=new_ppo,
                line_number=line.line_number,
                item=line.item,
                description=line.description,
                quantity=line.quantity,
                unit_price=line.unit_price,
                cartons=line.cartons,
                cbm=line.cbm,
                total_weight=line.total_weight,
                line_total=line.line_total,
                notes=line.notes,
                destination=line.destination,
            )

        new_ppo.recalculate_totals()

    messages.success(
        request,
        f'PPO-{new_ppo.ppo_number} created as a copy of PPO-{source.ppo_number}. '
        f'You can now edit it.'
    )
    return redirect('procurement:ppo_edit', pk=new_ppo.pk)


# ============================================================================
# PROFORMA INVOICE VIEWS
# ============================================================================

class ProformaInvoiceListView(LoginRequiredMixin, ListView):
    model = ProformaInvoice
    template_name = 'procurement/proformainvoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 50


class ProformaInvoiceDetailView(LoginRequiredMixin, DetailView):
    model = ProformaInvoice
    template_name = 'procurement/proformainvoice_detail.html'
    context_object_name = 'invoice'


class ProformaInvoiceCreateView(LoginRequiredMixin, CreateView):
    model = ProformaInvoice
    form_class = ProformaInvoiceForm
    template_name = 'procurement/proformainvoice_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ppo_id = self.request.GET.get('ppo_id')
        if ppo_id:
            context['ppo'] = get_object_or_404(PlannedPurchaseOrder, pk=ppo_id)
        return context

    def form_valid(self, form):
        ppo_id = self.request.POST.get('ppo_id') or self.request.GET.get('ppo_id')
        if not ppo_id:
            messages.error(self.request, 'PPO must be specified.')
            return self.form_invalid(form)
        ppo = get_object_or_404(PlannedPurchaseOrder, pk=ppo_id)
        form.instance.ppo = ppo
        form.instance.vendor = ppo.vendor
        form.instance.reviewed_by = self.request.user
        self.object = form.save()
        return redirect('procurement:pi_detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse('procurement:pi_detail', kwargs={'pk': self.object.pk})


# ============================================================================
# PPO ATTACHMENT VIEWS
# ============================================================================

@login_required
def ppo_upload_attachment(request, pk):
    ppo = get_object_or_404(PlannedPurchaseOrder, pk=pk)
    if request.method == 'POST':
        form = PPOAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.ppo = ppo
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, 'Attachment uploaded successfully.')
            return redirect('procurement:ppo_detail', pk=ppo.pk)
    else:
        form = PPOAttachmentForm()
    return render(request, 'procurement/ppo_upload_attachment.html', {'ppo': ppo, 'form': form})


# ============================================================================
# API/AJAX VIEWS
# ============================================================================

@login_required
def item_search_api(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    items = Item.objects.filter(
        item_no__icontains=query
    ) | Item.objects.filter(
        description__icontains=query
    )
    results = [
        {
            'id': item.id,
            'text': f"{item.item_no} - {item.description}"
        }
        for item in items[:30]
    ]
    return JsonResponse({'results': results})


@login_required
def item_detail_api(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        return JsonResponse({
            'id': item.id,
            'item_no': item.item_no,
            'description': item.description,
            'upc_master_carton_qty': item.upc_master_carton_qty or 0,
            'master_carton_volume': float(item.master_carton_volume or 0),
        })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)


@login_required
def vendor_defaults_api(request, vendor_id):
    """Return default port_of_loading and country_of_origin for a vendor."""
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        return JsonResponse({
            'default_port_of_loading': vendor.default_port_of_loading or '',
            'default_country_of_origin': vendor.default_country_of_origin or '',
            'payment_terms': vendor.payment_terms or '',
            'lead_time_days': vendor.lead_time_days or '',
            'currency': vendor.currency or 'USD',
        })
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)
