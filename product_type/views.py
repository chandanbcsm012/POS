from django.shortcuts import render, HttpResponse
from django.views.generic import View, UpdateView, DeleteView
from .forms import ProductTypeForm
from .models import ProductType
from django.contrib import messages
from django.urls import reverse_lazy


class ProductTypeView(View):
    template_name = 'product_type/productType.html'
    queryset = None
    form_class = ProductTypeForm

    def get(self, request, *args, **kwargs):
        self.queryset = ProductType.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'One ProductType added.')
            self.queryset = ProductType.objects.all()
            return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})
        else:
            messages.error(request, ' Data is not valid. Please try again.')
            return render(request, self.template_name)


class ProductTypeUpdateView(UpdateView):
    model = ProductType
    form_class = ProductTypeForm


class ProductTypeDeleteView(DeleteView):
    model = ProductType
    success_url =  reverse_lazy('product-type')
