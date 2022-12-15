from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('detail/', views.detail, name='detail'),
    path('order/data', views.order_data, name='order-data'),
    path('order/action', views.order_action, name='order_action'),
    path('cart/data', views.cart_data, name='cart'),
    path('cart/action', views.cart_action, name='cart-action'),
    path('menu', views.menu_data, name='menu'),
    path('menu/detail', views.menu_detail_data, name='menu-detail'),
    path('menu/category', views.category_data, name='menu-category_data'),
]
