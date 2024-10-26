from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import json

from core.models.user_model import User
from core.services.chat_service import ChatService
from core.services.group_service import GroupService
from core.services.user_services import UserService

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"private_{self.user_id}_{self.scope['user'].id}"

        if self.scope['user'] == AnonymousUser():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        sender = self.scope['user']
        if not isinstance(sender, User):
            sender = await database_sync_to_async(UserService.retrieve_user)(sender.id)

        receiver = await database_sync_to_async(UserService.retrieve_user)(self.user_id)

        await database_sync_to_async(ChatService.send_private_chat_message)(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'private_chat_message',
                'message': message,
                'sender': str(sender.id)
            }
        )

    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_name = f"group_{self.group_id}"

        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = str(self.scope['user'].id)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def group_chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
