from django.db import models
from django.urls import reverse
from supplier.models import Supplier
from datetime import date
from tax_rate.models import Tax_Rate


class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE)

    referance_no = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(default=date.today)

    PURCHASE_STATUS_LIST = [("", "Please Select"),
                            ("Received", "Received"),
                            ("Pending", "Pending"),
                            ("Ordered", "Ordered")]

    purchase_status = models.CharField(
        choices=PURCHASE_STATUS_LIST, max_length=20, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    document = models.FileField(upload_to='document/', blank=True, null=True)

    DISCOUNT_TYPE_LIST = [
        ("", "Please Select"),
        ("none", "None"),
        ("fixed", "Fixed Amount"),
        ("%", "Percentage (%)")
    ]

    net_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True)
    discount_type = models.CharField(
        choices=DISCOUNT_TYPE_LIST, max_length=20, blank=True, null=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    tax = models.ManyToManyField(Tax_Rate, blank=True)
    tax_details = models.CharField(max_length=200, blank=True, null=True)
    tax_total = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, default=0)
    shipping_details = models.TextField(blank=True, null=True)
    shipping_charges = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True, default=0
    )
    additional = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)
    total_purchase_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('purchase')

    class Meta:
        db_table = 'purchase'


class PurchasePayment(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    payment_date_time = models.DateTimeField(auto_now=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2)
    PAYMENT_METHOD_CHOICE = [
        ("cash", "Cash"),
        ("cheque", "Cheque"),
        ("bank", "Bank Transfer"),
        ("card", "Card"),
        ("other", "Other")
    ]
    payemnt_method = models.CharField(
        choices=PAYMENT_METHOD_CHOICE, default="cash", max_length=50, blank=True, null=True)
    card_no = models.CharField(max_length=30, blank=True, null=True)
    card_holder_name = models.CharField(max_length=50, blank=True, null=True)
    card_transaction_no = models.CharField(
        max_length=50, blank=True, null=True)
    CRAD_TYPE_CHOICE = [
        ("debitCard", "Debit Card"),
        ("creditCard", "Credit Card"),
        ("masterCard", "Master Card"),
        ("VisaCard", "Visa Card"),
    ]
    cad_type = models.CharField(
        choices=CRAD_TYPE_CHOICE, default="debitCard", max_length=20, blank=True, null=True)
    card_month = models.PositiveSmallIntegerField(blank = True, null=True)
    card_year = models.PositiveSmallIntegerField(blank = True, null=True)
    cvv = models.PositiveSmallIntegerField(blank=True, null=True)
    cheque_no = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=50, blank=True, null=True)
    payment_note = models.TextField(blank=True, null=True)
    due_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'purchase_payment'
