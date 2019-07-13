from django.db import models
from customer.models import Customer
from tax_rate.models import Tax_Rate
from datetime import date

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    sale_date = models.DateField(default=date.today)
    SALE_STATUS_LIST = [("", "Please Select"),
                            ("final", "Final"),
                            ("draft", "Draft"),
                            ("quotation", "Quotation")]

    sale_status = models.CharField(
        choices=SALE_STATUS_LIST, max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    PAY_TERM_OPTION = [("", "Please Select"),
                        ("day", "Day"),
                        ("month", "Month")
                        ]
    pay_term_option = models.CharField(max_length=10, choices=PAY_TERM_OPTION, blank=True, null=True)
    pay_num = models.IntegerField(blank=True, null=True)
    net_total_amount = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    DISCOUNT_TYPE_LIST = [
        ("", "Please Select"),
        ("none", "None"),
        ("fixed", "Fixed Amount"),
        ("%", "Percentage (%)")
    ]

    net_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPE_LIST, max_length=20, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    tax = models.ManyToManyField(Tax_Rate, blank=True)
    tax_details = models.CharField(max_length=200, blank=True, null=True)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    shipping_details = models.CharField(max_length = 30, null=True, blank=True)
    shipping_charges = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    sales_total = models.DecimalField(max_digits= 15, decimal_places=2, null=True, blank=True)
    sales_note = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'sale'

class SalePayment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    payment_date_time = models.DateTimeField(auto_now=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_paid = models.DecimalField(max_digits=15, decimal_places=2)
    PAYMENT_METHOD_CHOICE = [
        ("cash", "Cash"),
        ("cheque", "Cheque"),
        ("bank", "Bank Transfer"),
        ("card","Card"),
        ("other", "Other")
    ]
    payemnt_method = models.CharField( choices=PAYMENT_METHOD_CHOICE, max_length=50, blank=True, null=True)
    card_no = models.CharField(max_length=30, blank=True, null=True)
    card_holder_name = models.CharField(max_length=50, blank=True, null=True)
    card_transaction_no = models.CharField(max_length=50, blank=True, null=True)
    CRAD_TYPE_CHOICE = [
        ("debitCard", "Debit Card"),
        ("creditCard", "Credit Card"),        
        ("masterCard", "Master Card"),
        ("VisaCard", "Visa Card"),
    ]
    cad_type = models.CharField(choices=CRAD_TYPE_CHOICE, max_length=20, blank=True, null=True)
    card_month = models.CharField(blank=True, null=True, max_length=10)
    card_year = models.CharField(blank=True, null=True, max_length=20)
    cvv = models.CharField(blank=True, null=True, max_length=10)
    cheque_no = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=50, blank=True, null=True)
    payment_note = models.TextField(blank=True, null=True)
    due_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length = 15, blank=True, null=True)

    class Meta:
        db_table = 'sale_payment'