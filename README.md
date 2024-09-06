# kc3_chatapp

kc3 で チャットアプリを作成する勉強会 を行うためのものである。

# Djangoのセットアップ
このブランチでは`Djangoのプロジェクトとアプリケーション`、`SQLite`の作成を行うためのものである。

## Djangoのプロジェクトの作成
下記のコマンドはカレントディレクトリに、`myproject`という名前のプロジェクトを作成するためのものである。

```
docker-compose run web django-admin startproject myproject .
```

## Djangoのアプリケーションの作成
下記のコマンドはカレントディレクトリに`myapp`というアプリケーションを作成するためのものである。

```
docker-compose run web python manage.py startapp myapp
```

## SQLiteの作成
Djangoにデフォルトで入っているアプリケーションを使うために、データベーステーブルを作成する必要がある。

```
docker-compose run --rm web python manage.py migrate
```

# 参考
プロジェクトとアプリケーションの違いやそれぞれのセットアップについて詳しくは下記のリンクを参照してほしい

https://docs.djangoproject.com/ja/5.1/intro/tutorial01/


