# kc3_chatapp

kc3 で チャットアプリを作成する勉強会 を行うためのものである。

### 【要件】
- ユーザー認証
- リアルタイムメッセージング
- 単一のメインチャットルーム
  
### 【使用技術】
- Django (Python)
	- channels
	- channels_redis
- Redis
- HTML/CSS/JavaScript


## はじめに
環境構築は`setup`ブランチに書いてある手順ですでに出来上がっているものとする。
> https://github.com/zono0013/kc3_chatapp/blob/setup/README.md

`myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ`
> https://github.com/zono0013/kc3_chatapp/blob/main/README.md

`アプリケーションへのログイン機能の追加`の２つも終了しているものとする。
> https://github.com/zono0013/kc3_chatapp/blob/login/README.md


この後には`基本３つの段階`と`１つのオプション`でハンズオンに取り組んでいただく。

基本段階
~~1. myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ~~
~~2. アプリケーションへのログイン機能の追加~~
3. チャット機能の実装

オプション
1. チャット履歴の追加

それぞれの実装の完成形は`project_setting`,`login`,`chat`,`option1`のブランチに記載してある。

**以降このREADMEでは`チャット機能の実装`の手順について記載する。**

## バックエンドの実装

### asgi.py
```python
import os

from django.core.asgi import get_asgi_application
import myapp.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    ),
})
```
役割: 

必要性: 

### routing.py
```python
from django.urls import re_path
from myapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
```
役割: 

必要性:

### consumers.py
```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

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
```
役割: 

必要性:

## クライアントの実装

### chat.htmlのJS

```HTML
<script>
        let chatSocket;
        const usernameElement = document.getElementById('username');
        const username = usernameElement.getAttribute('data-username');

        document.addEventListener('DOMContentLoaded', function() {
            joinRoom(); // ページがロードされた瞬間に接続する
        });

        function joinRoom() {
            const url = `ws://${window.location.host}/ws/chat/`;
            chatSocket = new WebSocket(url);
            initChatSocket();
        }

        function initChatSocket() {
            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                console.log('Data:', data);
                if (data.type === 'chat') {
                    console.log('Message:', data.message);
                    addMessage(data.message, data.user);
                }
            };

            document.getElementById('form').addEventListener('submit', function(e) {
                e.preventDefault();
                sendMessage();
            });
        }

        function addMessage(message, username) {
            const messagesDiv = document.getElementById(`message_div`);
            messagesDiv.insertAdjacentHTML('beforeend', `<p>${username}:${message}</p>`);
        }

        function sendMessage() {
            const form = document.getElementById('form');
            const formData = new FormData(form);
            const message = formData.get('message').trim();
            if(message){
                console.log(message);
                chatSocket.send(JSON.stringify({'message': message, 'user': username}));
                form.reset();
            }

        }
    </script>
```

役割: 
必要性: 

## 実装結果の確認
下記のコマンドでプロジェクトを立ち上げる
```bash
docker-compose up --build
```

`http://0.0.0.0:8000/`をタブ２個 開き、それぞれ別のアカウントでログインしよう。

<img width="742" alt="スクリーンショット 2024-09-07 4 34 36" src="https://github.com/user-attachments/assets/a707b22e-4c44-4e00-915a-1f68a3044f0d">

お互いに送受信可能なことが確認できる。

<img width="651" alt="スクリーンショット 2024-09-07 4 35 49" src="https://github.com/user-attachments/assets/d54c490f-32d1-4495-aff3-2f11741f5bfe">

<img width="659" alt="スクリーンショット 2024-09-07 4 36 10" src="https://github.com/user-attachments/assets/e4c41d0f-1396-4b0b-b978-477da1287c58">


ローカル同士の通信だが参加者同士で通信をしてもらうために`setting.py`の一部を書き換えてもらう。

これにより異なる参加者同士で通信できることを体感してもらうことができると思う。
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # 'hosts': [('redis', 6379)],
            'hosts': ["redis://:pee6b1e88ae2cdfe5ab74ea5e9878c7789b391feeed6c61f11f64022f40545444@ec2-107-21-32-196.compute-1.amazonaws.com:14289"], # 追加
        }
    }
}
```
