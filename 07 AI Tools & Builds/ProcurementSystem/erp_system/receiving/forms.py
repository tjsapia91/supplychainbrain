from django import forms
from django.utils import timezone
from .models import GoodsReceiptPO
from vendors.models import ThreePLProvider


class GoodsReceiptPOForm(forms.ModelForm):
    # PPO number text field — user types a number, JS looks it up and sets the hidden ppo FK
    ppo_number_input = forms.CharField(
        label='PO #',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter PO number to look up',
            'autocomplete': 'off',
        }),
    )

    class Meta:
        model = GoodsReceiptPO
        fields = ['ppo', 'vendor', 'receipt_date', 'posting_date', 'status', 'warehouse', 'reference', 'notes']
        widgets = {
            'ppo': forms.HiddenInput(),
            'vendor': forms.HiddenInput(),
            'receipt_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'posting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AWB/BL or tracking #'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'reference': 'AWB/BL / Reference',
            'warehouse': 'Receiving 3PL',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ppo'].required = False  # Will be set by JS
        self.fields['vendor'].required = False  # Auto-populated from PPO
        self.fields['warehouse'].required = False
        self.fields['warehouse'].queryset = ThreePLProvider.objects.filter(is_active=True).order_by('name')
        self.fields['warehouse'].empty_label = 'Select 3PL...'
        self.fields['status'].initial = 'draft'

        # Set default dates
        today = timezone.now().date().isoformat()
        if not self.instance.pk:
            self.fields['receipt_date'].initial = today
            self.fields['posting_date'].initial = today

        # Pre-fill PPO number on edit
        if self.instance.pk and self.instance.ppo:
            self.fields['ppo_number_input'].initial = self.instance.ppo.ppo_number
