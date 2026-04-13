from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F, Min, Max
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import csv
import json

from accounts.mixins import permission_check
from .models import ContainerPlan, ContainerItem, DemandForecast, ContainerStatusLog
from .forms import (
    ContainerPlanForm, ContainerStatusForm, ContainerItemForm,
    ContainerItemReceiveForm, DemandForecastForm, BulkForecastForm,
    DocumentUploadForm,
)
from .parsers import parse_document
from procurement.models import PlannedPurchaseOrder, PPOLineItem
from receiving.models import GoodsReceiptPO, GRPOLineItem
from items.models import Item
from vendors.models import ThreePLProvider


# ──────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────

@login_required
def container_dashboard(request):
    """Main container planning dashboard with summary stats"""
    containers = ContainerPlan.objects.all()

    # Status counts
    planning = containers.filter(status__in=['planning', 'packing']).count()
    booked = containers.filter(status__in=['booked', 'ready_to_load', 'loaded']).count()
    in_transit = containers.filter(status__in=['in_transit', 'at_port', 'customs']).count()
    delivered = containers.filter(status__in=['delivered', 'completed']).count()

    # In-transit containers with details
    transit_containers = containers.filter(status__in=['in_transit', 'at_port', 'customs']).order_by('eta_port')

    # Recent containers
    recent = containers[:10]

    # PPOs ready for container allocation (confirmed/approved, container transport)
    allocatable_ppos = PlannedPurchaseOrder.objects.filter(
        status__in=['confirmed', 'ceo_approved'],
        mode_of_transport='container',
    ).annotate(
        allocated_units=Sum('lines__container_allocations__quantity'),
    ).order_by('-date')[:10]

    context = {
        'planning_count': planning,
        'booked_count': booked,
        'in_transit_count': in_transit,
        'delivered_count': delivered,
        'total_count': containers.count(),
        'transit_containers': transit_containers,
        'recent_containers': recent,
        'allocatable_ppos': allocatable_ppos,
    }
    return render(request, 'containers/dashboard.html', context)


# ──────────────────────────────────────────────
# CONTAINER PLAN CRUD
# ──────────────────────────────────────────────

@login_required
def container_list(request):
    """List all container plans with filtering"""
    containers = ContainerPlan.objects.all()

    # Filters
    status = request.GET.get('status', '')
    transport = request.GET.get('transport', '')
    search = request.GET.get('q', '')

    if status:
        containers = containers.filter(status=status)
    if transport:
        containers = containers.filter(transport_mode=transport)
    if search:
        containers = containers.filter(
            Q(plan_number__icontains=search) |
            Q(container_number__icontains=search) |
            Q(booking_reference__icontains=search) |
            Q(forwarder__icontains=search)
        )

    context = {
        'containers': containers,
        'status_choices': ContainerPlan.STATUS_CHOICES,
        'transport_choices': ContainerPlan.TRANSPORT_MODE_CHOICES,
        'current_status': status,
        'current_transport': transport,
        'current_search': search,
    }
    return render(request, 'containers/container_list.html', context)


@login_required
@permission_check('can_manage_containers')
def container_create(request):
    """Create a new container plan"""
    if request.method == 'POST':
        form = ContainerPlanForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.plan_number = ContainerPlan.get_next_plan_number()
            container.created_by = request.user
            container.save()
            messages.success(request, f'Container plan {container.plan_number} created.')
            return redirect('container_detail', pk=container.pk)
    else:
        form = ContainerPlanForm()

    return render(request, 'containers/container_form.html', {'form': form, 'title': 'New Container Plan'})


@login_required
def container_detail(request, pk):
    """Container detail with items, utilization, and status timeline"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    items = container.items.select_related('item', 'ppo_line__ppo').all()
    status_logs = container.status_logs.all()[:20]

    # Capacity utilization
    cbm_pct = container.cbm_utilization
    weight_pct = container.weight_utilization

    # Status update form
    status_form = ContainerStatusForm(initial={
        'new_status': container.status,
        'actual_load_date': container.actual_load_date,
        'date_sailed': container.date_sailed,
        'eta_port': container.eta_port,
        'warehouse_delivery_date': container.warehouse_delivery_date,
        'date_entry_summary_received': container.date_entry_summary_received,
        'cross_dock_pickup_date': container.cross_dock_pickup_date,
        'cross_dock_delivery_date': container.cross_dock_delivery_date,
        'cross_dock_bol': container.cross_dock_bol,
    })

    context = {
        'container': container,
        'items': items,
        'status_logs': status_logs,
        'cbm_pct': cbm_pct,
        'weight_pct': weight_pct,
        'status_form': status_form,
    }
    return render(request, 'containers/container_detail.html', context)


@login_required
@permission_check('can_manage_containers')
def container_edit(request, pk):
    """Edit container plan details"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    if request.method == 'POST':
        form = ContainerPlanForm(request.POST, instance=container)
        if form.is_valid():
            form.save()
            messages.success(request, f'Container {container.plan_number} updated.')
            return redirect('container_detail', pk=container.pk)
    else:
        form = ContainerPlanForm(instance=container)

    return render(request, 'containers/container_form.html', {
        'form': form,
        'title': f'Edit {container.container_number or container.plan_number}',
        'container': container,
    })


