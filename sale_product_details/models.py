from django.db import models
from sale.models import Sale
from product.models import Product

class SaleProductDetails(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 50, null= True, blank = True)
    product_quantity = models.IntegerField(null= True, blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places=2, null= True, blank = True)
    subtotal = models.DecimalField(max_digits=10, decimal_places = 2, null= True, blank = True)
    
    class Meta:
        db_table = 'sale_product_details'