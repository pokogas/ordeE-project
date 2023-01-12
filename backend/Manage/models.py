import uuid

from django.db import models

from Account.models import UserAccount
from django.utils import timezone


# Shop
class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    permission_code = models.IntegerField(default=333332)
    phone = models.CharField(max_length=19, default="0480-66-2212")
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)


class Room(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20)
    status_count = (
        (0, '予約'),
        (1, '空席'),
        (2, '使用中'),
        (3, '準備中'),
    )
    status = models.IntegerField(choices=status_count, default=3)
    space = models.IntegerField(default=1)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.SET_NULL, blank=True, null=True)
    reserve = models.ForeignKey('Reserve.Reserve', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Waiting(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    space = models.IntegerField(default=1)
    visits_time = models.DateTimeField()


# Menu


class Category(models.Model):
    name = models.CharField(max_length=50)
    display_priority = models.IntegerField(default=1)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    detail = models.TextField(max_length=500)
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    stock_unlimited = models.BooleanField(default=True)
    sold_out = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, blank=True)
    option = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title


# ManageMember

class ShopManagement(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    role_count = (
        (0, 'super_admin'),
        (1, 'Admin'),
        (2, 'super_staff'),
        (3, 'Staff'),
    )
    role = models.IntegerField(choices=role_count, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "shop"],
                name="shop_manage_unique"
            ),
        ]


# message関連 MessageCategory,MessageActionItem,ShopMessage,ShopMessageAction

class MessageCategory(models.Model):
    name = models.CharField(max_length=15)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    color = models.CharField(default="#FF6032FF", max_length=20)

    def __str__(self):
        return self.name


class MessageActionItem(models.Model):
    name = models.CharField(max_length=6)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class ShopMessage(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(default="")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    post_time = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(MessageCategory, on_delete=models.CASCADE, blank=True, null=True)
    system = models.BooleanField(default=False)
    oc_data = models.JSONField(blank=True, null=True)


class ShopMessageAction(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    action = models.ForeignKey(MessageActionItem, on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(ShopMessage, on_delete=models.CASCADE, blank=True, null=True)