@login_required
@permission_check('can_manage_containers')
def container_update_status(request, pk):
    """Update container status and milestone dates"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    if request.method == 'POST':
        form = ContainerStatusForm(request.POST)
        if form.is_valid():
            old_status = container.status
            new_status = form.cleaned_data['new_status']

            # Update dates
            for field in ['actual_load_date', 'date_sailed', 'eta_port',
                          'warehouse_delivery_date', 'date_entry_summary_received',
                          'cross_dock_pickup_date', 'cross_dock_delivery_date', 'cross_dock_bol']:
                val = form.cleaned_data.get(field)
                if val:
                    setattr(container, field, val)

            container.status = new_status
            container.save()

            # Create audit log
            if old_status != new_status:
                ContainerStatusLog.objects.create(
                    container=container,
                    from_status=old_status,
                    to_status=new_status,
                    changed_by=request.user,
                    notes=form.cleaned_data.get('notes', ''),
                )

            messages.success(request, f'Status updated to {container.get_status_display()}.')

    return redirect('container_detail', pk=container.pk)


# ──────────────────────────────────────────────
# CONTAINER ITEM MANAGEMENT
# ──────────────────────────────────────────────

@login_required
@permission_check('can_manage_containers')
def container_add_item(request, pk):
    """Add a line item to a container (manual entry)"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    if request.method == 'POST':
        form = ContainerItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.container = container
            item.save()
            container.recalculate_totals()
            messages.success(request, f'Item added to {container.plan_number}.')
            return redirect('container_detail', pk=container.pk)
    else:
        form = ContainerItemForm()

    return render(request, 'containers/container_add_item.html', {
        'form': form,
        'container': container,
    })


@login_required
@permission_check('can_manage_containers')
def container_allocate_ppo(request, pk):
    """Allocate PPO line items to a container"""
    container = get_object_or_404(ContainerPlan, pk=pk)

    # Get PPO lines available for allocation (container transport, confirmed/approved)
    available_lines = PPOLineItem.objects.filter(
        ppo__status__in=['confirmed', 'ceo_approved', 'in_transit'],
        ppo__mode_of_transport='container',
    ).select_related('ppo', 'item').order_by('ppo__ppo_number', 'line_number')

    if request.method == 'POST':
        selected_ids = request.POST.getlist('ppo_lines')
        count = 0
        for line_id in selected_ids:
            try:
                ppo_line = PPOLineItem.objects.get(pk=line_id)
                # Calculate remaining qty not yet allocated
                already_allocated = ppo_line.container_allocations.aggregate(
                    total=Sum('quantity')
                )['total'] or 0
                remaining = (ppo_line.quantity or 0) - already_allocated
                if remaining > 0:
                    # Check if custom qty was provided
                    custom_qty = request.POST.get(f'qty_{line_id}')
                    alloc_qty = int(custom_qty) if custom_qty else remaining
                    alloc_qty = min(alloc_qty, remaining)

                    ContainerItem.objects.create(
                        container=container,
                        ppo_line=ppo_line,
                        item=ppo_line.item,
                        description=ppo_line.description,
                        destination=ppo_line.destination,
                        quantity=alloc_qty,
                    )
                    count += 1
            except (PPOLineItem.DoesNotExist, ValueError):
                continue

        container.recalculate_totals()
        messages.success(request, f'{count} PPO line(s) allocated to container.')
        return redirect('container_detail', pk=container.pk)

    # Annotate available lines with already-allocated quantities and CBM-per-unit
    ppo_numbers_set = set()
    vendor_names_set = set()
    for line in available_lines:
        allocated = line.container_allocations.aggregate(total=Sum('quantity'))['total'] or 0
        line.already_allocated = allocated
        line.remaining = (line.quantity or 0) - allocated
        # CBM per unit estimate for live utilization
        if line.cbm and line.quantity and line.quantity > 0:
            line.cbm_per_unit = float(line.cbm) / float(line.quantity)
        else:
            line.cbm_per_unit = 0
        ppo_numbers_set.add(str(line.ppo.ppo_number))
        if line.ppo.vendor:
            vendor_names_set.add(line.ppo.vendor.name)

    context = {
        'container': container,
        'available_lines': available_lines,
        'ppo_numbers': sorted(ppo_numbers_set),
        'vendor_names': sorted(vendor_names_set),
        'cbm_pct': container.cbm_utilization,
    }
    return render(request, 'containers/container_allocate_ppo.html', context)


