from django.urls import path
from dashboard.views import DashboradView
urlpatterns = [
    path('', DashboradView.as_view(), name='dashboard'),
]