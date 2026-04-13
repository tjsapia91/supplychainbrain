from django import forms
from .models import ReportSource, UploadedReport


class ReportUploadForm(forms.Form):
    """Form for uploading CSV/Excel report files from external systems."""

    report_source = forms.ModelChoiceField(
        queryset=ReportSource.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Select the system this data was exported from.',
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls,.tsv',
        }),
        help_text='Upload a CSV, XLSX, or TSV file.',
    )
    data_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        help_text='Date the data was current (defaults to today).',
    )

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            ext = f.name.rsplit('.', 1)[-1].lower() if '.' in f.name else ''
            if ext not in ('csv', 'xlsx', 'xls', 'xlsm', 'tsv'):
                raise forms.ValidationError(
                    'Unsupported file type. Please upload a .csv, .xlsx, or .tsv file.'
                )
            # 25 MB limit
            if f.size > 25 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 25 MB.')
        return f
