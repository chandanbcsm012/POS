from django.db import models
from django.urls import reverse

# Create your models here.
class Tax_Rate(models.Model):
    name = models.CharField(max_length = 15)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "{0}@ {1} %".format(self.name, self.percentage)
    
    def get_absolute_url(self):
        return reverse('tax_rate_list') 

    class Meta:
        db_table = 'tax_rate'
