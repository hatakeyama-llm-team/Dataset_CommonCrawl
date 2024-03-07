# ベースイメージの指定
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /app

# 依存ファイルのコピー
COPY ./requirements.txt /app
COPY ./extract_data/warc /app
COPY ./preprocess_data/mc4s /app

# Pythonライブラリのインストール
RUN pip install -r requirements.txt \
    && apt update \
    && apt install -y mecab libmecab-dev mecab-ipadic-utf8 build-essential cmake libboost-system-dev \
    libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev \
    && ln -s /etc/mecabrc /usr/local/etc/mecabrc \
    && pip install --no-cache-dir https://github.com/kpu/kenlm/archive/master.zip \
    && pip install --no-cache-dir sentencepiece "protobuf<3.20.*" \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# fasttextのモデルダウンロード
RUN mkdir -p /app/preprocess_data/mc4s/annotations/text_labels/ \
    && cd /app/preprocess_data/mc4s/annotations/text_labels/ \
    && wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.bin.gz \
    && gzip -d cc.ja.300.bin.gz \
    && rm -f cc.ja.300.bin.gz

# kenlmと関連ファイルのダウンロード
RUN mkdir -p /app/extract_data/warc/data/lm_sp \
    && wget -c -P /app/extract_data/warc/data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.arpa.bin \
    && wget -c -P /app/extract_data/warc/data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.sp.model

ENV PYTHONPATH /app
# jupyterのインストール
RUN pip install --no-cache-dir jupyter

# ポートの公開
EXPOSE 8701

# Jupyter Notebookの起動
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8701", "--no-browser", "--allow-root", "--NotebookApp.token=''"]