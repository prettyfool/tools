# coding:utf-8
import logging


def logger(logger=None, name='', **kwargs):
    '''
    usage:
        logger : logging.getLogger object
        name   : logging.getLogger(name)
        **kwargs ：
            logfile : logfile path
                default: won't add a file to disk
            formatter : log formatter
                default: %(asctime)s - %(levelname)s - %(message)s
    '''
    if not logger:
        logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if 'formatter' in kwargs:
        formatter = logging.Formatter(kwargs.get('formatter'))
    else:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    if 'logfile' in kwargs:
        fh = logging.FileHandler(kwargs.get('logfile'))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    log = logger(logfile='test.log')
    log.info('info')
    log.warn('warn')
    log.debug('debug')
    log.error('error')
