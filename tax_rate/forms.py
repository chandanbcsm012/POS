from django import forms
from tax_rate.models import Tax_Rate

class TaxRateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'pattern':'[A-Za-z]{3,4}', 'title': 'Must contains 3 or 4 characters.'}))
    percentage = forms.IntegerField(widget=forms.NumberInput(attrs={'autocomplete':'off', 'max':'100'}))
    class Meta:
        model = Tax_Rate
        fields = '__all__'