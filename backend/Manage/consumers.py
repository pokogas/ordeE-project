import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.exceptions import ValidationError

from Manage.serializers import ShopMessageSerializer, OrderSerializers
from . import permission
from .models import ShopMessage, Shop, ShopManagement
from Customer.models import OrderConclusion
from .permission import Permission


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    # def disconnect(self, code):
    #     self.disconnect()

    def receive(self, text_data, bytes_data=None):
        context = {
            'message': 'testing consumer',
        }
        user = self.scope['user']
        if user_id := user.id:
            context.update({'user': str(user_id)})
        else:
            context.update({'user': None})
        self.send(text_data=json.dumps(context))


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.shop_id = self.scope['url_route']['kwargs']['shop_id']
        user = self.scope['user']
        await self.channel_layer.group_add(f'chat_{str(self.shop_id)}', self.channel_name)
        self.user_id = user.id
        if self.scope['user'] == "AnonymousUser":
            return self.close()
        if await self.access_authority_check():
            if await self.authorityChecker():
                return await self.accept()
        return await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f'chat_{str(self.shop_id)}', self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']
        message_category_id = text_data_json['category_id']
        if message_text == "/chat close":
            print("cmd")
        data = {
            'type': 'chat_message',
            'shop_id': str(self.shop_id),
            'message': message_text,
            'message_category_id': message_category_id,
            'user': self.user_id
        }
        message_db = await self._create_message(data)
        data_json = json.dumps(await self.serializer(message_db))
        data = {
            'type': 'chat_message',
            'data_json': data_json,
        }
        await self.channel_layer.group_send(f'chat_{str(self.shop_id)}', data)

    async def chat_message(self, data):
        await self.send(text_data=data["data_json"])

    @database_sync_to_async
    def _create_message(self, data):
        return ShopMessage.objects.create(shop_id=data['shop_id'],
                                          user_id=data['user'],
                                          message=data['message'],
                                          category_id=data['message_category_id'])

    @database_sync_to_async
    def serializer(self, message_db):
        serializer = ShopMessageSerializer(message_db)
        return serializer.data

    @database_sync_to_async
    def access_authority_check(self):
        try:
            ShopManagement.objects.filter(user_id=self.user_id, is_active=True).order_by("role")[0]
        except (Shop.DoesNotExist, ValidationError):
            return False
        except ShopManagement.DoesNotExist:
            return False
        return True

    @database_sync_to_async
    def authorityChecker(self):
        try:
            shop = Shop.objects.get(id=str(self.shop_id))
            executing_permission = "CHAT"
            shop_permission_code = shop.permission_code
            manage = ShopManagement.objects.filter(user_id=self.user_id, is_active=True).order_by("role")[0]
            if manage.role != 0:
                try:
                    shop = Shop.objects.get(id=str(self.shop_id))
                    manage = \
                        ShopManagement.objects.filter(user_id=self.user_id, is_active=True, shop=shop).order_by("role")[
                            0]
                except:
                    return False
        except:
            return False

        perm = Permission(executing_permission=executing_permission,
                          manage_role=manage.role,
                          shop_permission_code=shop_permission_code)

        return perm.isAvailable()


class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.shop_id = self.scope['url_route']['kwargs']['shop_id']
        user = self.scope['user']
        await self.channel_layer.group_add(f'order_{str(self.shop_id)}', self.channel_name)
        self.user_id = user.id
        if self.scope['user'] == "AnonymousUser":
            return self.close()
        if await self.access_authority_check():
            if await self.authorityChecker():
                return await self.accept()
        return await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(str(self.shop_id), self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        oc_id_or_order_id = text_data_json['oc_id_or_order_id']
        data = {
            'type': text_data_json['type'],
            'oc_id_or_order_id': oc_id_or_order_id,
        }
        await self.channel_layer.group_send(f'order_{str(self.shop_id)}', data)

    async def ORDER(self, data):
        trans_data = {
            'direction': "ORDER",
            'orders': data["orders"]
        }
        await self.send(text_data=json.dumps(trans_data))

    async def COOK_COMP(self, data):
        trans_data = {
            'direction': "COOK_COMP",
            'order_id': data["order_id"]
        }
        await self.send(text_data=json.dumps(trans_data))

    async def COMP(self, data):
        trans_data = {
            'direction': "COMP",
            'order_id': data["order_id"]
        }
        await self.send(text_data=json.dumps(trans_data))

    @database_sync_to_async
    def access_authority_check(self):
        try:
            ShopManagement.objects.get(user_id=self.user_id, is_active=True)
        except (Shop.DoesNotExist, ValidationError):
            return False
        except ShopManagement.DoesNotExist:
            return False
        return True

    @database_sync_to_async
    def authorityChecker(self):
        try:
            shop = Shop.objects.get(id=str(self.shop_id))
            executing_permission = "ORDER"
            shop_permission_code = shop.permission_code
            manage = ShopManagement.objects.filter(user_id=self.user_id, is_active=True).order_by("role")[0]
            if manage.role != 0:
                try:
                    shop = Shop.objects.get(id=str(self.shop_id))
                    manage = \
                        ShopManagement.objects.filter(user_id=self.user_id, is_active=True, shop=shop).order_by("role")[
                            0]
                except:
                    return False
        except:
            return False

        perm = Permission(executing_permission=executing_permission,
                          manage_role=manage.role,
                          shop_permission_code=shop_permission_code)

        return perm.isAvailable()


class ActionConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.shop_id = self.scope['url_route']['kwargs']['shop_id']
        user = self.scope['user']
        await self.channel_layer.group_add(f'order_{str(self.shop_id)}', self.channel_name)
        self.user_id = user.id
        if self.scope['user'] == "AnonymousUser":
            return self.close()
        if await self.access_authority_check():
            if await self.authorityChecker():
                return await self.accept()
        return await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(str(self.shop_id), self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        detail = text_data_json['detail']
        data = {
            'type': text_data_json['type'],
            'action': action,
            'detail': detail
        }
        await self.channel_layer.group_send(f'action_{str(self.shop_id)}', data)

    async def ORDER(self, data):
        trans_data = {
            'direction': "ORDER",
            'orders': data["orders"]
        }
        await self.send(text_data=json.dumps(trans_data))

    async def COOK_COMP(self, data):
        trans_data = {
            'direction': "COOK_COMP",
            'order_id': data["order_id"]
        }
        await self.send(text_data=json.dumps(trans_data))

    async def COMP(self, data):
        trans_data = {
            'direction': "COMP",
            'order_id': data["order_id"]
        }
        await self.send(text_data=json.dumps(trans_data))

    @database_sync_to_async
    def access_authority_check(self):
        try:
            ShopManagement.objects.get(user_id=self.user_id, is_active=True)
        except (Shop.DoesNotExist, ValidationError):
            return False
        except ShopManagement.DoesNotExist:
            return False
        return True

    @database_sync_to_async
    def authorityChecker(self):
        try:
            shop = Shop.objects.get(id=str(self.shop_id))
            executing_permission = "ACTION_WEBSOCKET"
            shop_permission_code = shop.permission_code
            manage = ShopManagement.objects.filter(user_id=self.user_id, is_active=True).order_by("role")[0]
            if manage.role != 0:
                try:
                    shop = Shop.objects.get(id=str(self.shop_id))
                    manage = \
                        ShopManagement.objects.filter(user_id=self.user_id, is_active=True, shop=shop).order_by("role")[
                            0]
                except:
                    return False
        except:
            return False

        perm = Permission(executing_permission=executing_permission,
                          manage_role=manage.role,
                          shop_permission_code=shop_permission_code)

        return perm.isAvailable()
