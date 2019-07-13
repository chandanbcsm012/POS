from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Sale, SalePayment
from product.models import Product
from .forms import SaleForm, SalePaymentForm
from django.views.generic import View, DeleteView, UpdateView
from tax_rate.models import Tax_Rate
from sale_product_details.models import SaleProductDetails
from django.core import serializers
from django.urls import reverse_lazy
import json
from django.db.models import Sum
from purchase.views import filterTaxDetails

class AddSale(View):
    def get(self, request, *args, **kwargs):
        sale_form = SaleForm()
        sale_payment_form = SalePaymentForm()
        return render(request, "sale\partial_sale_form.html", {"form": sale_form, "pay_form": sale_payment_form})

    def post(self, request, *args, **kwargs):
        sale = request.POST.get("sale_obj", None)
        tax_id = request.POST.get("tax_id", None)
        products = request.POST.get("product_list", None)
        payment_object = request.POST.get("sale_payment", None)
        sale_dict = {}
        payment_object_dict = {}
        product_list = []
        tax_id_list = []
        msg = ""
        if sale is not None:
            sale_dict = json.loads(sale)
            sale = Sale.objects.create(**sale_dict)
            payment_dict = json.loads(payment_object)
            # if payment_dict['payemnt_method']:
            payment_dict["sale"] = sale
            SalePayment.objects.create(**payment_dict)
            if tax_id is not None:
                tax_id_list = json.loads(tax_id)
                for tax_id in tax_id_list:
                    tax = Tax_Rate.objects.get(id=tax_id)
                    sale.tax.add(tax)
            else:
                msg = "tax_error"
            if products is not None:
                product_list = json.loads(products)
                pro_list = [
                    SaleProductDetails(
                        sale=sale,
                        product_id=e["product_id"],
                        product_name=e["product_name"],
                        product_quantity=e["product_quantity"],
                        price=e["price"],
                        subtotal=e["subtotal"]
                    )for e in product_list
                ]
                created_list = SaleProductDetails.objects.bulk_create(pro_list)
                msg = "success"
            else:
                msg = "product_list_error"
        else:
            msg = "sale_error"
        return HttpResponse(msg)


def sale_list(request):
    sql = """SELECT "sale_payment"."id", "sale_payment"."sale_id", "sale_payment"."payment_date_time", "sale_payment"."paid_amount", "sale_payment"."payemnt_method", "sale_payment"."card_no", "sale_payment"."card_holder_name", "sale_payment"."card_transaction_no", "sale_payment"."cad_type", "sale_payment"."card_month", "sale_payment"."card_year", "sale_payment"."cvv", "sale_payment"."cheque_no", "sale_payment"."bank_account", "sale_payment"."payment_note", "sale_payment"."due_amount", "sale_payment"."payment_status", "sale"."id", "sale"."customer_id", "sale"."sale_date", "sale"."sale_status", "sale"."location", "sale"."pay_term_option", "sale"."pay_num", "sale"."net_total_amount", "sale"."net_amount", "sale"."discount_type", "sale"."discount", "sale"."discount_amount", "sale"."tax_details", "sale"."tax_total", "sale"."shipping_details", "sale"."shipping_charges", "sale"."sales_total", "sale"."sales_note" FROM "sale_payment" INNER JOIN "sale" ON ("sale_payment"."sale_id" = "sale"."id") and sale_payment.id =( select Max(id) from sale_payment p2 where  sale_payment.sale_id = p2.sale_id);"""
    payment = SalePayment.objects.raw(sql)
    return render(request, "sale/sale_list.html", {"payments": payment})


def save_sale_form(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sales = Sale.objects.all()
            data['html_sale_list'] = render_to_string('sale/includes/partial_sale_list.html', {
                'sales': sales
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
    else:
        form = SaleForm()
    return save_sale_form(request, form, 'sale/includes/partial_sale_create.html')


def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
    else:
        form = SaleForm(instance=sale)
    return save_sale_form(request, form, 'sale/includes/partial_sale_update.html')

class SaleUpdate(UpdateView):
    model = Sale
    form_class =  SaleForm
    template_name = "sale/sale_update.html"

class SaleDelete(DeleteView):
    model = Sale
    success_url = reverse_lazy('sale_list')
    

class SaleProductView(View):
    def get(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, pk=kwargs["pk"])
        saleProducts = SaleProductDetails.objects.filter(
            sale=sale)
        salePayment = SalePayment.objects.filter(sale=sale)
        print(saleProducts)
        return render(request, "sale/sale_detail_view.html", {"products": saleProducts, "sale": sale, "payments": salePayment})

class SalePrint(View):
    def get(self, request, *args, **kwargs):
        data = dict()
        sale = get_object_or_404(Sale, pk=kwargs["pk"])
        sale_product_details = SaleProductDetails.objects.filter(sale_id = sale.id)
        sale_payment = SalePayment.objects.filter(sale = sale).last()
        data["invoice_template"] = render_to_string("sale/sale_invoice.html", {"sale":sale, "products": sale_product_details, "payment": sale_payment})
        return JsonResponse(data)

class SalePaymentView(View):
    def get(self, request, *args, **kwargs):
        sale = get_object_or_404(Sale, pk=kwargs["pk"])
        payments = SalePayment.objects.filter(sale = sale)
        return render(request, "sale/sale_payment_list.html", {"sale": sale, "payments": payments})
        
class SalePaymentCreate(View):
    def get(self, request, *args, **kwargs):
        data = dict()
        sale = get_object_or_404(Sale, pk=kwargs["pk"])
        payment = SalePayment.objects.filter(sale = sale).last()
        paymentForm = SalePaymentForm(initial={'sale': sale, 'total_paid': payment.total_paid ,'due_amount': payment.due_amount, "payment_status": payment.payment_status})
        data['form'] = render_to_string("sale/sale_payment_create.html", {"form":paymentForm, "sale": sale, "payment": payment}, request=request)
        print(data)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()
        form = SalePaymentForm(request.POST)
        print("request.POST = ", request.POST)
        print(form)
        if form.is_valid():
            form.save()
            purchase = request.POST.get("sale")
            print(purchase)
            data["msg"] = "payment saved."
        else:
            data["msg"] = "data is not valid."
        return JsonResponse(data)

def calculateTotalSaleAmount():
    amount = Sale.objects.aggregate(Sum('sales_total'))
    return amount['sales_total__sum']

def saleTotalPaidAmount():
    amount = SalePayment.objects.aggregate(Sum('total_paid'))
    return amount['total_paid__sum']

def saleTaxTotal():
    amount = Sale.objects.aggregate(Sum('tax_total'))
    return amount["tax_total__sum"]

def saleTaxListDetails():
    taxListDetails = Sale.objects.values("tax_details")
    context = filterTaxDetails(taxListDetails)
    return context