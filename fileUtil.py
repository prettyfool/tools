# -*- coding:utf-8 -*-
import os
import hashlib

BLOCK_SIZE = 1024 * 8  # 单次最大读取文件字节大小


def getFileMd5(file_path):
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


if __name__ == "__main__":
    filepath = r'E:\package\PKG_tugele\SGTugele_v4.0.0_Build_918_20171117_test_tugele_debug.apk'
    md5 = getFileMd5(filepath)
    print(md5)
