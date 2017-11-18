# coding:utf-8
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists('log'):
    os.mkdir('log')

_fh = logging.FileHandler(r'.\log\runtime.log')
_ch = logging.StreamHandler()

_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
_fh.setFormatter(_formatter)
_ch.setFormatter(_formatter)

logger.addHandler(_fh)
logger.addHandler(_ch)
