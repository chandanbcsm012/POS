from django.db import models
from purchase.models import Purchase
from product.models import Product

class PurchaseProductDetails(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    unit_seleing_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchase_product_details'
