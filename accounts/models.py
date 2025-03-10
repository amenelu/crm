from django.db import models
from django.contrib.auth.models import User
from .models import *


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=30, null=True)
    profile_pic = models.ImageField(default="one.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = [("Indoor", "Indoor"), ("Out Door", "Out Door")]
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=50, null=True)
    category = models.CharField(max_length=200, choices=CATEGORY, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = [
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
    ]
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
