from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View, UpdateView, CreateView, DeleteView, ListView, View
from django.contrib import messages
from django.urls import reverse_lazy
from product.models import Product
from django.http import JsonResponse, FileResponse
from supplier.models import Supplier
import json
from django.core import serializers
from django.template.loader import render_to_string
from purchase.models import Purchase, PurchasePayment
from purchase.forms import PurchaseForm, PurchasePaymentForm
from tax_rate.models import Tax_Rate
from purchase_product_details.models import PurchaseProductDetails
from django.db.models import Max,  FilteredRelation, Q, Sum

class PurchaseView(View):
    def get(self, request, *args, **kwargs):
        purchaseForm = PurchaseForm
        context = {}
        context['form'] = purchaseForm
        return render(request, "purchase/purchase_create.html", context)

    def post(self, request, *args, **kwargs):
        purchase = request.POST.get("purchases_obj", None)
        tax_id = request.POST.get("tax_id", None)
        products = request.POST.get("products", None)
        payment_object = request.POST.get("payemnt_obj", None)
        purchase_dict = {}
        payment_object_dict = {}
        product_list = []
        tax_id_list = []
        msg = ""
        if purchase is not None:
            purchase_dict = json.loads(purchase)
            pur = Purchase.objects.create(**purchase_dict)
            payment_dict = json.loads(payment_object)
            # if payment_dict['payemnt_method']:
            payment_dict["purchase"] = pur
            PurchasePayment.objects.create(**payment_dict)
            if tax_id is not None:
                tax_id_list = json.loads(tax_id)
                for tax_id in tax_id_list:
                    tax = Tax_Rate.objects.get(id=tax_id)
                    pur.tax.add(tax)
            else:
                msg = "tax_error"
            if products is not None:
                product_list = json.loads(products)
                pro_list = [
                    PurchaseProductDetails(
                        purchase=pur,
                        name=e["name"],
                        product=Product.objects.get(id=e["product_id"]),
                        unit_cost=e["unit_cost"],
                        quantity=e["quantity"],
                        unit_seleing_price=e["unit_seleing_price"],
                        total_cost=e["total_cost"]
                    )for e in product_list
                ]
                created_list = PurchaseProductDetails.objects.bulk_create(
                    pro_list)
                msg = "success"
            else:
                msg = "product_list_error"
        else:
            msg = "purchase_error"
        return HttpResponse(msg)


class PurchaseList(View):
    def get(self, request, *args, **kwargs):
        # payments = PurchasePayment.objects.select_related("purchase").filter(
        #     id=int(PurchasePayment.objects.aggregate(Max("id")).get('id__max')))
        sql = """SELECT "purchase_payment"."id", "purchase_payment"."purchase_id", "purchase_payment"."payment_date_time", "purchase_payment"."paid_amount", "purchase_payment"."payemnt_method", "purchase_payment"."card_no", "purchase_payment"."card_holder_name", "purchase_payment"."card_transaction_no", "purchase_payment"."cad_type",
"purchase_payment"."card_month", "purchase_payment"."card_year", "purchase_payment"."cvv", "purchase_payment"."cheque_no",
"purchase_payment"."bank_account", "purchase_payment"."payment_note", "purchase_payment"."due_amount",
 "purchase_payment"."payment_status", "purchase"."id", "purchase"."supplier_id", "purchase"."referance_no",
 "purchase"."date", "purchase"."purchase_status", "purchase"."location", "purchase"."document", "purchase"."net_amount",
 "purchase"."discount_type", "purchase"."discount", "purchase"."discount_amount", "purchase"."tax_details",
 "purchase"."tax_total", "purchase"."shipping_details", "purchase"."shipping_charges", "purchase"."additional",
 "purchase"."total_purchase_amount" FROM "purchase_payment" INNER JOIN "purchase"
 ON ("purchase_payment"."purchase_id" = "purchase"."id")
 and purchase_payment.id =( select Max(id) from purchase_payment p2 where  purchase_payment.purchase_id = p2.purchase_id);
 """
        payments = PurchasePayment.objects.raw(sql)
        return render(request, 'purchase/purchase.html', {"payments": payments})


class PurchaseCreate(CreateView):
    model = Purchase
    fields = '__all__'


# class PurchaseUpdateView(UpdateView):
#     model = Purchase
#     form_class = PurchaseForm

class PurchaseUpdateView(View):
    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=kwargs["pk"])
        tax_details_list = purchase.tax_details.split(",")
        purchaseProduct = PurchaseProductDetails.objects.filter(
            purchase__id=kwargs["pk"])
        purchaseForm = PurchaseForm(request.POST or None, instance=purchase)
        return render(request, "purchase/purchase_update.html", {"form": purchaseForm, "products": purchaseProduct, "purchase": purchase, "tax_details": tax_details_list})

    def post(self, request, *args, **kwargs):
        data = dict()
        purchase = request.POST.get("purchase", None)
        tax_id = request.POST.get("tax__id", None)
        products = request.POST.get("products", None)
        if purchase is not None:
            purchase_dict = json.loads(purchase)
            purchase_id = purchase_dict["purchase__id"]
            del purchase_dict["purchase__id"]
            res = Purchase.objects.filter(
                pk=purchase_id).update(**purchase_dict)
            pur = get_object_or_404(Purchase, pk=purchase_id)
            Tax_Rate.objects.filter(purchase=pur).clear()
            # if tax_id is not None:
            #     tax_id_list = json.loads(tax_id)
            #     for tax_id in tax_id_list:
            #         tax = Tax_Rate.objects.get(id=tax_id)
            #         pur.tax.add(tax)
            print("products = ", products)
        data["purchase"] = purchase_dict
        return JsonResponse(data)


