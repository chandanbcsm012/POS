from django.db import models
from django.urls import reverse
# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("brand")

    class Meta:
        db_table = 'brand'

        