from django.urls import path
from .views import BrandView, BrandUpdateView, BrandDeleteView
urlpatterns = [
    path("", BrandView.as_view(), name="brand"),
    path("<int:pk>", BrandUpdateView.as_view(), name="update-brand"),
    path("<int:pk>/delete", BrandDeleteView.as_view(), name="delete-brand"),
]