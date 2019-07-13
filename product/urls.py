from django.urls import path
from .views import ProductView, ProductUpdateView, ProductDeleteView
urlpatterns = [
    path('', ProductView.as_view(), name="product"),
    path('<int:pk>', ProductUpdateView.as_view(), name="update-product"),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name="delete-product")
]