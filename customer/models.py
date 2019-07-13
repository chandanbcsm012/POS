from django.db import models
from datetime import date
from django.urls import reverse
from django_countries.fields import CountryField
# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer_group = models.CharField(max_length=30, blank=True, null=True)
    pay_num = models.IntegerField(blank=True, null=True)
    pay_term_option = models.CharField(max_length=30, blank=True, null=True)
    country = CountryField(blank_label='select country')
    gender = models.CharField(max_length=10, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    

    def get_absolute_url(self):
        return reverse('customer') 
    
    def __str__(self):
        return self.first_name+" "+ self.last_name
    
    class Meta:
        db_table = 'customer'
