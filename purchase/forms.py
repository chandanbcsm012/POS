from django import forms
from purchase.models import Purchase, PurchasePayment
from supplier.models import Supplier


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'

class PurchasePaymentForm(forms.ModelForm):
    class Meta:
        model = PurchasePayment
        fields = '__all__'