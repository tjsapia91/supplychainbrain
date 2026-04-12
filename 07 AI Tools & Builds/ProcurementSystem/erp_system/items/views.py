from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from accounts.mixins import InventoryRequiredMixin, ViewerOrAboveMixin, AdminRequiredMixin
from .models import Item
from .forms import ItemForm
import django_filters


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['item_no', 'description', 'abc_classification', 'branch', 'inactive']


class ItemListView(ViewerOrAboveMixin, FilterView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 50
    filterset_class = ItemFilter


class ItemDetailView(ViewerOrAboveMixin, DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'


class ItemCreateView(InventoryRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('items:item_list')


class ItemUpdateView(InventoryRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('items:item_list')


class ItemDeleteView(AdminRequiredMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('items:item_list')
