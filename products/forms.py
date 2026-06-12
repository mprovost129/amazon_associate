from django import forms


class ProductImportForm(forms.Form):
    csv_file = forms.FileField(help_text='Upload a CSV using the product export/template columns.')
    update_existing = forms.BooleanField(required=False, initial=True, help_text='Update products that match an existing slug.')
