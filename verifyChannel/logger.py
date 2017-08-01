# coding:utf-8
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists('log'):
	os.mkdir('log')

fh = logging.FileHandler(r'.\log\runtime.log')
ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)

logger.addHandler(fh)  
logger.addHandler(ch)
