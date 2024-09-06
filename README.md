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

この後には`基本３つの段階`と`１つのオプション`でハンズオンに取り組んでいただく。

基本段階
1. myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ
2. アプリケーションへのログイン機能の追加
3. チャット機能の実装

オプション
1. チャット履歴の追加

それぞれの実装の完成形は`project_setting`,`login`,`chat`,`option1`のブランチに記載してある。

**以降このREADMEでは`myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ`の手順について記載する。**

## myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ

### ALLOWED_HOSTS の追加
```python
ALLOWED_HOSTS = [
    "localhost",  # 追加
    "0.0.0.0",  # 追加
]
```
役割: 開発サーバーがリクエストを受け付けるホストを指定します。

必要性: ローカル開発環境でDjangoアプリケーションを実行するために必要です。セキュリティ上の理由から、Djangoは許可されたホストからのリクエストのみを受け付けます。

### INSTALLED_APPS への追加
```python
INSTALLED_APPS = [
    ...
    'myapp',  # 追加
    'channels',  # 追加
]
```
役割: プロジェクトで使用するDjangoアプリケーションとライブラリを指定します。

必要性:
  - 'myapp': 開発するチャットアプリケーションを Django プロジェクトに統合します。
  - 'channels': WebSocket を使用したリアルタイム通信を可能にするDjango Channels を有効にします。

### テンプレートディレクトリの設定
```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR/'templates'],  # 追加
        ...
    },
]
```
役割: プロジェクト全体で使用するテンプレートファイル(HTMLファイル)の場所を指定します。
必要性: アプリケーション外の共通テンプレートを使用可能にします。

### ASGI_APPLICATIONの設定
```python
ASGI_APPLICATION = 'myproject.asgi.application'
```
役割: ASGIサーバーがDjangoアプリケーションを実行するためのエントリーポイントを指定します。
必要性: 通常のHTTP通信に加え、Django Channelsを使用したWebSocket通信を可能にします。

### CHANNEL_LAYERSの設定
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    },
}
```
役割: Django ChannelsのバックエンドとしてRedisを使用するように設定します。
必要性: 複数のWebSocket接続間でメッセージを効率的に配信するために必要です。Redisは高速で信頼性の高いメッセージングシステムを提供します。

>Redisについて詳しくは以下を参照  
[http://redis.shibu.jp](http://redis.shibu.jp)

## 実装結果の確認
下記のコマンドでプロジェクトを立ち上げる
```bash
docker-compose up --build
```

`http://0.0.0.0:8000/`を開いて下記のような状態が見られると成功である。

<img width="1470" alt="スクリーンショット 2024-09-07 2 49 43" src="https://github.com/user-attachments/assets/5bb9f5d1-483b-42c5-98a6-892506e3817d">



