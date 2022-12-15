from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('reservation/get_reservation_shops', views.get_reservation_shops, name='get_reservation_shop'),
    path('reservation/reservation_create', views.reservation_create, name='reservation_create'),
    path('reservation/get_shop_reservation_datetime', views.get_shop_reservation_datetime, name='get_shop_reservation_datetime'),
    path('reservation/reserving', views.reserving,name='reserving'),

]
