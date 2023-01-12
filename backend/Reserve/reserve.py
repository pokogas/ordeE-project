import random
import time

from .models import ShopSetting, Reserve
from Manage.models import Shop
import datetime

def reservation_id_generation(shop_id, reserved_datetime):
    # 指定した予約日から存在するreserver_idをlist化
    id_list = list(Reserve.objects.filter(reservation_date__date=reserved_datetime.strftime('%Y-%m-%d'), shop=shop_id).values_list("reserver_id", flat=True))
    reserver_id = 0
    flag = True
    while flag:
        reserver_id = random.randrange(1000,9999)
        flag = reserver_id in id_list
    return reserver_id


def date_range(start, stop, step=datetime.timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step


def hour_range(start, stop, step=datetime.timedelta(hours=1)):
    current = start
    while current <= stop:
        yield current
        current += step


def get_available_shops():
    return Shop.objects.filter(shopsetting__reservation_function_using=True)


def get_shop_reservation_setting(shop_id):
    return ShopSetting.objects.get(shop_id=shop_id)

# 1時間当たりの予約数の制限確認
def reservation_limit_check(reserved_datetime, setting, shop_id):
    if setting.one_hour_max_reservation <= len(Reserve.objects.filter(reservation_date=reserved_datetime, shop=shop_id)):
        return False
    return True

def reservation_check(reserved_datetime, shop_id):
    calendar = ReserveCalendar(shop_id=shop_id, get_option="calendar_only").get_reservation_status_calendar()
    if reserved_datetime.strftime('%Y-%m-%d') in calendar:
        if reserved_datetime.strftime('%Y-%m-%d %H:%M') in calendar[reserved_datetime.strftime('%Y-%m-%d')]:
            return True
    return False

class ReserveCalendar:

    def __init__(self, shop_id, get_option="calendar_as_reservation_number"):
        self.shop_id = shop_id
        self.get_option = get_option

    def get_reservation_status_hours(self, date):
        res = {}
        setting = get_shop_reservation_setting(self.shop_id)
        now_date = datetime.datetime.now()
        reserved_shortest_hour = datetime.datetime(date.year, date.month, date.day,
                                                   setting.first_reservation_releasing_time)
        reserved_longest_hour = datetime.datetime(date.year, date.month, date.day,
                                                  setting.last_reservation_releasing_time)
        if date.date() == now_date.date() and date.hour >= setting.first_reservation_releasing_time:
            reserved_shortest_hour = datetime.datetime(date.year, date.month, date.day, date.hour + 1)
        if self.get_option == "calendar_only":
            for date in hour_range(reserved_shortest_hour, reserved_longest_hour):
                res[date.strftime('%Y-%m-%d %H:%M')] = 0
        elif self.get_option == "calendar_as_reservation_number":
            for date in hour_range(reserved_shortest_hour, reserved_longest_hour):
                res[date.strftime('%Y-%m-%d %H:%M')] = len(
                    Reserve.objects.filter(reservation_date=date, shop=self.shop_id))
        return res

    def get_reservation_status_calendar(self):
        res = {}
        setting = get_shop_reservation_setting(self.shop_id)
        now_date = datetime.datetime.now()
        reserved_shortest_date = now_date + datetime.timedelta(hours=setting.reservation_shortest_reception_hours)
        reserved_longest_date = reserved_shortest_date + datetime.timedelta(
            hours=setting.reservation_longest_reception_hours)
        if not reserved_shortest_date.hour < setting.last_reservation_releasing_time and 0 == datetime.timedelta(
                hours=setting.reservation_shortest_reception_hours).days:
            reserved_shortest_date = reserved_shortest_date + datetime.timedelta(days=1)
        for date in date_range(reserved_shortest_date, reserved_longest_date):
            res[date.strftime('%Y-%m-%d')] = self.get_reservation_status_hours(date)
        return res


class ReserveAction:

    def __init__(self, shop_id, reserve_num):
        self.shop_id = shop_id
        self.reserve_num = reserve_num

    def reserving(self, reserved_datetime_str, request_user):
        setting = get_shop_reservation_setting(self.shop_id)
        reserved_datetime = datetime.datetime.strptime(reserved_datetime_str, '%Y-%m-%d %H:%M')
        if not reservation_check(reserved_datetime, self.shop_id) or not reservation_limit_check(reserved_datetime, setting, self.shop_id):
            print("予約不可")
            return
        reservation = Reserve.objects.create(reservation_date=reserved_datetime, shop_id=self.shop_id, reserve_num=self.reserve_num, reserver_account=request_user, reserver_id=reservation_id_generation(self.shop_id, reserved_datetime))
        return reservation
