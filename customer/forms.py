from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    first_name = forms.CharField(max_length=15, required=True, label_suffix=' *')
    last_name = forms.CharField(max_length=15, required=True, label_suffix=' *')
    phone = forms.CharField(max_length=10, required=True, label_suffix=' *')

    GENDER_CHOICES = [
                    ('',"select gender"),
                    ('Male', 'Male'),
                      ('Female', 'Female')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select())

    PAY_TERM_CHOICES = [
                        ('',"select pay term"),
                        ('Day', 'Day'),
                        
                        ('Month', 'Month'),
                        ]
    pay_term_option = forms.ChoiceField(
        choices=PAY_TERM_CHOICES, widget=forms.Select())

    class Meta:
        model = Customer
        fields = '__all__'