@login_required
@permission_check('can_manage_containers')
def container_remove_item(request, pk, item_pk):
    """Remove an item from a container"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    item = get_object_or_404(ContainerItem, pk=item_pk, container=container)
    if request.method == 'POST':
        item.delete()
        container.recalculate_totals()
        messages.success(request, 'Item removed from container.')
    return redirect('container_detail', pk=container.pk)


# ──────────────────────────────────────────────
# IN-TRANSIT TRACKING
# ──────────────────────────────────────────────

@login_required
def in_transit_list(request):
    """In-transit tracking dashboard - replaces the manual WATER/TRUCK/AIR Excel sheets"""
    mode = request.GET.get('mode', '')
    status = request.GET.get('status', '')

    containers = ContainerPlan.objects.exclude(
        status__in=['planning', 'packing', 'cancelled']
    ).prefetch_related(
        'items__ppo_line__ppo__goods_receipts',
        'items__ppo_line__ppo__vendor',
        'items__item',
    )

    if mode:
        containers = containers.filter(transport_mode=mode)
    if status:
        containers = containers.filter(status=status)

    # Group by status for summary
    status_summary = containers.values('status').annotate(count=Count('id')).order_by('status')

    # Build enriched container data with linked PPOs and GRPOs
    enriched = []
    for c in containers.order_by('eta_port'):
        # Collect unique PPOs linked through container items
        ppos = {}
        for ci in c.items.all():
            if ci.ppo_line and ci.ppo_line.ppo:
                ppo = ci.ppo_line.ppo
                ppos[ppo.pk] = ppo

        # Collect unique GRPOs linked through those PPOs
        grpos = {}
        vendors = {}
        for ppo in ppos.values():
            for grpo in ppo.goods_receipts.all():
                if grpo.status != 'cancelled':
                    grpos[grpo.pk] = grpo
            if ppo.vendor:
                vendors[ppo.vendor.pk] = ppo.vendor

        enriched.append({
            'container': c,
            'ppo_numbers': sorted(set(str(p.ppo_number) for p in ppos.values())),
            'ppo_statuses': sorted(set(p.get_status_display() for p in ppos.values())),
            'grpo_numbers': sorted(set(g.grpo_number for g in grpos.values())) if grpos else [],
            'grpo_statuses': sorted(set(g.get_status_display() for g in grpos.values())) if grpos else [],
            'vendor_names': sorted(set(v.name for v in vendors.values())) if vendors else [],
        })

    context = {
        'enriched_containers': enriched,
        'status_summary': status_summary,
        'current_mode': mode,
        'current_status': status,
        'transport_choices': ContainerPlan.TRANSPORT_MODE_CHOICES,
        'active_statuses': [
            ('booked', 'Booked'),
            ('ready_to_load', 'Ready to Load'),
            ('loaded', 'Loaded'),
            ('in_transit', 'In Transit'),
            ('at_port', 'At Port'),
            ('customs', 'In Customs'),
            ('delivered', 'Delivered'),
            ('completed', 'Completed'),
        ],
    }
    return render(request, 'containers/in_transit_list.html', context)


@login_required
@permission_check('can_manage_containers')
def container_receive(request, pk):
    """Record receiving quantities for a container"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    items = container.items.select_related('item').all()

    if request.method == 'POST':
        updated = 0
        for ci in items:
            qty_key = f'qty_received_{ci.pk}'
            date_key = f'receive_date_{ci.pk}'
            if qty_key in request.POST:
                try:
                    ci.qty_received = int(request.POST[qty_key])
                    if request.POST.get(date_key):
                        ci.receive_date = request.POST[date_key]
                    ci.save()
                    updated += 1
                except ValueError:
                    pass

        messages.success(request, f'{updated} item(s) updated with receiving data.')
        return redirect('container_detail', pk=container.pk)

    context = {
        'container': container,
        'items': items,
    }
    return render(request, 'containers/container_receive.html', context)


# ──────────────────────────────────────────────
# AUTO-CREATE GRPOs FROM CONTAINER DELIVERY
# ──────────────────────────────────────────────

@login_required
@permission_check('can_manage_containers')
def container_generate_grpos(request, pk):
    """
    Preview auto-generated GRPOs for a delivered container.
    Groups container items by PPO → one GRPO per PPO.
    """
    container = get_object_or_404(ContainerPlan, pk=pk)
    items = container.items.select_related('item', 'ppo_line__ppo__vendor').all()

    # Group container items by PPO
    ppo_groups = {}
    for ci in items:
        if ci.ppo_line and ci.ppo_line.ppo:
            ppo = ci.ppo_line.ppo
            if ppo.pk not in ppo_groups:
                ppo_groups[ppo.pk] = {
                    'ppo': ppo,
                    'vendor': ppo.vendor,
                    'items': [],
                    'total_units': 0,
                    'existing_grpos': list(
                        ppo.goods_receipts.exclude(status='cancelled')
                        .values_list('grpo_number', flat=True)
                    ),
                }
            ppo_groups[ppo.pk]['items'].append(ci)
            ppo_groups[ppo.pk]['total_units'] += ci.quantity or 0

    # Items without PPO link (manual entries)
    orphan_items = [ci for ci in items if not ci.ppo_line or not ci.ppo_line.ppo]

    warehouses = ThreePLProvider.objects.filter(is_active=True).order_by('name')

    context = {
        'container': container,
        'ppo_groups': ppo_groups,
        'orphan_items': orphan_items,
        'warehouses': warehouses,
        'today': date.today().isoformat(),
    }
    return render(request, 'containers/container_generate_grpos.html', context)


