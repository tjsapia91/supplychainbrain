from django import forms
from .models import APInvoice


class APInvoiceForm(forms.ModelForm):
    class Meta:
        model = APInvoice
        fields = [
            'invoice_number', 'vendor', 'ppo', 'grpo', 'invoice_date', 'due_date',
            'total_amount', 'currency', 'status', 'file', 'match_notes', 'payment_date', 'payment_reference'
        ]
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'ppo': forms.Select(attrs={'class': 'form-control'}),
            'grpo': forms.Select(attrs={'class': 'form-control'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'match_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_reference': forms.TextInput(attrs={'class': 'form-control'}),
        }
