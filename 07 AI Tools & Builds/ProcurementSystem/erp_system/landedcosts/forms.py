from django import forms
from django.utils import timezone
from .models import LandedCostDocument
from vendors.models import Vendor, Branch


class LandedCostDocumentForm(forms.ModelForm):
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
        model = LandedCostDocument
        fields = ['ppo', 'vendor', 'branch', 'container', 'grpo',
                  'document_date', 'posting_date', 'status', 'notes']
        widgets = {
            'ppo': forms.HiddenInput(),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'container': forms.Select(attrs={'class': 'form-control'}),
            'grpo': forms.Select(attrs={'class': 'form-control'}),
            'document_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'posting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ppo'].required = False
        self.fields['vendor'].required = True
        self.fields['vendor'].queryset = Vendor.objects.filter(is_active=True).order_by('name')
        self.fields['branch'].required = False
        self.fields['branch'].queryset = Branch.objects.filter(is_active=True).order_by('name')
        self.fields['branch'].empty_label = 'Select Branch...'
        self.fields['container'].required = False
        self.fields['container'].empty_label = 'None (optional)'
        self.fields['grpo'].required = False
        self.fields['grpo'].empty_label = 'None (set on receipt)'
        self.fields['status'].initial = 'draft'
        self.fields['posting_date'].required = False

        today = timezone.now().date().isoformat()
        if not self.instance.pk:
            self.fields['document_date'].initial = today

        if self.instance.pk and self.instance.ppo:
            self.fields['ppo_number_input'].initial = self.instance.ppo.ppo_number
