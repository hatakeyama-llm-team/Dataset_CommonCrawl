import glob

from botocore.exceptions import NoCredentialsError
from .file_utils import make_dir, download_file, decompress_gz
import os
from .s3_utils import download_file_with_progress

base_url = "https://data.commoncrawl.org/"
make_dir("data/gz")
make_dir("data/warc")


def get_cc_path_list(path_dir="data/path_list/*"):
    path_list = []
    for file_path in glob.glob(path_dir):
        print(file_path)
        with open(file_path, "r") as f:
            temp_path_list = f.readlines()

        temp_path_list = [path.strip() for path in temp_path_list]

        path_list += temp_path_list

    return path_list


def cc_path_to_urls(cc_path):
    url = base_url+cc_path
    filename = cc_path.replace("/", "_")
    gz_path = f"data/gz/{filename}"
    warc_path = f"data/warc/{filename}".replace(".gz", "")

    return url, gz_path, warc_path


def download_warc_file(path):
    '''cloudfrontからHTTP経由でダウンロードする'''
    url, gz_path, warc_path = cc_path_to_urls(path)

    if os.path.exists(warc_path):
        print(f"warc_pathにはファイルが存在しています")
        return warc_path
    try:
        if os.path.exists(gz_path):
            print(f"gz_pathがすでに存在します: {gz_path}")
        else:
            print("downloading "+url)
            download_file(url, gz_path)
        print("decompressing "+gz_path)
        decompress_gz(gz_path, warc_path,
                      remove_gz=False, fill_blank_gz=True)
        return warc_path
    except Exception as e:
        print(e)
        print("fail loading "+url)
        return warc_path


def download_warc_file_with_s3(path:str):
    '''前提条件：AWSの認証情報が設定されている必要がある'''
    '''s3からboto3を使用してダウンロードする'''

    url, gz_path, warc_path = cc_path_to_urls(path)

    if os.path.exists(warc_path):
        print(f"warc_pathにはファイルが存在しています")
        return warc_path
    try:
        CC_BUCKET_NAME = "commoncrawl"
        print(f'download from s3://{CC_BUCKET_NAME}/{path} to {warc_path}')
        # s3からダウンロードする設定
        download_file_with_progress(CC_BUCKET_NAME, path, warc_path)

        decompress_gz(gz_path, warc_path,
                      remove_gz=False, fill_blank_gz=True)
        return warc_path
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(e)
        print("fail loading " + url)
        return warc_path

