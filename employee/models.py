from django.db import models
from datetime import date


class Employee(models.Model):

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    phone_tow = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    office = models.CharField(max_length=30)
    start_date = models.DateField(default=date.today)
    photo = models.ImageField(upload_to='uploadedImages/')

    class Meta:
        db_table = 'employee'