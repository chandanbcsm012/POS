from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, DeleteView
from .forms import BrandForm
from .models import Brand
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


class BrandView(View):
    template_name = 'brand/brand.html'
    form_class = BrandForm
    queryset = None

    def get(self, request, *args, **kwargs):
        self.queryset = Brand.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'One Category added.')
            return redirect('brand')
        else:
            messages.error(request, ' Data is not valid. Please try again.')
            return redirect('brand')

class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm

class BrandDeleteView(DeleteView):
    model = Brand
    success_url = '/brand'