@login_required
@permission_check('can_manage_containers')
def container_confirm_grpos(request, pk):
    """
    Actually create one GRPO per PPO from the container's items.
    POST only — called from the confirmation page.
    """
    if request.method != 'POST':
        return redirect('container_generate_grpos', pk=pk)

    container = get_object_or_404(ContainerPlan, pk=pk)
    items = container.items.select_related('item', 'ppo_line__ppo__vendor').all()

    # Group container items by PPO
    ppo_groups = {}
    for ci in items:
        if ci.ppo_line and ci.ppo_line.ppo:
            ppo = ci.ppo_line.ppo
            if ppo.pk not in ppo_groups:
                ppo_groups[ppo.pk] = {'ppo': ppo, 'items': []}
            ppo_groups[ppo.pk]['items'].append(ci)

    warehouse_id = request.POST.get('warehouse', '')
    warehouse = None
    if warehouse_id:
        try:
            warehouse = ThreePLProvider.objects.get(pk=int(warehouse_id))
        except (ThreePLProvider.DoesNotExist, ValueError):
            pass

    receipt_date = request.POST.get('receipt_date', '') or date.today().isoformat()

    created_grpos = []
    from django.db import transaction
    with transaction.atomic():
        for ppo_pk, group in ppo_groups.items():
            ppo = group['ppo']

            # Check if user opted to skip this PPO
            if request.POST.get(f'skip_ppo_{ppo.pk}'):
                continue

            # Create the GRPO
            grpo = GoodsReceiptPO(
                grpo_number=GoodsReceiptPO.get_next_grpo_number(),
                ppo=ppo,
                vendor=ppo.vendor,
                receipt_date=receipt_date,
                posting_date=receipt_date,
                status='draft',
                warehouse=warehouse,
                reference=container.hbl_number or container.booking_reference or '',
                received_by=request.user,
                notes=f'Auto-generated from container {container.container_number or container.plan_number}',
            )
            grpo.save()

            # Create GRPO line items from the container items for this PPO
            for ci in group['items']:
                qty_received = request.POST.get(f'qty_{ci.pk}', '')
                try:
                    qty_received = int(qty_received) if qty_received else ci.quantity
                except ValueError:
                    qty_received = ci.quantity

                GRPOLineItem.objects.create(
                    grpo=grpo,
                    ppo_line=ci.ppo_line,
                    item=ci.item,
                    description=ci.description or (ci.item.description if ci.item else ''),
                    destination=ci.destination or '',
                    quantity_expected=ci.quantity or 0,
                    quantity_received=qty_received,
                    quantity_damaged=0,
                )

            created_grpos.append(grpo)

            # Update PPO receiving totals and status
            from receiving.views import _update_ppo_receiving
            _update_ppo_receiving(ppo, request.user)

    if created_grpos:
        grpo_nums = ', '.join(f'GRPO-{g.grpo_number}' for g in created_grpos)
        messages.success(request, f'{len(created_grpos)} GRPO(s) created: {grpo_nums}')

        # Auto-cascade: check if container should move to completed
        _check_container_completion(container, request.user)
    else:
        messages.warning(request, 'No GRPOs were created.')

    return redirect('container_detail', pk=container.pk)


# ──────────────────────────────────────────────
# AUTO-STATUS CASCADE
# ──────────────────────────────────────────────

def _check_container_completion(container, user):
    """
    If all PPOs linked to this container are fully_received or closed,
    auto-update the container status to 'completed'.
    """
    items = container.items.select_related('ppo_line__ppo').all()
    ppos = {}
    for ci in items:
        if ci.ppo_line and ci.ppo_line.ppo:
            ppos[ci.ppo_line.ppo.pk] = ci.ppo_line.ppo

    if not ppos:
        return

    all_done = all(
        p.status in ('fully_received', 'closed')
        for p in ppos.values()
    )

    if all_done and container.status not in ('completed', 'cancelled'):
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


# ──────────────────────────────────────────────
# DASHBOARD ALERTS
# ──────────────────────────────────────────────

