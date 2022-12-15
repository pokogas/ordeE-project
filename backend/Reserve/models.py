import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from Account.models import UserAccount
from django.utils import timezone
from Manage.models import Shop


class Reserve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reservation_date = models.DateTimeField(default=timezone.now)
    staff_publication = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    reserve_num = models.IntegerField(default=1)
    reserver_id = models.IntegerField(default=1)
    reserver_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)


class ShopSetting(models.Model):
    reservation_function_using = models.BooleanField(default=True)
    approval_system = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    one_hour_max_reservation = models.IntegerField(default=2)  # 1時間最大2件まで予約可能 例 12時に2人予約が居たら 12時に新規予約不可
    max_visits_count = models.IntegerField(default=10)  # 定員です
    reservation_shortest_reception_hours = models.IntegerField(default=3,validators=[MinValueValidator(1)])  # 予約はint時間後から受付可能です
    reservation_longest_reception_hours = models.IntegerField(default=240,validators=[MinValueValidator(48)])  # 予約はint時間後まで受付可能です
    first_reservation_releasing_time = models.IntegerField(default=9)  # 予約はint時から受付可能です
    last_reservation_releasing_time = models.IntegerField(default=19)  # 予約はint時まで受付可能です

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["shop"],
                name="shop_setting_unique"
            ),
        ]
