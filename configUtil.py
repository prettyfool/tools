# coding=utf-8
__author__ = 'majunfeng'

from configparser import ConfigParser


def get_config(file_ini):
    """
    @ file_ini  file path of datasource
    @ return object of datasource
    """
    conf = ConfigParser()
    conf.read(file_ini)
    return conf
