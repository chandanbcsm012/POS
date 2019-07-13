from django.urls import path
from tax_rate.views import TaxRateCreateView, TaxRateListView, TaxRateUpdateView, TaxRateDeleteView
urlpatterns = [
    path("list", TaxRateListView.as_view(), name="tax_rate_list" ),
    path("create", TaxRateCreateView.as_view(), name="tax_rate_create" ),
    path("<int:pk>", TaxRateUpdateView.as_view(), name="tax_rate_update" ),
    path("<int:pk>/delete", TaxRateDeleteView.as_view(), name="tax_rate_delete" )
]