@login_required
def dashboard_alerts_api(request):
    """
    JSON endpoint returning actionable alerts for the dashboard.
    Alert types:
      - overdue_eta: containers past ETA but not yet delivered
      - unallocated_ppo: confirmed PPOs with container transport but no container items
      - no_grpo: delivered containers with no GRPOs generated
      - overdue_delivery: containers past warehouse delivery date but not completed
    """
    today = date.today()
    alerts = []

    # 1. Overdue ETA — in transit past ETA port date
    overdue_eta = ContainerPlan.objects.filter(
        status__in=['in_transit', 'at_port', 'customs'],
        eta_port__lt=today,
    ).order_by('eta_port')
    for c in overdue_eta:
        days_late = (today - c.eta_port).days
        alerts.append({
            'type': 'overdue_eta',
            'severity': 'danger' if days_late > 7 else 'warning',
            'message': f'{c.container_number or c.plan_number} is {days_late} day(s) past ETA',
            'link': f'/containers/{c.pk}/',
            'container_id': c.pk,
        })

    # 2. Unallocated PPOs — confirmed/approved, container transport, no items allocated
    unallocated_ppos = PlannedPurchaseOrder.objects.filter(
        status__in=['confirmed', 'ceo_approved'],
        mode_of_transport='container',
    ).exclude(
        lines__container_allocations__isnull=False,
    ).distinct()
    for ppo in unallocated_ppos:
        alerts.append({
            'type': 'unallocated_ppo',
            'severity': 'info',
            'message': f'PPO #{ppo.ppo_number} ({ppo.vendor.name if ppo.vendor else "?"}) needs container allocation',
            'link': f'/procurement/ppos/{ppo.pk}/',
            'ppo_id': ppo.pk,
        })

    # 3. No GRPO — delivered containers with no GRPOs generated
    delivered_no_grpo = ContainerPlan.objects.filter(
        status='delivered',
    ).prefetch_related('items__ppo_line__ppo__goods_receipts')
    for c in delivered_no_grpo:
        ppos_in_container = set()
        has_grpo = False
        for ci in c.items.all():
            if ci.ppo_line and ci.ppo_line.ppo:
                ppos_in_container.add(ci.ppo_line.ppo.pk)
                if ci.ppo_line.ppo.goods_receipts.exclude(status='cancelled').exists():
                    has_grpo = True

        if ppos_in_container and not has_grpo:
            alerts.append({
                'type': 'no_grpo',
                'severity': 'warning',
                'message': f'{c.container_number or c.plan_number} delivered but no GRPO created',
                'link': f'/containers/{c.pk}/generate-grpos/',
                'container_id': c.pk,
            })

    # 4. Overdue warehouse delivery
    overdue_delivery = ContainerPlan.objects.filter(
        status__in=['delivered'],
        warehouse_delivery_date__lt=today - timedelta(days=3),
    ).exclude(status__in=['completed', 'cancelled'])
    for c in overdue_delivery:
        days = (today - c.warehouse_delivery_date).days
        alerts.append({
            'type': 'overdue_delivery',
            'severity': 'warning',
            'message': f'{c.container_number or c.plan_number} delivered {days}d ago, not yet completed',
            'link': f'/containers/{c.pk}/',
            'container_id': c.pk,
        })

    return JsonResponse({'alerts': alerts, 'count': len(alerts)})


# ──────────────────────────────────────────────
# DEMAND FORECASTING
# ──────────────────────────────────────────────

@login_required
def forecast_dashboard(request):
    """Demand forecast dashboard by SKU and channel"""
    item_no = request.GET.get('item', '')
    channel = request.GET.get('channel', '')

    forecasts = DemandForecast.objects.select_related('item').all()

    if item_no:
        forecasts = forecasts.filter(item__item_no=item_no)
    if channel:
        forecasts = forecasts.filter(channel=channel)

    # Get list of items with forecasts for the filter dropdown
    forecast_items = Item.objects.filter(
        demand_forecasts__isnull=False
    ).distinct().order_by('item_no')

    # Summary by item: total forecast for next 6 months
    today = date.today().replace(day=1)
    six_months = today + timedelta(days=180)
    upcoming = DemandForecast.objects.filter(
        month__gte=today, month__lte=six_months
    ).values('item__item_no', 'item__description').annotate(
        total_forecast=Sum('forecast_qty'),
        total_actual=Sum('actual_qty'),
    ).order_by('item__item_no')

    context = {
        'forecasts': forecasts[:200],
        'forecast_items': forecast_items,
        'channel_choices': DemandForecast.CHANNEL_CHOICES,
        'current_item': item_no,
        'current_channel': channel,
        'upcoming_summary': upcoming,
    }
    return render(request, 'containers/forecast_dashboard.html', context)


@login_required
@permission_check('can_manage_containers')
def forecast_create(request):
    """Create a single forecast entry"""
    if request.method == 'POST':
        form = DemandForecastForm(request.POST)
        if form.is_valid():
            forecast = form.save(commit=False)
            forecast.created_by = request.user
            forecast.save()
            messages.success(request, 'Forecast entry created.')
            return redirect('forecast_dashboard')
    else:
        form = DemandForecastForm()

    return render(request, 'containers/forecast_form.html', {'form': form, 'title': 'New Forecast Entry'})


