from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, DeleteView
from .forms import CategoryForm
from .models import Category
from django.contrib import messages
from django.urls import reverse_lazy

class CategoryView(View):
    template_name = 'category/category.html'
    queryset = None
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        self.queryset = Category.objects.all()
        return render(request, self.template_name, {'form': self.form_class, 'data_lists': self.queryset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'One Category added.')
        else:
            messages.error(request, ' Data is not valid. Please try again.')
        
        return redirect("/category")

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'

class CategoryDeleteView(DeleteView):
    model = Category
    success_url =  reverse_lazy('category')