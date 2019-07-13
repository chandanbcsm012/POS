from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm
from django.views.generic import View, UpdateView, DeleteView
from django.contrib import messages


class SupplierView(View):
    form_class = SupplierForm
    queryset = None
    template_name = 'supplier/supplier.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Supplier.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'One Supplier added.')
            return redirect("supplier")
        else:
            messages.error(request, ' Data is not valid. Please try again.')
            return redirect("supplier")


class SupplierUpdateView(UpdateView):
    form_class = SupplierForm
    model = Supplier
    template_name = 'supplier/supplier_update_form.html'


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = '/supplier'
