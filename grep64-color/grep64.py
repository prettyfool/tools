# coding:utf-8

import requests
import os
from contextlib import closing
import shutil
import re
import logging
import sys

def _log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if not os.path.exists(r'log'):
        os.mkdir('log')
    fh = logging.FileHandler(r'.\log\runtime.log')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = _log()

def download(url, filename, outdir='./'):
    """
    @func 下载文件到指定目录
    @url 下载链接
    @filename 文件名
    @outdir 下载目录，默认为当前目录
    """
    if not os.path.exists(outdir):
        return
    with closing(requests.get(url, filename, stream=True, verify=False)) as r:
        with open(os.path.join(outdir, filename), 'wb') as f:
            logger.info('%s download [%s]'%(filename,url))
            for chunk in r.iter_content(1024):
                f.write(chunk)


def gt64(filepath):
    cmd = r"gifsicle.exe --cinfo %s" % filepath
    logger.info(cmd)
    std = os.popen(cmd)
    lines = std.readlines()
    for line in lines:
        if 'global' in line:
            color = int(line.strip().split()[-1][1:-1])
            logger.info('%s color is %s'%(filepath, str(color)))
            break
    if color > 64:
        return True
    else:
        return False


if __name__ == '__main__':
    if len(sys.argv)<2:
        logger.warn('you need input filename')
    else:
        filepath = sys.argv[1]
    pics = 'pics'
    if not os.path.exists(pics):
        pics = os.mkdir('pics')
    with open(filepath, 'r') as f:
        for line in f:
            url, filename = line.strip(), os.path.basename(line.strip())
            download(url, filename)
            pic_temp = os.path.join(os.curdir, filename)
            if os.path.exists(pic_temp):
                if gt64(pic_temp):
                    try:
                        logger.info('%s moving to %s'%(filename,'pics'))
                        shutil.move(pic_temp, '.\pics')
                    except shutil.Error as msg:
                        logger.error(msg)
                        os.remove(pic_temp)
                else:
                    logger.info('%s removing'%filename)
                    os.remove(pic_temp)
