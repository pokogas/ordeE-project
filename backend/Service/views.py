import datetime
import json

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

import Reserve.serializers
from Manage.models import Shop
from Reserve.models import ShopSetting
from Reserve import reserve


@api_view(["POST"])
def reservation_create(request):
    print(request.user)
    return Response({"OK"})


@api_view(["GET"])
def get_reservation_shops(request):
    serializer = Reserve.serializers.ShopSerializers(reserve.get_available_shops(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def get_shop_reservation_datetime(request):
    shop_id = Shop.objects.get(id=request.query_params.get("shop_id"))
    setting_serializer = Reserve.serializers.ShopSettingSerializers(reserve.get_shop_reservation_setting(shop_id))
    reservation_datetime = reserve.ReserveCalendar(shop_id=shop_id).get_reservation_status_calendar()
    return Response({"setting": setting_serializer.data, "datetime": reservation_datetime})


@api_view(["POST"])
def reserving(request):
    data = request.data
    serializer = Reserve.serializers.ReserveSerializers(reserve.ReserveAction(shop_id=data["shop_id"], reserve_num=data["reserve_num"]).reserving(data["reserved_datetime"], request.user))
    return Response(serializer.data)
