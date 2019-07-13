from django.urls import path
from .views import CustomerView, CustomerUpdateView, CustomerDeleteView
urlpatterns = [
    path('', CustomerView.as_view(), name="customer"),
    path('<int:pk>', CustomerUpdateView.as_view(), name="update-customer"),
    path('<int:pk>/delete', CustomerDeleteView.as_view(), name="delete-customer"),
]