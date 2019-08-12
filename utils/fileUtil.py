# -*- coding:utf-8 -*-
import os
import hashlib
import tempfile

import requests

BLOCK_SIZE = 1024 * 8  # 单次最大读取文件字节大小


def get_file_md5(file_path):
    """
    @desc      获取文件的md5值
    @file_path 文件的路径
    @return    文件的md5值
    """
    if not os.path.exists(file_path):
        return None
    mHash = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            block = f.read(1024 * 8)
            if not block:
                break
            mHash.update(block)
    return mHash.hexdigest()


def download_file(url, filename=None, outdir=None):
    """
    下载文件
    :param url: 下载文件的url
    :param filename: 下载文件名，默认不传参，生成系统临时文件名
    :return: 下载文件的完整路径
    """
    if filename and os.path.exists(filename):
        return filename
    if filename is None:
        if outdir:
            filename = os.path.join(outdir, os.path.basename(url))
        else:
            f = tempfile.NamedTemporaryFile(delete=False).name
            filename = f + os.path.splitext(url)[1]
    try:
        r = requests.get(url, stream=True, verify=False)
    except requests.exceptions.HTTPError as e:
        raise ('%s is Error\n%s' % (url, e))
    else:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(16 * 1024):
                f.write(chunk)
    return filename

if __name__ == "__main__":
    file_path = r'E:\package\PKG_tugele\SGTugele_v4.4.0_Build_1141_20180607_test_tugele_debug.apk'
    md5 = get_file_md5(file_path)
    print(md5)
