#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import hashlib
import tempfile
import time

import requests


def calculate_md5(file_path, block_size=2**20):
    """
    计算文件的MD5值，适用GB以上的大文件
    :param file_path: 文件路径
    :param block_size: 每次读取文件的块大小。默认的块大小为1MB（2**20字节），这是一个合理的大小，可以在大多数情况下提供良好的性能。
    :return:
    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()


if __name__ == '__main__':
    file_path = '/Users/prettyfool/work/KA/OPPO/厂商同步/OTA/OPD2201_11_C_OTA_1010_all_oypX2K_10010111.zip'
    st = time.time()
    md5_value = calculate_md5(file_path)
    print(f'MD5 value of {file_path}: {md5_value}')
    print(f'时间结果：{time.time() - st}')



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
