from django.shortcuts import render
from django.views.generic import View
from purchase.views import calculateTotalPurchseAmount, purchaseTaxTotal, purchaseTaxListDetails, purchaseTotalPaidAmount
from sale.views import calculateTotalSaleAmount, saleTaxTotal, saleTaxListDetails, saleTotalPaidAmount
from tax_rate.models import Tax_Rate

class PurchaseSaleReports(View):
    def get(self, request, *args, **kwargs):
        purchaseAmount = calculateTotalPurchseAmount()
        purchasePaidAmount = purchaseTotalPaidAmount()
        purchaseDue = purchaseAmount - purchasePaidAmount
        saleAmount = calculateTotalSaleAmount()
        salesPaidAmount = saleTotalPaidAmount() 
        salesDue = saleAmount - salesPaidAmount
        purchaseTax = purchaseTaxTotal()
        saleTax = saleTaxTotal()
        context = {
            "purchaseAmount": purchaseAmount,
            "purchaseDue": purchaseDue,
            "purchaseTax": purchaseTax,
            "saleAmount": saleAmount,
            "salesDue": salesDue,
            "saleTax": saleTax,
        }
        return render(request, "reports/purchase_sale_reports.html", context)

class PurchaseTaxDetailsReports(View):
    def get(self, request, *args, **kwargs):
        purchaseTax = purchaseTaxTotal()
        saleTax = saleTaxTotal()
        purchaseTaxDetails = purchaseTaxListDetails()
        saleTaxDetails = saleTaxListDetails()
        context = {
            "purchaseTax": purchaseTax,
            "saleTax": saleTax,
            "purchaseTaxDetails": purchaseTaxDetails,
            "saleTaxDetails": saleTaxDetails,
        }
        return render(request, "reports/tax_reports.html", context)
