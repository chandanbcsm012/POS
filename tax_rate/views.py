from django.shortcuts import render
from tax_rate.models import Tax_Rate
from tax_rate.forms import TaxRateForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

class TaxRateCreateView(CreateView):
    model = Tax_Rate
    form_class = TaxRateForm

class TaxRateListView(ListView):
    model = Tax_Rate

class TaxRateUpdateView(UpdateView):
    model = Tax_Rate
    form_class = TaxRateForm

class TaxRateDeleteView(DeleteView):
    model = Tax_Rate
    success_url = reverse_lazy('tax_rate_list')