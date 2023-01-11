from django.urls import path
from rest_framework.exceptions import ValidationError

from . import views, authentication


app_name = 'manage'

urlpatterns = [
    path('auth/jwt/create/', authentication.TokenObtainPairView.as_view(), name="logout"),
    path('test/', views.test, name='test'),
    path('manage_user_me/', views.manage_user_me, name='manage_user_me'),
    path('access_home/', views.access_home, name='access_home'),
    path('order/get_order/', views.get_order, name='get_order'),
    path('order/get_orders/', views.get_orders, name='get_orders'),
    path('order/order_action/', views.order_action, name='order_action'),
    path('floor/get_rooms/', views.get_rooms, name='get_rooms'),
    path('access_order_history/', views.access_order_history, name='access_order_history'),
    path('access_menu/', views.access_menu, name='access_menu'),
    path('access_room/', views.access_room, name='access_room'),
    path('access_shop_info/', views.access_shop_info, name='access_shop_info'),
    path('to_day_messages/', views.to_day_messages, name='to_day_messages'),
    path('messages_custom_category/', views.messages_custom_category, name='messages_custom_category'),
    path('shops/', views.shops, name='user_manage_shops'),
]