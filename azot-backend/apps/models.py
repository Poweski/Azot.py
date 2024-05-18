import uuid

from django.db import models

# Create your models here.

class Client(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    client_info = models.OneToOneField('ClientInfo', on_delete=models.CASCADE, null=True, blank=True)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)

    def __str__(self):
        return self.email


class Seller(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    seller_info = models.OneToOneField('SellerInfo', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email


class ClientInfo(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class SellerInfo(models.Model):
    organization = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.organization


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.URLField()

    items_available = models.IntegerField()
    tags = models.CharField(max_length=100)

    owner = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.id

class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)

    def __str__(self):
        return self.id


