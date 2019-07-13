from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, DeleteView, DetailView
from .forms import CustomerForm
from .models import Customer
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse

class CustomerView(View):
    form_class = CustomerForm
    queryset = None
    template_name = 'customer/customer.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Customer.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        self.queryset = Customer.objects.all()
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'One Customer added.')

            return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})
        else:
            messages.error(request, ' Data is not valid. Please try again.')
            return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_update_form.html'

class CustomerDeleteView(DeleteView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/customer_confirm_delete.html'
    success_url = '/customer'


