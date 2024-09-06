import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message  # 追加


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'main'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # メッセージをデータベースに保存
        await self.save_message(user, self.room_name, message)  # 追加

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def save_message(self, user, room, message):
        Message.objects.create(user=user, room=room, content=message)