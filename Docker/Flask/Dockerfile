# Pythonのイメージを指定
FROM python:3.11.3-buster
# PYTHONDONTWRITEBYTECODEとPYTHONUNBUFFEREDはオプション
# pycファイル(および__pycache__)の生成を行わないようにする
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
# コンテナのワークディレクトリを/codeに指定
WORKDIR /code
# ローカルのrequirements.txtをコンテナの/codeフォルダ直下に置く
COPY ./requirements.txt /code/
# コンテナ内でpip install -r requirements.txtを実行
RUN pip install -U pip && \
    pip install -r requirements.txt
# ソースコードをコンテナにコピー
COPY . /code/
# Flaskのアプリケーションを実行
<<<<<<< HEAD
CMD ["python", "app.py"]
=======
# CMD ["python", "app.py"]
CMD ["flask", "--app", "app", "run", "--debug", "--host=0.0.0.0"]
>>>>>>> d85865382315593572c5318d1d80281a13efdc93
