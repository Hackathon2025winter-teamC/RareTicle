FROM python:3.12

WORKDIR /app

# システム依存パッケージのインストール
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# プロジェクトファイルのコピー
COPY . .

# 静的ファイル用ディレクトリの作成
RUN mkdir -p /app/static
