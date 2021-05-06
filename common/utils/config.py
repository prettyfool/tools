# coding=utf-8
__author__ = 'majunfeng'


'''
this module is used to implement a method which can read config file, 
likes ini,yaml,xml, 
finally, these will transfer to a dict or list.
'''

from configparser import ConfigParser
import yaml

def get_config(file_ini):
    """
    @ file_ini  file path of datasource
    @ return object of datasource
    """
    c = ConfigParser()
    c.read(file_ini)
    to_dict = {section: {option: c.get(section, option) for option in c.options(section)} for section in c.sections()}
    return to_dict


def load_yaml(file_yaml):
    with open(file_yaml,encoding='utf-8') as fp:
        y = yaml.load(fp)
    return y
