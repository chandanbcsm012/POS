from django.shortcuts import render
from django.views.generic import View
from purchase.views import calculateTotalPurchseAmount, purchaseTaxTotal
from sale.views import calculateTotalSaleAmount, saleTaxTotal

class DashboradView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        purchase_amount = calculateTotalPurchseAmount
        sale_amount = calculateTotalSaleAmount
        purchaseTax = purchaseTaxTotal
        saleTax = saleTaxTotal
        return render(request, self.template_name,{"purchase_amount": purchase_amount, "purchaseTaxTotal":purchaseTax, "sale_amount": sale_amount, "saleTaxTotal": saleTax})