@login_required
@permission_check('can_manage_containers')
def forecast_bulk_upload(request):
    """Bulk upload forecasts from CSV"""
    if request.method == 'POST':
        form = BulkForecastForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            try:
                decoded = f.read().decode('utf-8-sig').splitlines()
                reader = csv.DictReader(decoded)
                created = 0
                errors = []
                for i, row in enumerate(reader, start=2):
                    try:
                        item = Item.objects.get(item_no=row['item_no'].strip())
                        obj, was_created = DemandForecast.objects.update_or_create(
                            item=item,
                            channel=row['channel'].strip().lower(),
                            month=row['month'].strip(),
                            defaults={
                                'forecast_qty': int(row['forecast_qty']),
                                'source': row.get('source', 'CSV Upload').strip(),
                                'created_by': request.user,
                            }
                        )
                        created += 1
                    except Item.DoesNotExist:
                        errors.append(f"Row {i}: Item '{row.get('item_no', '')}' not found")
                    except Exception as e:
                        errors.append(f"Row {i}: {str(e)}")

                if created:
                    messages.success(request, f'{created} forecast(s) imported.')
                if errors:
                    messages.warning(request, f'{len(errors)} error(s): {"; ".join(errors[:5])}')

                return redirect('forecast_dashboard')
            except Exception as e:
                messages.error(request, f'Error reading file: {str(e)}')
    else:
        form = BulkForecastForm()

    return render(request, 'containers/forecast_bulk_upload.html', {'form': form})


@login_required
def forecast_item_detail(request, item_no):
    """Detailed forecast view for a single item across all channels"""
    item = get_object_or_404(Item, item_no=item_no)
    forecasts = DemandForecast.objects.filter(item=item).order_by('month', 'channel')

    # Build a month-by-channel matrix
    months = forecasts.values_list('month', flat=True).distinct().order_by('month')
    channels = forecasts.values_list('channel', flat=True).distinct().order_by('channel')

    matrix = {}
    for m in months:
        matrix[m] = {}
        for ch in channels:
            try:
                fc = forecasts.get(month=m, channel=ch)
                matrix[m][ch] = fc
            except DemandForecast.DoesNotExist:
                matrix[m][ch] = None

    # In-transit and on-order quantities
    in_transit_qty = ContainerItem.objects.filter(
        item=item,
        container__status__in=['in_transit', 'at_port', 'customs'],
    ).aggregate(total=Sum('quantity'))['total'] or 0

    on_order_qty = PPOLineItem.objects.filter(
        item=item,
        ppo__status__in=['confirmed', 'ceo_approved'],
    ).aggregate(total=Sum('quantity'))['total'] or 0

    context = {
        'item': item,
        'forecasts': forecasts,
        'months': months,
        'channels': channels,
        'matrix': matrix,
        'in_transit_qty': in_transit_qty,
        'on_order_qty': on_order_qty,
        'current_stock': item.in_stock,
    }
    return render(request, 'containers/forecast_item_detail.html', context)


# ──────────────────────────────────────────────
# EXPORTS
# ──────────────────────────────────────────────

@login_required
def export_container_csv(request, pk):
    """Export container items as CSV"""
    container = get_object_or_404(ContainerPlan, pk=pk)
    items = container.items.select_related('item', 'ppo_line__ppo').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="container_{container.container_number or container.plan_number}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'PPO#', 'UPC/Item#', 'Description', 'Destination', 'HTS Code',
        'Units', 'Cases', 'CBM', 'Weight', 'Value',
        'Qty Received', 'Variance', 'Notes'
    ])

    for ci in items:
        writer.writerow([
            ci.ppo_number or '',
            ci.item.item_no if ci.item else '',
            ci.description,
            ci.destination,
            ci.hts_code,
            ci.quantity,
            ci.cartons,
            ci.cbm,
            ci.total_weight,
            ci.line_value,
            ci.qty_received,
            ci.variance,
            ci.notes,
        ])

    return response


@login_required
def export_transit_csv(request):
    """Export in-transit data as CSV (replaces manual IN TRANSIT LOG)"""
    containers = ContainerPlan.objects.exclude(
        status__in=['planning', 'packing', 'cancelled']
    ).prefetch_related('items__item', 'items__ppo_line__ppo')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="in_transit_log_{date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Container#', 'Plan#', 'Status', 'Transport', 'PPO#', 'Item#',
        'Description', 'Destination', 'Qty Shipped', 'Cases', 'CBM',
        'Commercial Invoice', 'Forwarder', 'HTS Code', 'Vendor Invoice',
        'HBL', 'Date Sailed', 'ETA Port', 'Whse Delivery',
        'Receiving Warehouse', 'Qty Received', 'Variance',
        'Cross-dock Pickup', 'Cross-dock Delivery', 'BOL#',
        'Transfer Qty', 'Transfer Date', 'SAP Doc#', 'Notes'
    ])

    for c in containers:
        for ci in c.items.all():
            writer.writerow([
                c.container_number, c.plan_number, c.get_status_display(),
                c.get_transport_mode_display(),
                ci.ppo_number or '', ci.item.item_no if ci.item else '',
                ci.description, ci.destination, ci.quantity, ci.cartons, ci.cbm,
                c.commercial_invoice, c.forwarder, ci.hts_code, ci.vendor_invoice_no,
                c.hbl_number, c.date_sailed, c.eta_port, c.warehouse_delivery_date,
                c.receiving_warehouse, ci.qty_received, ci.variance,
                c.cross_dock_pickup_date, c.cross_dock_delivery_date, c.cross_dock_bol,
                ci.transfer_qty, ci.transfer_date, ci.transfer_sap_doc, ci.notes,
            ])

    return response


