from rest_framework.exceptions import ValidationError, APIException
from .models import Shop

from .models import ShopManagement


class ShopNotFound(APIException):
    status_code = 404
    default_detail = 'shopNotFound'
    default_code = 'shopNotFound'


class NotAccessPermission(APIException):
    status_code = 403
    default_detail = 'NotAccessPermission'
    default_code = 'NotAccessPermission'


class UseAuthorityInAccessProhibited(APIException):
    status_code = 403
    default_detail = 'UseAuthorityInAccessProhibited'
    default_code = 'UseAuthorityInAccessProhibited'


class ShopNotAccessPermission(APIException):
    status_code = 403
    default_detail = 'ShopNotAccessPermission'
    default_code = 'ShopNotAccessPermission'


PERMISSIONS = [
    "ACCESS_HOME",
    "ORDER",
    "ACTION_WEBSOCKET",
    "ACCESS_ORDER_REALTIME",
    "ACCESS_ORDER_HISTORY",
    "ACCESS_MENU",
    "ACCESS_ROOM",
    "ACCESS_SHOP_INFO",
    "CHAT"
]


# TODO PERMISSIONSの追加時にコード不足でエラーになった場合 DEFAULTから引っ張ってこれる処理を作ること
class Permission:

    def __init__(self, executing_permission, manage_role, shop_permission_code):
        self.exp = executing_permission
        self.role = manage_role
        self.spc = shop_permission_code

    def isAvailable(self):
        permission_cord = str(self.spc)
        list_permission_cord = list(permission_cord)
        list_num = [int(s) for s in list_permission_cord]
        if self.role == 0:
            return True
        elif self.role == 1:
            return True
        elif self.role == 2 and list_num[PERMISSIONS.index(self.exp)] >= 2:
            return True
        elif self.role == 3 and list_num[PERMISSIONS.index(self.exp)] == 3:
            return True
        return False

    # 権限チェッカー
    # 使い方 authorityChecker(アクセスユーザーのパーミッション, 使用するパーミッション, パーミッションコード)
    # をすることで権限の有無の確認が出来ます。
    def authorityChecker(self):
        if not self.isAvailable():
            raise UseAuthorityInAccessProhibited
        return None


# 管理者ページアクセスチェック
# ここでuserIDの有効性/ステータス/バリデーションをチェックします
# 使い方@api_view(["GET"])の下に@access_authority_check("使用するパーミッション")を設置してください
def access_authority_check(executing_permission):
    def wrapper(func):
        def checker(request, *args, **kwargs):
            try:
                manage = ShopManagement.objects.filter(user=request.user, is_active=True).order_by("role")[0]
                if executing_permission == "DEFAULT":
                    return func(request, *args, **kwargs)
                if manage.role != 0:
                    try:
                        shop = Shop.objects.get(id=request.query_params.get("shop_id"))
                        manage = ShopManagement.objects.filter(user=request.user,
                                                               is_active=True,
                                                               shop=shop).order_by("role")[0]
                        permission = Permission(executing_permission=executing_permission,
                                                manage_role=manage.role,
                                                shop_permission_code=shop.permission_code)
                        permission.authorityChecker()
                    except (Shop.DoesNotExist, ValidationError):
                        raise ShopNotFound
                    except (ShopManagement.DoesNotExist, IndexError):
                        raise ShopNotAccessPermission
                if manage.role == 0:
                    try:
                        Shop.objects.get(id=request.query_params.get("shop_id"))
                    except (Shop.DoesNotExist, ValidationError):
                        raise ShopNotFound
            except (ShopManagement.DoesNotExist, IndexError):
                raise NotAccessPermission

            return func(request, *args, **kwargs)

        return checker

    return wrapper
