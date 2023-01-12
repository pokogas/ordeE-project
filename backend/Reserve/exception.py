# バリデーションエラー
from rest_framework.exceptions import APIException


class ReservationError(APIException):
    status_code = 400
    default_detail = '予約が出来ませんでした.'
    default_code = 'reservation-error'
