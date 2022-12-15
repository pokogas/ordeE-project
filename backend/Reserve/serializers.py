from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Reserve, ShopSetting
from Manage.models import Shop
from Manage.serializers import MenuSerializers

User = get_user_model()


# カスタマーデータ
class ShopSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            "id",
            "name",
            "phone"
        )

# カスタマーデータ
class ShopSettingSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShopSetting
        fields = (
            "one_hour_max_reservation",
            "max_visits_count",
            "reservation_shortest_reception_hours",
            "reservation_longest_reception_hours",
            "first_reservation_releasing_time",
            "last_reservation_releasing_time",
        )