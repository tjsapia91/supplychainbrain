from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_no', 'description', 'in_stock', 'default_warehouse',
            'last_purchase_date', 'qty_ordered_by_customers', 'abc_classification',
            'qty_ordered_from_vendors', 'property_1', 'property_2', 'height_uom',
            'length_uom', 'width_uom', 'weight_uom', 'superseding_item',
            'upc_inner_carton_qty', 'upc_master_carton_qty', 'master_carton_volume',
            'issue_price', 'height_purchasing_unit', 'inactive', 'branch'
        ]
        widgets = {
            'item_no': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'default_warehouse': forms.Select(attrs={'class': 'form-control'}),
            'last_purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'qty_ordered_by_customers': forms.NumberInput(attrs={'class': 'form-control'}),
            'abc_classification': forms.Select(attrs={'class': 'form-control'}),
            'qty_ordered_from_vendors': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_1': forms.TextInput(attrs={'class': 'form-control'}),
            'property_2': forms.TextInput(attrs={'class': 'form-control'}),
            'height_uom': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'length_uom': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'width_uom': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight_uom': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'superseding_item': forms.TextInput(attrs={'class': 'form-control'}),
            'upc_inner_carton_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'upc_master_carton_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'master_carton_volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'issue_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'height_purchasing_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'inactive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
        }