# ──────────────────────────────────────────────
# API ENDPOINTS (for AJAX)
# ──────────────────────────────────────────────

@login_required
def api_ppo_lines(request):
    """API: Get PPO line items for a given PPO number (for dynamic forms)"""
    ppo_number = request.GET.get('ppo')
    if not ppo_number:
        return JsonResponse({'lines': []})

    try:
        ppo = PlannedPurchaseOrder.objects.get(ppo_number=ppo_number)
        lines = []
        for line in ppo.lines.select_related('item').all():
            allocated = line.container_allocations.aggregate(total=Sum('quantity'))['total'] or 0
            lines.append({
                'id': line.pk,
                'item_no': line.item.item_no,
                'description': line.description,
                'quantity': line.quantity,
                'allocated': allocated,
                'remaining': (line.quantity or 0) - allocated,
                'destination': line.destination,
                'cartons': line.cartons,
                'cbm': str(line.cbm or 0),
            })
        return JsonResponse({'lines': lines, 'ppo': ppo_number})
    except PlannedPurchaseOrder.DoesNotExist:
        return JsonResponse({'lines': [], 'error': 'PPO not found'})


@login_required
def api_item_forecast(request, item_no):
    """API: Get forecast data for chart rendering"""
    try:
        item = Item.objects.get(item_no=item_no)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

    forecasts = DemandForecast.objects.filter(item=item).order_by('month')
    data = {}
    for fc in forecasts:
        month_key = fc.month.strftime('%Y-%m')
        if month_key not in data:
            data[month_key] = {'month': month_key, 'forecast': 0, 'actual': 0}
        data[month_key]['forecast'] += fc.forecast_qty
        data[month_key]['actual'] += fc.actual_qty

    return JsonResponse({'item': item_no, 'data': list(data.values())})


# ──────────────────────────────────────────────
# SMART DOCUMENT UPLOAD
# ──────────────────────────────────────────────

@login_required
@permission_check('can_manage_containers')
def document_upload(request):
    """Upload a shipping document (Excel, PDF, image) for automatic data extraction."""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            target = form.cleaned_data['target']
            container = form.cleaned_data.get('container')

            try:
                parsed = parse_document(uploaded_file, uploaded_file.name)
            except Exception as e:
                messages.error(request, f'Error parsing document: {str(e)}')
                return render(request, 'containers/document_upload.html', {'form': form})

            # Try to match item_no values to existing Items
            for item_data in parsed.get('items', []):
                item_no = item_data.get('item_no', '')
                if item_no:
                    try:
                        db_item = Item.objects.get(item_no=item_no)
                        item_data['item_id'] = db_item.pk
                        item_data['item_match'] = db_item.item_no
                    except Item.DoesNotExist:
                        # Try partial match
                        matches = Item.objects.filter(item_no__icontains=item_no)[:1]
                        if matches:
                            item_data['item_id'] = matches[0].pk
                            item_data['item_match'] = f'{matches[0].item_no} (fuzzy)'
                        else:
                            item_data['item_match'] = 'Not found'

            # Store parsed data in session for the review step
            request.session['parsed_doc'] = {
                'container': parsed.get('container', {}),
                'items': parsed.get('items', []),
                'doc_type': parsed.get('doc_type', ''),
                'filename': uploaded_file.name,
                'target': target,
                'container_pk': container.pk if container else None,
            }

            return redirect('document_review')
    else:
        form = DocumentUploadForm()

    # Get open containers for the dropdown
    open_containers = ContainerPlan.objects.filter(
        status__in=['planning', 'packing', 'booked', 'ready_to_load']
    )

    return render(request, 'containers/document_upload.html', {
        'form': form,
        'open_containers': open_containers,
    })


