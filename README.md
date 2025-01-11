<p style="display: inline">
<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge&logoColor=white">
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">
<!-- ミドルウェア一覧 -->
<img src="https://img.shields.io/badge/-MySQL-4479A1.svg?logo=mysql&style=for-the-badge&logoColor=white">
<!-- インフラ一覧 -->
<img src="https://img.shields.io/badge/-Docker-1488C6.svg?logo=docker&style=for-the-badge">
<img src="https://img.shields.io/badge/-aws-232F3E.svg?logo=amazon-aws&style=for-the-badge">
</p>

## 前提

- バージョン

下記バージョンで環境構築をおこなった

```bash
# docker --version
Docker version 20.10.13, build a224086

# docker compose version
Docker Compose version v2.3.3
```

## 環境構築手順

初回のみ(config ファイル生成)実行
※すでに config ファイルが生成されているため実行不要

```bash
docker-compose run web django-admin startproject config .
```

### 準備

1. 「.env.local」を「.env」にリネームする

2. ビルド

```bash
docker-compose build
# キャッシュを使わずにビルドする場合は下記を実行
docker-compose build --no-cache
```

3. データベースのマイグレーション:

```bash
docker-compose exec web python manage.py migrate
```

4. コンテナの起動

```bash
docker-compose up
```

5. ブラウザで確認

http://localhost:8080/ を開く

## その他

エラーが起きたらログを確認して調査する

```bash
# フロントのログ
docker-compose logs web
# DBのログ
docker-compose logs db
```

## 参考

[全プロジェクトで重宝されるイケてる README を作成しよう！](https://qiita.com/shun198/items/c983c713452c041ef787)
