# Python公式イメージを使用
FROM python:3.11-slim

# 作業ディレクトリを作成
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースをコピー
COPY . .

# ポート5000を開放
EXPOSE 5000

# アプリケーションを起動
CMD ["python", "app.py"]
