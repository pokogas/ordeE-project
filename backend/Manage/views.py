from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Customer.models import OrderConclusion, Order
from .models import ShopManagement, Shop, ShopMessage, MessageCategory, Room, Waiting
from .permission import access_authority_check
from .serializers import ShopMessageSerializer, MessageCategorySerializer, ManageUserSerializer, ShopSerializer, \
    ShopManagementSerializer, OrderSerializers, RoomsSerializers, WaitingSerializers, ReserveSerializers
from Reserve.models import Reserve
import datetime
from django.utils import timezone

User = get_user_model()

# TODO @csrf_protect csrfを有効にする

# メッセージカテゴリー
@api_view(["GET"])
@access_authority_check("CHAT")
def messages_custom_category(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    category = MessageCategory.objects.filter(shop=shop)
    serializer = MessageCategorySerializer(category, many=True)
    return Response(serializer.data)


# チャット
@api_view(["GET"])
@access_authority_check("CHAT")
def to_day_messages(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    first_time = timezone.now() - datetime.timedelta(days=2)
    end_time = timezone.now() + datetime.timedelta(minutes=1)
    messages = ShopMessage.objects.filter(shop=shop, post_time__range=[first_time, end_time]).order_by(
        "post_time")
    serializer = ShopMessageSerializer(messages, many=True)
    return Response(serializer.data)


# アクセスチェック(テスト用)
# カスタマーデータ
@api_view(["GET"])
@access_authority_check("ACCESS_MENU")
def test(request):
    return Response({"detail": "authSuccess"})


# ホーム
@api_view(["GET"])
@access_authority_check("ACCESS_HOME")
def access_home(request):
    return Response({"detail": "authSuccess"})


# 注文取得
@api_view(["GET"])
@access_authority_check("ORDER")
def get_order(request):
    oc = OrderConclusion.objects.get(id=request.query_params.get("oc_id"))
    serializer = OrderSerializers(oc.orders, many=True)
    return Response(serializer.data)


# 注文取得
@api_view(["GET"])
@access_authority_check("ORDER")
def get_orders(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    order = Order.objects.filter(customer__shop=shop, status=False)
    serializer = OrderSerializers(order, many=True)
    return Response(serializer.data)


def ws_send_order_action(shop_id, order_id, direction):
    channel_layer = get_channel_layer()
    order_ws_data = {
        'type': direction,
        'order_id': order_id,
    }
    async_to_sync(channel_layer.group_send)(
        f'order_{str(shop_id)}',
        order_ws_data,
    )


@api_view(["POST"])
@access_authority_check("ORDER")
@csrf_protect
def order_action(request):
    print(request.headers)
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    order_id = request.query_params.get("order_id")
    direction = request.query_params.get("direction")
    order = Order.objects.get(customer__shop=shop, id=order_id)
    if direction == "COOK_COMP":
        order.cook_status = True
        ws_send_order_action(shop.id, order_id, direction)
    if direction == "COMP":
        order.status = True
        ws_send_order_action(shop.id, order_id, direction)
    order.save()
    return Response({"detail": "success"})


# オーダー 注文履歴
@api_view(["GET"])
@access_authority_check("ACCESS_ORDER_HISTORY")
def access_order_history(request):
    return Response({"detail": "authSuccess"})


# フロアROOM取得
@api_view(["GET"])
@access_authority_check("ROOM")
def get_rooms(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    rooms = Room.objects.filter(shop=shop).order_by('name')
    serializer = RoomsSerializers(rooms, many=True)
    return Response(serializer.data)

# 待機者リスト取得 (当日)
@api_view(["GET"])
def get_waiting_list(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    waiting_list = Waiting.objects.filter(shop=shop, visits_time__day=datetime.date.today().day, active=True).order_by('visits_time')
    serializer = WaitingSerializers(waiting_list, many=True)
    return Response(serializer.data)

# 待機者チケットさ作成
@api_view(["POST"])
def waiting_ticket_create(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    space = request.query_params.get("space")
    waiting = Waiting.objects.create(shop=shop, space=int(space), visits_time=timezone.now())
    serializer = WaitingSerializers(waiting)
    return Response(serializer.data)

# 予約者リスト取得 (当日) // TODO 権限つけろ 上2こも
@api_view(["GET"])
def get_today_reserve_list(request):
    shop = Shop.objects.get(id=request.query_params.get("shop_id"))
    reserve_list = Reserve.objects.filter(shop=shop, reservation_date__day=datetime.date.today().day, active=True).order_by('reservation_date')
    serializer = ReserveSerializers(reserve_list, many=True)
    return Response(serializer.data)

# メニュー
@api_view(["GET"])
@access_authority_check("ACCESS_MENU")
def access_menu(request):
    return Response({"detail": "authSuccess"})


# フロア
@api_view(["GET"])
@access_authority_check("ACCESS_ROOM")
def access_room(request):
    return Response({"detail": "authSuccess"})


# 店舗情報
@api_view(["GET"])
@access_authority_check("ACCESS_SHOP_INFO")
def access_shop_info(request):
    return Response({"detail": "authSuccess"})


# 管理店舗取得API
@api_view(["GET"])
@access_authority_check("DEFAULT")
def shops(request):
    type = request.query_params.get("type")
    if type == "userManage":
        manage = ShopManagement.objects.filter(user=request.user, is_active=True).order_by("role")[0]
        if manage.role == 0:
            manage = ShopManagement.objects.filter(user=request.user, is_active=True).exclude(role=0,
                                                                                              shop=None).order_by(
                "role")
            serializer = ShopManagementSerializer(manage, many=True)
            return Response(serializer.data)
        manage = ShopManagement.objects.filter(user=request.user, is_active=True).order_by("role")
        serializer = ShopManagementSerializer(manage, many=True)
        return Response(serializer.data)
    if type == "all":
        shop = Shop.objects.all()
        serializer = ShopSerializer(shop, many=True)
        return Response(serializer.data)
    return Response({"detail": "Please put type in the parameter. The type can be userManage or all"})


"""
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
"""


# ManageUserMe
@api_view(["GET"])
@access_authority_check("DEFAULT")
def manage_user_me(request):
    manage = ShopManagement.objects.filter(user=request.user, is_active=True).order_by("role")[0]
    serializer = ManageUserSerializer(manage, many=False)
    return Response(serializer.data)
