from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddleware
from . import consumers

websocket_urlpatterns = [
    path('test', consumers.TestConsumer.as_asgi()),
    path('manage/chat/<uuid:shop_id>', consumers.ChatConsumer.as_asgi()),
    path('manage/order/<uuid:shop_id>', consumers.OrderConsumer.as_asgi()),
    path('manage/action/<uuid:shop_id>', consumers.ActionConsumer.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

