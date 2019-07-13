# Generated by Django 2.2 on 2019-05-29 07:15

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('business_name', models.CharField(max_length=30)),
                ('contact_Id', models.CharField(blank=True, max_length=10, null=True)),
                ('gst_number', models.CharField(blank=True, max_length=15, null=True)),
                ('opening_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_num', models.IntegerField(blank=True, null=True)),
                ('pay_term_option', models.CharField(blank=True, max_length=10, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'supplier',
                'ordering': ['first_name'],
            },
        ),
    ]
