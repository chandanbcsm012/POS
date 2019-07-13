from django.db import models

# Create your models here.
class Theame(models.Model):
    name = models.CharField(max_length=100)
    colorPrimary = models.CharField(max_length=100)
    colorSecondary = models.CharField(max_length=100)
    nightMode = models.CharField(max_length=100)
    backgroundImage = models.ImageField(upload_to = "teameImageBackground")