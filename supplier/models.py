from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

class Supplier(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    business_name = models.CharField(max_length=30)
    contact_Id = models.CharField(max_length=10, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    pay_num = models.IntegerField(blank=True, null=True)
    pay_term_option = models.CharField(max_length=10, blank=True, null=True)
    country = CountryField(blank_label='select country')
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)     
    address = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('supplier')

    def __str__(self):
        return self.first_name+" "+self.last_name

    class Meta:
        db_table = 'supplier'
        ordering = ['first_name']