class PurchaseDeleteView(DeleteView):
    model = Purchase
    success_url = reverse_lazy('purchase_list')


def product_search(request):
    if request.is_ajax():
        search_text = request.GET.get('term', '').capitalize()
        queryset = Product.objects.filter(name__icontains=search_text)
        results = []
        for product in queryset:
            results.append(product.name)
        data = json.dumps(results)
        mimetype = 'application/json'
    else:
        data = 'fail'
        mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_product(request):
    search_text = request.GET.get('name', '').capitalize()
    data = serializers.serialize(
        "json", queryset=Product.objects.filter(name__icontains=search_text))
    return JsonResponse(data, safe=False)


def print_purchase(request, pk):
    data = dict()
    purchase = get_object_or_404(Purchase, pk=pk)
    supplier = get_object_or_404(Supplier, pk=purchase.supplier_id)
    purchase_product_details = PurchaseProductDetails.objects.filter(
        purchase_id=purchase.id)
    purchase_payment = PurchasePayment.objects.filter(
        purchase=purchase).order_by('-id')[0]
    tax_details = purchase.tax.all()
    data['invoice_template'] = render_to_string("purchase/purchase_print.html",
                                                {'purchase': purchase, 'supplier': supplier, 'product': purchase_product_details, 'payment': purchase_payment, 'tax': tax_details})
    return JsonResponse(data)

# Purchase Payment View


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        payments = PurchasePayment.objects.filter(purchase_id=id)
        purchase = get_object_or_404(Purchase, pk=id)
        data = dict()
        data['template'] = render_to_string("purchase/purchase_payment.html", {
            "payments": payments,
            "purchase": purchase
        })
        return JsonResponse(data)


class AddPayment(View):
    data = dict()

    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=kwargs["pk"])
        payments = PurchasePayment.objects.filter(purchase=purchase).last()
        # print( payments.due_amount)
        form = PurchasePaymentForm(initial={
                                   'purchase': purchase, 'due_amount': payments.due_amount, "payment_status": payments.payment_status})
        self.data["form"] = render_to_string("purchase/payment_create.html", {
                                             "form": form, "purchase": purchase, 'payments': payments}, request=request)
        return JsonResponse(self.data)

    def post(self, request, *args, **kwargs):
        form = PurchasePaymentForm(request.POST)
        print("request.POST = ", request.POST)
        print(form)
        if form.is_valid():
            form.save()
            purchase = request.POST.get("purchase")
            print(purchase)
            self.data["msg"] = "payment saved."
        else:
            self.data["msg"] = "data is not valid."
        return JsonResponse(self.data)


class PurchaseProduct(View):
    def get(self, request, *args, **kwargs):
        purchase = get_object_or_404(Purchase, pk=kwargs["pk"])
        purchaseProducts = PurchaseProductDetails.objects.filter(
            purchase=purchase)
        purchasePayment = PurchasePayment.objects.filter(purchase=purchase)
        print(purchaseProducts)
        return render(request, "purchase/detailview.html", {"product": purchaseProducts, "purchase": purchase, "payments": purchasePayment})


def calculateTotalPurchseAmount():
    amount = Purchase.objects.aggregate(Sum('total_purchase_amount'))
    return amount['total_purchase_amount__sum']

def purchaseTotalPaidAmount():
    amount = PurchasePayment.objects.aggregate(Sum('paid_amount'))
    return amount['paid_amount__sum']

def purchaseTaxTotal():
    amount = Purchase.objects.aggregate(Sum('tax_total'))
    return amount["tax_total__sum"]


def filterTaxDetails(taxList):
        tax_list = list()
        contex = dict()
        for tax in taxList:
            t = tax['tax_details'].split(",")
            tax_list.extend(t)
        tax = list()
        gst = 0
        sgst = 0
        cgst = 0
        igst = 0
        other = 0
        for t in tax_list:
            ta = t.split(" ")
            if "sgst@" in ta[2]:
                sgst = sgst + float(ta[8])
            elif "cgst@" in ta[2]:
                cgst = cgst + float(ta[8])
            elif "igst@" in ta[2]:
                igst = igst + float(ta[8])
            elif "gst@" in ta[2]:
                gst = gst + float(ta[8])
            else:
                other = other + float(ta[8])

        context = {
            "gst": gst,
            "sgst": sgst,
            "cgst": cgst,
            "igst": igst,
            "other": other
        }
        return context

def purchaseTaxListDetails():
    taxListDetails = Purchase.objects.values("tax_details")
    context = filterTaxDetails(taxListDetails)
    return context


def purchaseDueAmount():
    dueAmount = PurchasePayment.objects.all().aggregate(Sum('due_amount'))
    return dueAmount
