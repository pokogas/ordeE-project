from django.contrib import admin
from .models import Shop, Category, Menu, Room, ShopManagement, ShopMessage, MessageCategory, MessageActionItem, ShopMessageAction, Waiting

admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Room)
admin.site.register(ShopManagement)
admin.site.register(ShopMessage)
admin.site.register(MessageCategory)
admin.site.register(MessageActionItem)
admin.site.register(ShopMessageAction)
admin.site.register(Waiting)