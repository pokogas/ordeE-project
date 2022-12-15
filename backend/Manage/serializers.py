from rest_framework import serializers
from rest_framework.exceptions import APIException

from Customer.models import Order
from Manage.models import Menu, Category, ShopMessage, MessageCategory, ShopManagement, Shop
from django.contrib.auth import get_user_model


class NotAccessPermission(APIException):
    status_code = 403
    default_detail = 'NotAccessPermission'
    default_code = 'NotAccessPermission'


User = get_user_model()


# ユーザーシリアライザー
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_employee')


# カテゴリーシリアライザー
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'display_priority',
        )


# メニューシリアライザー
class MenuSerializers(serializers.ModelSerializer):
    category = CategorySerializers(many=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'title',
            'detail',
            'price',
            'stock',
            'stock_unlimited',
            'sold_out',
            'category',
            'option'
        )


# 全メニューシリアライザー
class MenusSerializers(serializers.ModelSerializer):
    category = CategorySerializers(many=True)

    class Meta:
        model = Menu
        fields = (
            'id',
            'title',
            'detail',
            'price',
            'stock',
            'stock_unlimited',
            'sold_out',
            'category',
        )


# メッセージカテゴリーシリアライザー
class MessageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCategory
        fields = (
            'id',
            'name',
            'color'
        )


# メッセージシリアライザー
class ShopMessageSerializer(serializers.ModelSerializer):
    category = MessageCategorySerializer()
    user = UserSerializers()

    class Meta:
        model = ShopMessage
        fields = (
            'user',
            'post_time',
            'category',
            'message',
            'id',
            'system',
            'oc_data'
        )


class ManageUserSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = ShopManagement
        fields = ('user', 'role')


class ShopSerializer(serializers.ModelSerializer):
    owner = UserSerializers()

    class Meta:
        model = Shop
        fields = ('name', 'id', 'phone', 'owner')


class ShopManagementSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = ShopManagement
        fields = ('role', 'shop', 'id')

# オーダーメニューデータ
class OrderMenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'id',
            'title',
        )

# オーダーデータ
class OrderSerializers(serializers.ModelSerializer):
    menu = OrderMenuSerializers()

    class Meta:
        model = Order
        fields = (
            "id",
            "menu",
            "status",
            "customer",
            "count",
            "amount",
            "order_time",
            "option",
            "cook_status"
        )
