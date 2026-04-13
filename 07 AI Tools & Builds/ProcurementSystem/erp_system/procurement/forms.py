from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.utils import timezone
from datetime import timedelta
from .models import (
    PurchaseRequisition,
    PurchaseRequisitionLine,
    PlannedPurchaseOrder,
    PPOLineItem,
    ProformaInvoice,
    PPOAttachment,
    PPOStatusLog,
)


class BootstrapMixin:
    """Mixin to add Bootstrap 5 classes to form fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({
                    'class': 'form-check-input'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'rows': 4
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control'
                })


class PurchaseRequisitionForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PurchaseRequisition
        fields = ['priority', 'notes']
        labels = {
            'priority': 'Priority Level',
            'notes': 'Additional Notes',
        }


class PurchaseRequisitionLineForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PurchaseRequisitionLine
        fields = ['item', 'quantity', 'suggested_vendor', 'notes']
        labels = {
            'item': 'Item',
            'quantity': 'Quantity',
            'suggested_vendor': 'Suggested Vendor',
            'notes': 'Notes',
        }


# Formset for PurchaseRequisitionLine
PurchaseRequisitionLineFormSet = inlineformset_factory(
    PurchaseRequisition,
    PurchaseRequisitionLine,
    form=PurchaseRequisitionLineForm,
    extra=3,
    can_delete=True
)


class PlannedPurchaseOrderForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PlannedPurchaseOrder
        fields = [
            'ppo_number',
            'branch',
            'vendor',
            'bill_to',
            'ship_to_3pl',
            'requested_ship_date',
            'estimated_ship_date',
            'payment_terms',
            'mode_of_transport',
            'port_of_loading',
            'port_of_discharge',
            'country_of_origin',
            'incoterms',
            'lead_time_days',
            'currency',
            'deposit',
            'awb_bl_number',
            'vendor_pi_number',
            'special_notes',
            'wire_info',
        ]
        labels = {
            'ppo_number': 'PO #',
            'branch': 'Branch',
            'vendor': 'Seller / Exporter',
            'bill_to': 'Bill To',
            'ship_to_3pl': 'Ship To (3PL)',
            'requested_ship_date': 'Requested Ship Date',
            'estimated_ship_date': 'Estimated Ship Date',
            'payment_terms': 'Payment Terms',
            'mode_of_transport': 'Mode of Transport',
            'port_of_loading': 'Port of Loading',
            'port_of_discharge': 'Port of Discharge',
            'country_of_origin': 'Country of Origin',
            'incoterms': 'Incoterms',
            'lead_time_days': 'Lead Time (Days)',
            'currency': 'Currency',
            'deposit': 'Deposit Amount',
            'awb_bl_number': 'AWB/BL #',
            'vendor_pi_number': 'Vendor PI #',
            'special_notes': 'Special Notes',
            'wire_info': 'Wire/Bank Information',
        }
        widgets = {
            'requested_ship_date': forms.DateInput(attrs={'type': 'date'}),
            'estimated_ship_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # PPO number: optional on create (auto-generated), editable on update
        self.fields['ppo_number'].required = False
        if not self.instance.pk:
            self.fields['ppo_number'].widget.attrs['placeholder'] = 'Auto-generated if blank'
        self.fields['ppo_number'].help_text = 'Leave blank to auto-generate next number'
        # Make optional fields explicitly not required
        self.fields['bill_to'].required = False
        self.fields['branch'].required = False
        self.fields['ship_to_3pl'].required = False
        self.fields['requested_ship_date'].required = False
        self.fields['estimated_ship_date'].required = False
        self.fields['deposit'].required = False
        self.fields['lead_time_days'].required = False
        # Port of discharge: text input with datalist for autocomplete
        self.fields['port_of_discharge'].widget.attrs.update({
            'list': 'port-of-discharge-options',
            'autocomplete': 'off',
        })
        # Set default dates for new PPOs (not editing existing ones)
        if not self.instance.pk:
            today = timezone.now().date()
            default_ship_date = today + timedelta(days=45)
            self.fields['requested_ship_date'].initial = default_ship_date.isoformat()
            self.fields['estimated_ship_date'].initial = default_ship_date.isoformat()


class PPOLineItemForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PPOLineItem
        fields = ['item', 'description', 'quantity', 'unit_price', 'cartons', 'cbm', 'notes', 'destination', 'batch_code']
        labels = {
            'item': 'Item',
            'description': 'Description',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price (USD)',
            'cartons': 'Total CTNS',
            'cbm': 'CBM',
            'notes': 'Notes',
            'destination': 'Destination (e.g., Shopify, Amazon, Walmart)',
            'batch_code': 'Batch Code',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].required = False
        self.fields['unit_price'].required = False
        self.fields['quantity'].required = False
        self.fields['cartons'].required = False
        self.fields['cbm'].required = False

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        # If no item is selected and row isn't being deleted, skip validation
        # (treat as an empty row)
        if not item and not cleaned_data.get('DELETE'):
            # Check if ANY meaningful data was entered in this row
            has_data = any([
                cleaned_data.get('description'),
                cleaned_data.get('quantity'),
                cleaned_data.get('unit_price'),
                cleaned_data.get('notes'),
                cleaned_data.get('destination'),
            ])
            if not has_data:
                # Completely empty row — mark it so the formset skips it
                return cleaned_data
        return cleaned_data


# Formset for PPOLineItem
PPOLineItemFormSet = inlineformset_factory(
    PlannedPurchaseOrder,
    PPOLineItem,
    form=PPOLineItemForm,
    extra=13,
    can_delete=True
)


class ProformaInvoiceForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ProformaInvoice
        fields = ['pi_number', 'date', 'total_amount', 'currency', 'file', 'notes']
        labels = {
            'pi_number': 'PI Number',
            'date': 'Date',
            'total_amount': 'Total Amount',
            'currency': 'Currency',
            'file': 'Upload PI Document',
            'notes': 'Notes',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class PPOAttachmentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PPOAttachment
        fields = ['file', 'file_type', 'description']
        labels = {
            'file': 'Select File',
            'file_type': 'File Type',
            'description': 'Description',
        }


class CEOApprovalForm(BootstrapMixin, forms.Form):
    APPROVAL_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    SIGNATURE_TYPE_CHOICES = [
        ('typed', 'Type your name'),
        ('image', 'Upload signature image'),
    ]
    action = forms.ChoiceField(
        choices=APPROVAL_CHOICES,
        widget=forms.RadioSelect,
        label='Action'
    )
    notes = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Approval Notes / Rejection Reason',
        help_text='Provide comments for the approval or rejection reason if applicable.'
    )
    signature_type = forms.ChoiceField(
        choices=SIGNATURE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label='Signature Method',
        initial='typed',
    )
    signature_text = forms.CharField(
        max_length=200,
        required=False,
        label='Type your full name',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Michael Todd', 'class': 'form-control'}),
    )
    signature_image = forms.ImageField(
        required=False,
        label='Upload signature image',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        sig_type = cleaned_data.get('signature_type')
        sig_text = cleaned_data.get('signature_text')
        sig_image = cleaned_data.get('signature_image')

        if action == 'approve':
            if not sig_type:
                raise forms.ValidationError('Please select a signature method to approve.')
            if sig_type == 'typed' and not sig_text:
                raise forms.ValidationError('Please type your name to sign.')
            if sig_type == 'image' and not sig_image:
                raise forms.ValidationError('Please upload a signature image to sign.')
        return cleaned_data
