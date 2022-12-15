import json
from functools import wraps
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

import Manage.serializers
from Manage.models import Menu, Category, ShopMessage
from Manage.serializers import MenuSerializers, CategorySerializers, MenusSerializers, ShopMessageSerializer
from .models import Customer, Order, CartItem, OrderConclusion
from .serializers import CustomerSerializers, OrderSerializers, CartSerializers


# カスタマー情報が見つからない
class CustomerNotFound(APIException):
    status_code = 400
    default_detail = 'Customerが見つかりませんでした。'
    default_code = 'Customer-not-found'


# カスタマーの利用不可
class CustomerUnusable(APIException):
    status_code = 400
    default_detail = '利用期限が過ぎているか許可されていません。'
    default_code = 'customer-unusable'


# バリデーションエラー
class CustomerIDValidationError(APIException):
    status_code = 400
    default_detail = 'customerIDがが無効な形式です。'
    default_code = 'customer-validation-error'


# カスタマーチェック
# ここでcustomerIDの有効性/ステータス/バリデーションをチェックします
# 使い方@api_view(["GET"])の下に@customer_checkを設置してください
def customer_check(func):
    @wraps(func)
    def checker(request, *args, **kwargs):
        try:
            customer_id = request.query_params.get("customer_id")
            customer = Customer.objects.get(id=customer_id)
            if not customer.status:
                raise CustomerUnusable
        except Customer.DoesNotExist:
            raise CustomerNotFound
        except ValidationError:
            raise CustomerIDValidationError
        return func(request, *args, **kwargs)

    return checker


# カートストックチェック
def cartStockCheck(menu_id, count, customer, count_before_change):
    menu = Menu.objects.get(id=menu_id)
    carts = CartItem.objects.filter(customer=customer)
    stock = menu.stock
    for cart in carts:
        if menu == cart.menu:
            stock -= cart.count
    stock += count_before_change
    if stock < count and not menu.stock_unlimited or menu.sold_out:
        return False
    return True


# メニューの合計料金計算
def menuTotalChargeCalculation(menu_id, count, options):
    menu = Menu.objects.get(id=menu_id)
    options = options
    total_amount = menu.price
    for optionBox in options:
        if isinstance(optionBox, list):
            for option in optionBox:
                total_amount += option["fee"]
        else:
            total_amount += optionBox["fee"]
    total_amount *= count
    return total_amount


# オーダーストックチェック
def orderStockCheck(menu_id, customer):
    menu = Menu.objects.get(id=menu_id)
    carts = CartItem.objects.filter(customer=customer)
    stock = menu.stock
    cart_count = 0
    for cart in carts:
        if menu == cart.menu:
            cart_count += cart.count
    if stock < cart_count and not menu.stock_unlimited or menu.sold_out:
        return False
    return True


# cartItemAllRemove
def cartItemAllRemove(customer):
    cart = CartItem.objects.filter(customer=customer)
    for i in cart:
        i.delete()


# ws_send_order
def ws_send_order(customer, oc_id):
    oc_data = {
        'room': customer.room.name,
        'oc_id': str(oc_id)
    }

    channel_layer = get_channel_layer()
    message_db = ShopMessage.objects.create(shop_id=str(customer.shop_id),
                                            message=f'OCID:{oc_id}',
                                            category_id=2,
                                            system=True,
                                            oc_data=oc_data)
    data_json = json.dumps(ShopMessageSerializer(message_db).data)
    order_chat_data = {
        'type': 'chat_message',
        'data_json': data_json,
    }
    order_ws_data = {
        'type': 'ORDER',
        'orders': json.dumps(Manage.serializers.OrderSerializers(OrderConclusion.objects.get(id=str(oc_id)).orders, many=True).data, cls=DjangoJSONEncoder),
    }
    async_to_sync(channel_layer.group_send)(
        f'chat_{str(customer.shop_id)}',
        order_chat_data,
    )
    async_to_sync(channel_layer.group_send)(
        f'order_{str(customer.shop_id)}',
        order_ws_data,
    )


