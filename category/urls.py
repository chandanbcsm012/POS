from django.urls import path
from .views import CategoryView, CategoryUpdateView, CategoryDeleteView
urlpatterns = [
    path("", CategoryView.as_view(), name="category"),
    path("<int:pk>/", CategoryUpdateView.as_view(), name="update-category"),
    path("<int:pk>/delete", CategoryDeleteView.as_view(), name="delete-category")
]