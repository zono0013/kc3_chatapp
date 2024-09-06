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
class ChatView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        return render(request, "chat.html", {"user": user})


chat = ChatView.as_view()


# ログイン画面のビュー
class Login(View):

    # ログイン画面を表示
    def get(self, request):
        return render(request, "login.html")

    # ログイン機能
    def post(self, request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # ユーザー認証
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # ログイン成功
                login(request, user)
                return redirect('chat')
            else:
                # ログイン失敗
                messages.error(request, 'ユーザー名またはパスワードが間違っています。')

        return render(request,"login.html")


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
