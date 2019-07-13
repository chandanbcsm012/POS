from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
class UserView(View):
    template_name = 'user/user.html'
    
    def get(self, request, *args, **kwargs):
        user  = User.objects.all()
        return render(request, self.template_name,{'users':user})

# Create your views here.
class ProfileView(View):
    template_name = 'user/profile.html'
 
    def get(self, request, *args, **kwargs):
        current_user = request.user
        return render(request, self.template_name, {'user':current_user})

class UserLoginView(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        context = {'username':username, 'password':password}
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully.')
            return redirect('dashboard')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid Login')
            return render(request, self.template_name, context)

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('user-login')
    