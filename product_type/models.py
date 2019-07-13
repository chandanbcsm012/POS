from django.db import models
from django.urls import reverse
# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length = 30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-type')

    class Meta:
        db_table = 'product_type'