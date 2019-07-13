from django.urls import path
from .views import UserView, ProfileView, UserLoginView, UserLogoutView

urlpatterns = [
    path('', UserView.as_view(), name="user"),
    path('profile', ProfileView.as_view(), name='profile'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('logout', UserLogoutView.as_view(), name='user-logout'),
]