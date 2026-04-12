from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Avg, Q
from django_filters.views import FilterView
from accounts.mixins import VendorRequiredMixin, ViewerOrAboveMixin, AdminRequiredMixin
from .models import Vendor, BillToAddress, ShipToAddress, Branch, ThreePLProvider
from .forms import VendorForm, BillToAddressForm, ShipToAddressForm, BranchForm, ThreePLProviderForm
import django_filters


class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    code = django_filters.CharFilter(lookup_expr='icontains', label='Code')

    class Meta:
        model = Vendor
        fields = ['name', 'code', 'country', 'is_active']


class VendorListView(ViewerOrAboveMixin, FilterView):
    model = Vendor
    template_name = 'vendors/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 50
    filterset_class = VendorFilter

    def get_queryset(self):
        from django.db.models import Count
        return Vendor.objects.annotate(
            order_count=Count('purchase_orders'),
        ).order_by('name')


class VendorDetailView(ViewerOrAboveMixin, DetailView):
    model = Vendor
    template_name = 'vendors/vendor_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.object
        all_ppos = vendor.purchase_orders.select_related('branch', 'ship_to_3pl').all()

        active_statuses = ['draft', 'sent_to_vendor', 'pi_received', 'pending_ceo_approval',
                           'ceo_approved', 'confirmed', 'in_transit', 'partially_received']
        completed_statuses = ['fully_received', 'closed', 'cancelled', 'ceo_rejected']

        context['active_ppos'] = all_ppos.filter(status__in=active_statuses).order_by('-ppo_number')
        context['completed_ppos'] = all_ppos.filter(status__in=completed_statuses).order_by('-ppo_number')

        context['total_orders'] = all_ppos.count()
        context['active_orders'] = context['active_ppos'].count()
        context['total_spend'] = all_ppos.aggregate(s=Sum('total'))['s'] or 0
        context['avg_lead_time'] = vendor.lead_time_days or all_ppos.aggregate(a=Avg('lead_time_days'))['a']

        return context


class VendorCreateView(VendorRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'

    def get_success_url(self):
        return reverse_lazy('vendors:vendor_detail', kwargs={'pk': self.object.pk})


class VendorUpdateView(VendorRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendors/vendor_form.html'

    def get_success_url(self):
        return reverse_lazy('vendors:vendor_detail', kwargs={'pk': self.object.pk})


class VendorDeleteView(AdminRequiredMixin, DeleteView):
    model = Vendor
    template_name = 'vendors/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendors:vendor_list')


# --- Branches ---
class BranchListView(ViewerOrAboveMixin, ListView):
    model = Branch
    template_name = 'vendors/branch_list.html'
    context_object_name = 'branches'


class BranchCreateView(AdminRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'vendors/branch_form.html'
    success_url = reverse_lazy('vendors:branch_list')


class BranchUpdateView(AdminRequiredMixin, UpdateView):
    model = Branch
    form_class = BranchForm
    template_name = 'vendors/branch_form.html'
    success_url = reverse_lazy('vendors:branch_list')


# --- Bill-To Addresses ---
class BillToAddressListView(ViewerOrAboveMixin, ListView):
    model = BillToAddress
    template_name = 'vendors/billtoaddress_list.html'
    context_object_name = 'addresses'


class BillToAddressCreateView(VendorRequiredMixin, CreateView):
    model = BillToAddress
    form_class = BillToAddressForm
    template_name = 'vendors/billtoaddress_form.html'
    success_url = reverse_lazy('vendors:billto_list')


class BillToAddressUpdateView(VendorRequiredMixin, UpdateView):
    model = BillToAddress
    form_class = BillToAddressForm
    template_name = 'vendors/billtoaddress_form.html'
    success_url = reverse_lazy('vendors:billto_list')


# --- 3PL Providers ---
class ThreePLListView(ViewerOrAboveMixin, ListView):
    model = ThreePLProvider
    template_name = 'vendors/threepl_list.html'
    context_object_name = 'providers'


class ThreePLDetailView(ViewerOrAboveMixin, DetailView):
    model = ThreePLProvider
    template_name = 'vendors/threepl_detail.html'
    context_object_name = 'provider'


class ThreePLCreateView(VendorRequiredMixin, CreateView):
    model = ThreePLProvider
    form_class = ThreePLProviderForm
    template_name = 'vendors/threepl_form.html'
    success_url = reverse_lazy('vendors:threepl_list')


class ThreePLUpdateView(VendorRequiredMixin, UpdateView):
    model = ThreePLProvider
    form_class = ThreePLProviderForm
    template_name = 'vendors/threepl_form.html'
    success_url = reverse_lazy('vendors:threepl_list')


# --- Ship-To Addresses (legacy) ---
class ShipToAddressListView(ViewerOrAboveMixin, ListView):
    model = ShipToAddress
    template_name = 'vendors/shiptoaddress_list.html'
    context_object_name = 'addresses'


class ShipToAddressCreateView(VendorRequiredMixin, CreateView):
    model = ShipToAddress
    form_class = ShipToAddressForm
    template_name = 'vendors/shiptoaddress_form.html'
    success_url = reverse_lazy('vendors:shipto_list')


class ShipToAddressUpdateView(VendorRequiredMixin, UpdateView):
    model = ShipToAddress
    form_class = ShipToAddressForm
    template_name = 'vendors/shiptoaddress_form.html'
    success_url = reverse_lazy('vendors:shipto_list')