def cartAction(customer_id, data):
    customer = Customer.objects.get(id=customer_id)
    action = data["action"]
    if action == "ADD":
        menu_id = data["menu_id"]
        count = data["count"]
        options = data["option"]
        menu = Menu.objects.get(id=menu_id)
        amount = menuTotalChargeCalculation(menu_id, count, options)
        if not cartStockCheck(menu_id, count, customer, 0):
            res = {
                "detail": {
                    "error": "stockError",
                }
            }
            return Response(res, status=400)
        CartItem.objects.create(menu=menu, count=count, option=options, amount=amount, customer=customer)
        return Response({"detail": "complete"})
    elif action == "REMOVE":
        cart_id = data["cart_id"]
        cart = CartItem.objects.get(id=cart_id)
        cart.delete()
        return Response({"detail": "complete"})
    elif action == "ALL-REMOVE":
        cartItemAllRemove(customer)
        return Response({"detail": "complete"})
    elif action == "CHANGE":
        cart_id = data["cart_id"]
        count = data["count"]
        cart = CartItem.objects.get(id=cart_id)
        menu_id = cart.menu.id
        amount = menuTotalChargeCalculation(menu_id, count, cart.option)
        if not cartStockCheck(menu_id, count, customer, cart.count):
            res = {
                "detail": {
                    "error": "stockError",
                }
            }
            return Response(res, status=400)
        cart.count = count
        cart.amount = amount
        cart.save()
        return Response({"detail": "complete"})


def orderAction(customer_id):
    customer = Customer.objects.get(id=customer_id)
    cart_items = CartItem.objects.filter(customer=customer)
    sold_menus = []
    for cart_item in cart_items:
        if not orderStockCheck(cart_item.menu.id, customer):
            cart = CartItem.objects.get(id=cart_item.id)
            sold_menus.append(CartSerializers(cart).data)
    if not sold_menus:
        oc = OrderConclusion.objects.create()
        for cart_item in cart_items:
            order = Order.objects.create(menu=cart_item.menu, customer=customer, count=cart_item.count,
                                         amount=cart_item.amount,
                                         option=cart_item.option)
            oc.orders.add(order)
            menu = Menu.objects.get(id=cart_item.menu.id)
            customer.total_fee += cart_item.amount
            customer.save()
            if not menu.stock_unlimited:
                menu.stock -= cart_item.count
                menu.save()
        cartItemAllRemove(customer)
        ws_send_order(customer, oc.id)
        return Response({"detail": "complete"})
    return Response({"detail": {
        "error": "stockError",
        "soldMenus": sold_menus
    }}, status=400)


# カスタマーデータ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def detail(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    serializer = CustomerSerializers(customer)
    return Response(serializer.data)


# 注文データ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def order_data(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    orders = Order.objects.filter(customer=customer).order_by("-order_time")
    serializer = OrderSerializers(orders, many=True)
    return Response(serializer.data)


# カートデータ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def cart_data(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    cart_items = CartItem.objects.filter(customer=customer)
    serializer = CartSerializers(cart_items, many=True)
    return Response(serializer.data)


# メニューデータ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def menu_data(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    menus = Menu.objects.filter(shop=customer.shop)
    serializer = MenusSerializers(menus, many=True)
    return Response(serializer.data)


# メニュー詳細データ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def menu_detail_data(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    menu_id = int(request.query_params.get("menu_id"))
    menu = Menu.objects.get(id=menu_id, shop=customer.shop)
    serializer = MenuSerializers(menu)
    return Response(serializer.data)


# カテゴリーデータ
@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@customer_check
def category_data(request):
    customer_id = request.query_params.get("customer_id")
    customer = Customer.objects.get(id=customer_id)
    category = Category.objects.filter(shop=customer.shop)
    serializer = CategorySerializers(category, many=True)
    return Response(serializer.data)


# カートアクション
@api_view(["POST"])
@permission_classes((AllowAny,))
@customer_check
def cart_action(request):
    customer_id = request.query_params.get("customer_id")
    return cartAction(customer_id, request.data)


# オーダーアクション
@api_view(["POST"])
@permission_classes((AllowAny,))
@customer_check
def order_action(request):
    customer_id = request.query_params.get("customer_id")
    return orderAction(customer_id)
