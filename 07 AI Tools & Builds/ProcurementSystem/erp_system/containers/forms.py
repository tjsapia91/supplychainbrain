from django import forms
from .models import ContainerPlan, ContainerItem, DemandForecast
from procurement.models import PPOLineItem
from items.models import Item


class ContainerPlanForm(forms.ModelForm):
    class Meta:
        model = ContainerPlan
        fields = [
            'container_number', 'booking_reference', 'commercial_invoice',
            'container_type', 'max_cbm', 'max_weight_kg', 'transport_mode',
            'forwarder', 'hbl_number', 'incoterms', 'routing_notes',
            'port_of_loading', 'port_of_discharge', 'receiving_warehouse',
            'target_load_date', 'notes',
        ]
        widgets = {
            'target_load_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'routing_notes': forms.TextInput(attrs={'placeholder': 'e.g. DDP - Transload at LA'}),
        }


class ContainerStatusForm(forms.Form):
    """Form for updating container status with milestone dates"""
    STATUS_CHOICES = ContainerPlan.STATUS_CHOICES
    new_status = forms.ChoiceField(choices=STATUS_CHOICES)
    actual_load_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_sailed = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    eta_port = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    warehouse_delivery_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_entry_summary_received = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cross_dock_pickup_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cross_dock_delivery_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    cross_dock_bol = forms.CharField(required=False, max_length=100)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))


class ContainerItemForm(forms.ModelForm):
    class Meta:
        model = ContainerItem
        fields = [
            'ppo_line', 'item', 'description', 'destination', 'hts_code',
            'quantity', 'cartons', 'cbm', 'total_weight', 'line_value',
            'vendor_invoice_no', 'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class ContainerItemReceiveForm(forms.ModelForm):
    """Slim form for receiving items against a container"""
    class Meta:
        model = ContainerItem
        fields = ['qty_received', 'receive_date', 'transfer_qty', 'transfer_date', 'transfer_sap_doc', 'transfer_bol', 'notes']
        widgets = {
            'receive_date': forms.DateInput(attrs={'type': 'date'}),
            'transfer_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class AllocatePPOForm(forms.Form):
    """Form to allocate PPO line items to a container"""
    ppo_lines = forms.ModelMultipleChoiceField(
        queryset=PPOLineItem.objects.filter(
            ppo__status__in=['confirmed', 'ceo_approved', 'in_transit'],
            ppo__mode_of_transport='container',
        ),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class DemandForecastForm(forms.ModelForm):
    class Meta:
        model = DemandForecast
        fields = ['item', 'channel', 'month', 'forecast_qty', 'actual_qty', 'source', 'notes']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class BulkForecastForm(forms.Form):
    """Upload forecasts via CSV/Excel"""
    file = forms.FileField(help_text="CSV or Excel file with columns: item_no, channel, month (YYYY-MM-DD), forecast_qty, source")


class DocumentUploadForm(forms.Form):
    """Upload shipping documents (packing lists, commercial invoices, BOLs) in any format"""
    UPLOAD_TARGETS = [
        ('new', 'Create New Container Plan'),
        ('existing', 'Add to Existing Container'),
    ]
    file = forms.FileField(
        help_text="Upload Excel, PDF, CSV, or image files (JPG, PNG). Packing lists, commercial invoices, bills of lading."
    )
    target = forms.ChoiceField(choices=UPLOAD_TARGETS, initial='new')
    container = forms.ModelChoiceField(
        queryset=ContainerPlan.objects.filter(status__in=['planning', 'packing', 'booked', 'ready_to_load']),
        required=False,
        help_text="Select an existing container (only for 'Add to Existing')",
    )
