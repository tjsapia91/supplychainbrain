from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from accounts.mixins import FinanceRequiredMixin, ViewerOrAboveMixin
from .models import APInvoice
from .forms import APInvoiceForm
import django_filters


class APInvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = APInvoice
        fields = ['invoice_number', 'vendor', 'status']


class APInvoiceListView(ViewerOrAboveMixin, FilterView):
    model = APInvoice
    template_name = 'invoicing/apinvoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 50
    filterset_class = APInvoiceFilter


class APInvoiceDetailView(ViewerOrAboveMixin, DetailView):
    model = APInvoice
    template_name = 'invoicing/apinvoice_detail.html'
    context_object_name = 'invoice'


class APInvoiceCreateView(FinanceRequiredMixin, CreateView):
    model = APInvoice
    form_class = APInvoiceForm
    template_name = 'invoicing/apinvoice_form.html'
    success_url = reverse_lazy('invoicing:invoice_list')


class APInvoiceUpdateView(FinanceRequiredMixin, UpdateView):
    model = APInvoice
    form_class = APInvoiceForm
    template_name = 'invoicing/apinvoice_form.html'
    success_url = reverse_lazy('invoicing:invoice_list')
