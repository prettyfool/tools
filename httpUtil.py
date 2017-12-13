# coding=utf-8
__author__ = 'majunfeng'

from contextlib import closing
import os
from requests.api import get

CHUNK_SIZE = 1024  # 单次最大下载字节数


def download(url, **kwargs):
    """
    @func 下载文件到指定目录
    @url 下载链接
    @xlsx_file 文件名
    @outdir 下载目录，默认为当前目录下的download目录
    """
    outdir = kwargs.get('outdir')
    if not outdir:
        if not os.path.exists('download'):
            os.mkdir('download')
        outdir = os.path.join(os.curdir, 'download')
    filename = kwargs.get('xlsx_file', os.path.basename(url))
    with closing(get(url, filename, stream=True, verify=False)) as r:
        with open(os.path.join(outdir, filename), 'wb') as f:
            print('downloading %s' % filename)
            for chunk in r.iter_content(CHUNK_SIZE):
                f.write(chunk)