@login_required
@permission_check('can_manage_containers')
def document_review(request):
    """Review and edit extracted data before saving to a container."""
    parsed = request.session.get('parsed_doc')
    if not parsed:
        messages.warning(request, 'No document data to review. Please upload a document first.')
        return redirect('document_upload')

    container_fields = parsed.get('container', {})
    items = parsed.get('items', [])
    target = parsed.get('target', 'new')
    container_pk = parsed.get('container_pk')

    # Get existing container if targeting one
    existing_container = None
    if target == 'existing' and container_pk:
        try:
            existing_container = ContainerPlan.objects.get(pk=container_pk)
        except ContainerPlan.DoesNotExist:
            pass

    # Available items for dropdown matching
    all_items = Item.objects.all().order_by('item_no')
    # Destination choices
    destinations = ['AMZ', 'SB', 'AWD', '3PL', 'Floship', 'Walmart', 'AMZ Canada', 'Other']

    context = {
        'container_fields': container_fields,
        'items': items,
        'item_count': len(items),
        'target': target,
        'existing_container': existing_container,
        'filename': parsed.get('filename', ''),
        'doc_type': parsed.get('doc_type', ''),
        'all_items': all_items,
        'destinations': destinations,
        'container_type_choices': ContainerPlan.CONTAINER_TYPE_CHOICES,
        'status_choices': ContainerPlan.STATUS_CHOICES,
    }
    return render(request, 'containers/document_review.html', context)


@login_required
@permission_check('can_manage_containers')
def document_confirm(request):
    """Save the reviewed/edited data to create or update a container."""
    if request.method != 'POST':
        return redirect('document_upload')

    parsed = request.session.get('parsed_doc')
    if not parsed:
        messages.warning(request, 'Session expired. Please upload the document again.')
        return redirect('document_upload')

    target = parsed.get('target', 'new')
    container_pk = parsed.get('container_pk')

    # Build or get the container
    if target == 'existing' and container_pk:
        try:
            container = ContainerPlan.objects.get(pk=container_pk)
        except ContainerPlan.DoesNotExist:
            messages.error(request, 'Container not found.')
            return redirect('document_upload')
    else:
        container = ContainerPlan(
            plan_number=ContainerPlan.get_next_plan_number(),
            created_by=request.user,
        )

    # Apply container-level fields from the form
    for field in ['container_number', 'booking_reference', 'commercial_invoice',
                  'forwarder', 'hbl_number', 'incoterms', 'port_of_loading',
                  'port_of_discharge', 'receiving_warehouse', 'container_type',
                  'routing_notes']:
        val = request.POST.get(f'c_{field}', '').strip()
        if val:
            setattr(container, field, val)

    # Date fields
    for field in ['target_load_date', 'date_sailed', 'eta_port', 'warehouse_delivery_date']:
        val = request.POST.get(f'c_{field}', '').strip()
        if val:
            try:
                setattr(container, field, val)
            except Exception:
                pass

    # Status
    status_val = request.POST.get('c_status', '').strip()
    if status_val:
        container.status = status_val

    container.save()

    # Process line items
    item_count = int(request.POST.get('item_count', 0))
    created = 0
    for i in range(item_count):
        prefix = f'item_{i}_'
        item_no = request.POST.get(f'{prefix}item_no', '').strip()
        item_id = request.POST.get(f'{prefix}item_id', '').strip()
        description = request.POST.get(f'{prefix}description', '').strip()
        destination = request.POST.get(f'{prefix}destination', '').strip()
        hts_code = request.POST.get(f'{prefix}hts_code', '').strip()
        quantity = request.POST.get(f'{prefix}quantity', '0').strip()
        cartons = request.POST.get(f'{prefix}cartons', '0').strip()
        cbm = request.POST.get(f'{prefix}cbm', '0').strip()
        weight = request.POST.get(f'{prefix}total_weight', '0').strip()
        value = request.POST.get(f'{prefix}line_value', '0').strip()
        vendor_inv = request.POST.get(f'{prefix}vendor_invoice_no', '').strip()
        notes = request.POST.get(f'{prefix}notes', '').strip()

        # Skip if no meaningful data
        if not (item_no or description or item_id):
            continue

        # Resolve item
        db_item = None
        if item_id:
            try:
                db_item = Item.objects.get(pk=int(item_id))
            except (Item.DoesNotExist, ValueError):
                pass
        if not db_item and item_no:
            try:
                db_item = Item.objects.get(item_no=item_no)
            except Item.DoesNotExist:
                pass

        ci = ContainerItem(
            container=container,
            item=db_item,
            description=description or (db_item.description if db_item else item_no),
            destination=destination,
            hts_code=hts_code,
            quantity=int(float(quantity)) if quantity else 0,
            cartons=int(float(cartons)) if cartons else 0,
            cbm=Decimal(cbm) if cbm else Decimal('0'),
            total_weight=Decimal(weight) if weight else Decimal('0'),
            line_value=Decimal(value) if value else Decimal('0'),
            vendor_invoice_no=vendor_inv,
            notes=notes,
        )
        ci.save()
        created += 1

    container.recalculate_totals()

    # Clear session data
    if 'parsed_doc' in request.session:
        del request.session['parsed_doc']

    messages.success(request, f'Document imported! {created} item(s) added to container {container.container_number or container.plan_number}.')
    return redirect('container_detail', pk=container.pk)
