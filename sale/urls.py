from django.urls import path
from sale import views

urlpatterns = [
    path('list', views.sale_list, name='sale_list'),
    path('', views.AddSale.as_view(), name='sale_create'),
    path('<int:pk>', views.SaleProductView.as_view(), name="sale_details"),
    path('<int:pk>/delete/', views.SaleDelete.as_view(), name="sale_delete"),
    path('<int:pk>/print/', views.SalePrint.as_view(), name="sale_print"),
    path('<int:pk>/update/', views.SaleUpdate.as_view(), name="sale_update"),
    path("<int:pk>/payment/", views.SalePaymentView.as_view(), name="sale_payment"),
    path("<int:pk>/payment/create/", views.SalePaymentCreate.as_view(), name="sale_payment_create")
]
