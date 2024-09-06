# kc3_chatapp

kc3 で チャットアプリを作成する勉強会 を行うためのものである。

## Djangoのセットアップ
このブランチでは`Djangoのプロジェクトとアプリケーション`、`SQLite`の作成を行うためのものである。

### Djangoのプロジェクトの作成
下記のコマンドはカレントディレクトリに、`myproject`という名前のプロジェクトを作成するためのものである。

```
docker-compose run web django-admin startproject myproject .
```

### Djangoのアプリケーションの作成
下記のコマンドはカレントディレクトリに`myapp`というアプリケーションを作成するためのものである。

```
docker-compose run web python manage.py startapp myapp
```

### SQLiteの作成
Djangoにデフォルトで入っているアプリケーションを使うために、データベーステーブルを作成する必要がある。

```
docker-compose run --rm web python manage.py migrate
```

## 必要なファイルを追加する
1. rootディレクトリに`templates`ディレクトリを作成
2. 作成した`templates`ディレクトリに下記の３つのHTMLファイルを追加
  - login.html
  - signup.html
  - chat.html
3. myappディレクトリに下記２つのPythonファイルを追加
  - routing.py
  - consumers.py

## 結果
ここまでの確認として`tree`コマンドを使用すると下記の結果が得られる。

```bush
.
├── Dockerfile
├── README.md
├── db.sqlite3
├── docker-compose.yml
├── manage.py
├── myapp
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── admin.cpython-39.pyc
│   │   ├── apps.cpython-39.pyc
│   │   └── models.cpython-39.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-39.pyc
│   ├── models.py
│   ├── routing.py
│   ├── tests.py
│   └── views.py
├── myproject
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── asgi.cpython-39.pyc
│   │   ├── settings.cpython-39.pyc
│   │   ├── urls.cpython-39.pyc
│   │   └── wsgi.cpython-39.pyc
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── templates
    ├── chat.html
    ├── login.html
    └── signup.html

```


## 参考
プロジェクトとアプリケーションの違いやそれぞれのセットアップについて詳しくは下記のリンクを参照してほしい

https://docs.djangoproject.com/ja/5.1/intro/tutorial01/


