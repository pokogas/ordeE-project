from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.response import Response
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

# rest_framework_simplejwtのTokenViewBaseをオーバーライド。
class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            ShopManagement.objects.filter(user__email=request.data["email"], is_active=True)
        except (ShopManagement.DoesNotExist, IndexError):
            raise NotAccessPermission
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# ManageJwtCreate
class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer


"""
# ManageJwtRefresh
class TokenRefreshView(TokenViewBase):

    Takes a sliding JSON web token and returns a new, refreshed version if the
    token's refresh period has not expired.
    serializer_class = TokenRefreshSerializer
"""
