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
このブランチは下記のすべての段階が終わった後のものである。

この後には`基本３つの段階`と`１つのオプション`でハンズオンに取り組んでいただく。

~~基本段階~~
~~1. myproject/setting.pyの変更によるDjangoプロジェクトのセットアップ~~
~~2. アプリケーションへのログイン機能の追加~~
~~3. チャット機能の実装~~

~~オプション~~
~~1. チャット履歴の追加~~

それぞれの実装の完成形は`login`,`chat`,`v1`,`v2`のブランチに記載してある。


## まとめ
今回の勉強会を通してwebsocketを用いたリアルタイム通信、Djangoを用いたWeb開発などを身につけていただけたでしょうか？少しでも皆様のお力になれると幸いです。
