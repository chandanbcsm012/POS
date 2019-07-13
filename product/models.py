from django.db import models
from django.urls import reverse
from category.models import Category
from brand.models import Brand
from product_type.models import ProductType

class Product(models.Model):
    name = models.CharField(max_length = 30)
    type = models.ForeignKey(ProductType, on_delete = models.CASCADE)
    code = models.CharField(max_length = 30, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank= True, null= True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank= True, null= True)

    TAX_METHOD_CHOICE = [('Exclusive', 'Exclusive'),
                          ('Inclusive', 'Inclusive'),
                          ]


    tax_method = models.CharField(choices=TAX_METHOD_CHOICE, max_length=20, blank= True, null= True)
    
    quantity = models.IntegerField(blank= True, null= True)
    alert_quantity = models.IntegerField(blank= True, null= True)
    image = models.ImageField(upload_to = 'productImages', blank= True, null= True)
    description = models.TextField(blank= True, null= True)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('product')

    class Meta:
        db_table = 'product'