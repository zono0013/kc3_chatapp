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

さらに`myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ`も終了していることを前提とする。
> https://github.com/zono0013/kc3_chatapp/blob/main/README.md

この後には`基本３つの段階`と`１つのオプション`でハンズオンに取り組んでいただく。

基本段階
~~1. myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ~~
2. アプリケーションへのログイン機能の追加
3. チャット機能の実装

オプション
1. チャット履歴の追加

それぞれの実装の完成形は`project_setting`,`login`,`chat`,`option1`のブランチに記載してある。

**以降このREADMEでは`アプリケーションへのログイン機能の追加`の手順について記載する。**

## バックエンドの実装

### urls.py
```python
from django.contrib import admin
from django.urls import path

from myapp.views import chat, login_chat, signup_chat

urlpatterns = [
    path('admin/', admin.site.urls),
    # 他のURLパターンの追加
    path('signup/', signup_chat, name="signup"),
]
```

> 解答例：[https://github.com/zono0013/kc3_chatapp/blob/chat/myproject/urls.py
](https://github.com/zono0013/kc3_chatapp/blob/chat/myproject/urls.py)

### views.py
```python
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.

# チャット画面を表示するビュー
# loginをしていないと弾く処理、ユーザーの名前を返す処理、chat.htmlの表示の３つの機能をつける。
class ChatView(View):
    

chat = ChatView.as_view()


# ログイン画面のビュー
class Login(View):

    # ログイン画面を表示
    
    # ログイン機能
    

            # ユーザー認証
            

            
                # ログイン成功
                
                # ログイン失敗
               

        

login_chat = Login.as_view()


# ユーザー作成画面のビュー
class SignupView(View):

    # ユーザー作成画面の表示
    def get(self, request):
        return render(request, "signup.html")

    # ユーザー作成とログイン機能
    def post(self, request):
        if request.method == 'POST':
            new_username = request.POST.get('new_username')
            new_password = request.POST.get('new_password')
            try:
                # 新しいユーザーオブジェクトを作成し、ユーザー名とパスワードを設定
                user = User.objects.create_user(username=new_username, password=new_password)
            except Exception as e:
                # ユーザ作成失敗
                messages.error(request, 'ユーザーの作成に失敗しました。エラー: {}'.format(str(e)))

            # ログイン処理
            user = authenticate(request, username=new_username, password=new_password)
            if user is not None:
                # ログイン成功
                messages.error(request, 'ログインに成功しました。')
                login(request, user)
                return redirect('chat')
            else:
                # ログイン失敗
                messages.error(request, 'ユーザー名またはパスワードが間違っています。')
        return render(request, "signup.html")


signup_chat = SignupView.as_view()
```

> 解答例：[https://github.com/zono0013/kc3_chatapp/blob/chat/myapp/views.py
](https://github.com/zono0013/kc3_chatapp/blob/chat/myapp/views.py)

## クライアントの実装

### login.html

```HTML
<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>

<body>
<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <label for="username">ユーザー名:</label>
    <input type="text" id="username" name="username" required>
    <br>
    <label for="userpassword">パスワード:</label>
    <input type="password" id="userpassword" name="password" required>
    <br>
    <button type="submit">ログイン</button>
</form>
<a href="{% url 'signup' %}">新規アカウント作成</a>
</body>

</html>
```


### signup.html

```HTML
<!-- login.htmlを元に考えてみよう -->
```

> 解答例：[https://github.com/zono0013/kc3_chatapp/blob/chat/templates/login.html](https://github.com/zono0013/kc3_chatapp/blob/chat/templates/login.html)

### chat.html

```HTML
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Chat Room</title>
</head>

<body>
<h1>Let's chat!</h1>

<h2 id="username" data-username="{{ request.user.username }}">ユーザー: {{ request.user.username }}</h2>

<form id="form" class="message-form">
    <input type="text" name="message" placeholder="Enter message">
</form>

<div id="message_div"></div>

</body>
</html>
```


## 実装結果の確認
下記のコマンドでプロジェクトを立ち上げる
```bash
docker-compose up --build
```

`http://0.0.0.0:8000/`を開くと下記の様なログイン画面が表示される。何もアカウントを作ってない時にログインしてもリロードされるだけになる。

<img width="494" alt="スクリーンショット 2024-09-07 3 55 25" src="https://github.com/user-attachments/assets/ad24d23a-1cfe-4302-9d69-d0ba49f42531">

`新規アカウント作成`ボタンをクリックすると`url`が`http://0.0.0.0:8000/signup/`に変化し、サインアップ用の画面に変わったことがわかる。実際にアカウントを作成してみよう！！

<img width="451" alt="スクリーンショット 2024-09-07 4 00 12" src="https://github.com/user-attachments/assets/c9d45949-ee5e-4713-b312-11cedb24bf0b">

ログインボタンをクリックすると`url`が`http://0.0.0.0:8000/chat/`に変化し、チャット用の画面に変わったことがわかる。ここまで出来たらOK！！

<img width="434" alt="スクリーンショット 2024-09-07 4 01 20" src="https://github.com/user-attachments/assets/3da4f6a4-d662-4db5-abdd-3d2cfeb32f69">
