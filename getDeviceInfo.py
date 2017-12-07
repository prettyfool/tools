# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def getBrand():
    # 获取手机厂商名称
    cmd = "adb shell getprop ro.product.brand"
    std = os.popen(cmd)
    brand = std.readline().strip()
    return brand


def getModel():
    # 获取手机型号
    cmd = "adb shell getprop ro.product.model"
    std = os.popen(cmd)
    model = std.readline().strip()
    return model


def getOSVersion():
    # 获取系统版本号
    cmd = "adb shell getprop ro.build.version.release"
    std = os.popen(cmd)
    version = std.readline().strip()
    return version

def getDPI(type='str'):
    # 获取设备分辨率
    cmd = "adb shell dumpsys window displays"
    std = os.popen(cmd)
    pattern = re.compile('init=(\d+x\d+)')
    for line in std:
        d = re.search(pattern, line)
        if d:
            DPI = d.group(1)
            break
    if type == 'str':
        return DPI
    if type == 'tuple':
        return tuple(DPI.split('x'))
    if type == 'list':
        return DPI.split('x')
    if type == 'dict':
        dic = {}
        dic['width'], dic['high'] = DPI.split('x')
        return dic


def getDeviceId():
    # 获取设备序列号
    # 连接多个设备时，返回序列号列表
    cmd = "adb devices"
    std = os.popen(cmd)
    lines = std.readlines()
    if len(lines) < 2: return None
    ids = [line.split('\t')[0].strip() for line in lines if '\t' in line]
    if len(ids) < 2:
        return ids[0]
    else:
        return ids


def getANR():
    # 获取ANR 日志到脚本执行目录
    cmd = 'adb pull /data/anr/traces.txt .'
    os.popen(cmd)


if __name__ == "__main__":
    # print getInstalledAPP()
    # print getDPI(type='dict')
    # print getOSVersion()
    print getModel()
