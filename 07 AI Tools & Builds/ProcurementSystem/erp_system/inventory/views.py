from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from accounts.mixins import InventoryRequiredMixin, ViewerOrAboveMixin, AdminRequiredMixin
from .models import Warehouse, StockLevel, StockMovement
from .forms import WarehouseForm, StockLevelForm, StockMovementForm


class WarehouseListView(ViewerOrAboveMixin, ListView):
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'
    context_object_name = 'warehouses'


class WarehouseDetailView(ViewerOrAboveMixin, DetailView):
    model = Warehouse
    template_name = 'inventory/warehouse_detail.html'
    context_object_name = 'warehouse'


class WarehouseCreateView(AdminRequiredMixin, CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('inventory:warehouse_list')


class WarehouseUpdateView(AdminRequiredMixin, UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'inventory/warehouse_form.html'
    success_url = reverse_lazy('inventory:warehouse_list')


class StockLevelListView(ViewerOrAboveMixin, ListView):
    model = StockLevel
    template_name = 'inventory/stocklevel_list.html'
    context_object_name = 'stock_levels'
    paginate_by = 50


class StockMovementListView(ViewerOrAboveMixin, ListView):
    model = StockMovement
    template_name = 'inventory/stockmovement_list.html'
    context_object_name = 'movements'
    paginate_by = 50


class StockMovementCreateView(InventoryRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stockmovement_form.html'
    success_url = reverse_lazy('inventory:movement_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
