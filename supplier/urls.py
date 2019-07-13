from django.urls import path
from .views import SupplierView, SupplierUpdateView, SupplierDeleteView

urlpatterns = [
    path('', SupplierView.as_view(), name="supplier"),
    path('<int:pk>', SupplierUpdateView.as_view(), name="update-supplier"),
    path('<int:pk>/delete', SupplierDeleteView.as_view(), name="delete-supplier"),
]
