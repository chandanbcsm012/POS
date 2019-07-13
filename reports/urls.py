from django.urls import path
from reports import views

urlpatterns = [
    path("purchase-sales", views.PurchaseSaleReports.as_view(), name="p_s_r" ),
    path("tax", views.PurchaseTaxDetailsReports.as_view(), name="t_r")
]