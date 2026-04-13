from django.contrib import admin
from .models import ContainerPlan, ContainerItem, DemandForecast, ContainerStatusLog


class ContainerItemInline(admin.TabularInline):
    model = ContainerItem
    extra = 0
    raw_id_fields = ['ppo_line', 'item']


@admin.register(ContainerPlan)
class ContainerPlanAdmin(admin.ModelAdmin):
    list_display = ['plan_number', 'container_number', 'status', 'container_type', 'total_cbm', 'total_units', 'target_load_date', 'date_sailed']
    list_filter = ['status', 'container_type', 'transport_mode']
    search_fields = ['plan_number', 'container_number', 'booking_reference']
    inlines = [ContainerItemInline]
    readonly_fields = ['total_cbm', 'total_weight', 'total_cartons', 'total_units', 'total_value']


@admin.register(ContainerItem)
class ContainerItemAdmin(admin.ModelAdmin):
    list_display = ['container', 'item', 'destination', 'quantity', 'cartons', 'cbm', 'qty_received', 'variance']
    list_filter = ['destination', 'container__status']
    raw_id_fields = ['container', 'ppo_line', 'item']


@admin.register(DemandForecast)
class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ['item', 'channel', 'month', 'forecast_qty', 'actual_qty', 'source']
    list_filter = ['channel', 'month', 'source']
    raw_id_fields = ['item']


@admin.register(ContainerStatusLog)
class ContainerStatusLogAdmin(admin.ModelAdmin):
    list_display = ['container', 'from_status', 'to_status', 'changed_by', 'timestamp']
    list_filter = ['to_status']
