from django import forms
from .models import Brand
class BrandForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Brand