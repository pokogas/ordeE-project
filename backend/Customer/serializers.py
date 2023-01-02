from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer, Order, CartItem, OrderConclusion
from Manage.serializers import MenuSerializers

User = get_user_model()


# カスタマーデータ
class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "status",
            "total_fee"
        )


# オーダーデータ
class OrderSerializers(serializers.ModelSerializer):
    menu = MenuSerializers(read_only=True)

    class Meta:
        model = Order
        fields = (
            "menu",
            "status",
            "customer",
            "count",
            "amount",
            "order_time",
            "option",
            "cook_status"
        )


# カートデータ
class CartSerializers(serializers.ModelSerializer):
    menu = MenuSerializers(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "id",
            "menu",
            "customer",
            "count",
            "amount",
            "option"
        )
