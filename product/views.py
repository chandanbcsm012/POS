from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, DeleteView, ListView
from product.models import Product
from product.forms import ProductForm
from django.contrib import messages
from view_breadcrumbs  import BaseBreadcrumbMixin, UpdateBreadcrumbMixin, CreateBreadcrumbMixin, DetailBreadcrumbMixin , ListBreadcrumbMixin 




class ProductView(View):
    template_name = 'product/product.html'
    form_class = ProductForm
    queryset = None
    add_home = False

    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'One Product added.')
            return redirect('/product')
        else:
            messages.error(request, ' Data is not valid. Please try again.')
            return redirect('/product')
        
                   
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

class ProductDeleteView(DeleteView):
    model = Product
    add_home = False
    success_url = '/product'
