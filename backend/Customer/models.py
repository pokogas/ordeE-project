import uuid
from django.db import models
from django.utils import timezone
from Account.models import UserAccount
from Manage.models import Room, Menu, Shop, ShopMessage


# Create your models here.

class Customer(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    account_coordination = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, default="お客")
    status = models.BooleanField(default=True)
    total_fee = models.FloatField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(blank=True, default=False)
    cook_status = models.BooleanField(blank=True, default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(default=1)
    amount = models.FloatField(default=100)
    order_time = models.DateTimeField(default=timezone.now)
    option = models.JSONField(blank=True, null=True)


class OrderConclusion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orders = models.ManyToManyField(Order, blank=True)


class CartItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(default=1)
    amount = models.FloatField(blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    option = models.JSONField(blank=True, null=True)
