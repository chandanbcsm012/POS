from django import forms
from sale.models import Sale
from customer.models import Customer
from .models import SalePayment

class SaleForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())

    class Meta:
        model = Sale
        fields = "__all__"

class SalePaymentForm(forms.ModelForm):

    class Meta:
        model = SalePayment
        fields = "__all__"
        