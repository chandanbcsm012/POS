from django.urls import path
from .views import ProductTypeView, ProductTypeUpdateView, ProductTypeDeleteView
urlpatterns = [
    path("", ProductTypeView.as_view(), name='product-type'),
    path("<int:pk>", ProductTypeUpdateView.as_view(), name='update-product-type'),
    path("<int:pk>/delete", ProductTypeDeleteView.as_view(), name='delete-product-type'),
]