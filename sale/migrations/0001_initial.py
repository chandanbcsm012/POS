# Generated by Django 2.2 on 2019-06-11 05:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('tax_rate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateField(default=datetime.date.today)),
                ('sale_status', models.CharField(blank=True, choices=[('', 'Please Select'), ('final', 'Final'), ('draft', 'Draft'), ('quotation', 'Quotation')], max_length=20, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('pay_term_option', models.CharField(blank=True, choices=[('', 'Please Select'), ('day', 'Day'), ('month', 'Month')], max_length=10, null=True)),
                ('pay_num', models.IntegerField(blank=True, null=True)),
                ('net_total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('net_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('discount_type', models.CharField(blank=True, choices=[('', 'Please Select'), ('none', 'None'), ('fixed', 'Fixed Amount'), ('%', 'Percentage (%)')], max_length=20, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('tax_details', models.CharField(blank=True, max_length=200, null=True)),
                ('tax_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('shipping_details', models.CharField(blank=True, max_length=30, null=True)),
                ('shipping_charges', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('sales_total', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('sales_note', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('tax', models.ManyToManyField(blank=True, to='tax_rate.Tax_Rate')),
            ],
            options={
                'db_table': 'sale',
            },
        ),
        migrations.CreateModel(
            name='SalePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date_time', models.DateTimeField(auto_now=True)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('payemnt_method', models.CharField(blank=True, choices=[('', 'Please Select'), ('cash', 'Cash'), ('cheque', 'Cheque'), ('bank', 'Bank Transfer'), ('card', 'Card'), ('other', 'Other')], max_length=50, null=True)),
                ('card_no', models.CharField(blank=True, max_length=30, null=True)),
                ('card_holder_name', models.CharField(blank=True, max_length=50, null=True)),
                ('card_transaction_no', models.CharField(blank=True, max_length=50, null=True)),
                ('cad_type', models.CharField(blank=True, choices=[('', 'Please Select'), ('creditCard', 'Credit Card'), ('debitCard', 'Debit Card'), ('masterCard', 'Master Card'), ('VisaCard', 'Visa Card')], max_length=20, null=True)),
                ('card_month', models.CharField(blank=True, max_length=10, null=True)),
                ('card_year', models.CharField(blank=True, max_length=20, null=True)),
                ('cvv', models.CharField(blank=True, max_length=10, null=True)),
                ('cheque_no', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_note', models.TextField(blank=True, null=True)),
                ('due_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=15, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sale.Sale')),
            ],
            options={
                'db_table': 'sale_payment',
            },
        ),
    ]
