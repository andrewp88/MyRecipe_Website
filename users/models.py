from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dateofbirth = models.DateField()
    registrationDate = models.DateField().auto_now_add
    password = models.CharField(max_length=64)
    profileImg = models.ImageField()
    country = models.CharField(max_length=35 , default="Europe_default")
    email = models.EmailField()
