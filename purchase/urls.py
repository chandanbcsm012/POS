from django.urls import path
from purchase.views import (product_search, 
get_product, 
PurchaseList, 
PurchaseUpdateView, 
PurchaseDeleteView, 
PurchaseView, 
print_purchase,
PaymentView,
AddPayment,
PurchaseProduct
)

urlpatterns = [
    path("", PurchaseView.as_view(), name="purchase_add"),
    path("<int:pk>", PurchaseProduct.as_view(), name="purchase_view"),
    path("list", PurchaseList.as_view(), name="purchase_list"),
    path("<int:pk>/update", PurchaseUpdateView.as_view(), name="purchase_update"),
    path("<int:pk>/delete", PurchaseDeleteView.as_view(), name="purchase_delete"),
    path("ajax/product/search", product_search, name="ajax_product_search"),
    path("ajax/product/", get_product, name="ajax_product"),    
    path("<int:pk>/print", print_purchase, name="print_purchase"),
    path("<int:pk>/payment", PaymentView.as_view(), name="purchase_payment"),
    path("<int:pk>/payment/add", AddPayment.as_view(), name="add_payment")
]