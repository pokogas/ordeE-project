
from django.contrib import admin
from .models import CartItem, Customer, Order, OrderConclusion

admin.site.register(CartItem)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderConclusion)