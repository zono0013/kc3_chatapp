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

さらに基本段階の３つはすでに終了しているものとする
`myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ`
> https://github.com/zono0013/kc3_chatapp/blob/main/README.md

`アプリケーションへのログイン機能の追加`
> https://github.com/zono0013/kc3_chatapp/blob/login/README.md

`チャット機能の実装`
> https://github.com/zono0013/kc3_chatapp/blob/chat/README.md

この後には`基本３つの段階`と`１つのオプション`でハンズオンに取り組んでいただく。

~~基本段階~~
~~1. myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ~~
~~2. アプリケーションへのログイン機能の追加~~
~~3. チャット機能の実装~~

オプション
1. チャット履歴の追加

それぞれの実装の完成形は`project_setting`,`login`,`chat`,`option1`のブランチに記載してある。

**以降このREADMEでは`チャット履歴の追加`の手順について記載する。**

## バックエンド実装

### models.py
```python
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
```
役割:

必要性:

### マイグレーション
Modelsで宣言したもののテーブルを作成し使い得る状態にするためには下記２つの動作が必要である。

```bash
docker-compose run web python manage.py makemigrations
```

```bash
 docker-compose run web python manage.py migrate 
```

### views.py
```python
from .models import Message  # 追加

class ChatView(View):
    @method_decorator(login_required)
    def get(self, request, room_name='main'):  # 追加
        user = request.user
        messages = Message.objects.filter(room=room_name)  # 追加
        return render(request, "chat.html", {
            "user": user,
            "room_name": room_name,  # 追加
            "messages": messages  # 追加
        })
```
役割: 

必要性:

### consumers.py
```python
from .models import Message  # 追加


class ChatConsumer(AsyncWebsocketConsumer):
#一部省略

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

#一部省略


    @database_sync_to_async  # 追加
    def save_message(self, user, room, message):  # 追加
        Message.objects.create(user=user, room=room, content=message)  # 追加
```
役割: 

必要性: 

## クライアント実装
### chat.html
```HTML
    <!-- チャットの履歴表示 -->
    <div id="chat-log">
        {% for message in messages %}
            <p>{{ message.user.username }}:{{ message.content }}</p>
        {% endfor %}
    </div>
```
役割: 
必要性: 


## 実装結果の確認

下記のコマンドでプロジェクトを立ち上げる
```bash
docker-compose up --build
```

`http://0.0.0.0:8000/`を開いてログインし、メッセージを送信。画面をリロードしても送ったメッセージを見ることができると完成！！




