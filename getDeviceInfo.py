# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def init():
    """
    : 启动adb
    : return 启动成功返回True
    """
    cmd = 'adb start-server'
    std = os.popen(cmd)
    if std:
        return True


def get_brand():
    """
    : 获取手机厂商名称
    """
    cmd = "adb shell getprop ro.product.brand"
    std = os.popen(cmd)
    brand = std.readline().strip()
    return brand


def get_model():
    """
    : 获取手机型号
    """
    cmd = "adb shell getprop ro.product.model"
    std = os.popen(cmd)
    model = std.readline().strip()
    return model


def get_os_version():
    """
    :获取系统版本号
    """
    cmd = "adb shell getprop ro.build.version.release"
    std = os.popen(cmd)
    version = std.readline().strip()
    return version


def get_dpi():
    """
    : 获取设备分辨率
    """
    cmd = 'adb shell wm size'
    std = os.popen(cmd)
    for line in std:
        d = re.search('(\d+.\d+)', line.strip())
        if d:
            return d.group(1)


def get_device_id():
    """
    : 获取设备序列号
    : return 连接多个设备时，返回序列号列表
    """
    cmd = "adb shell getprop ro.serialno"
    std = os.popen(cmd)
    serialno = std.readline().strip()
    return serialno


def get_anr():
    """
    : 获取ANR 日志到脚本执行目录
    """
    cmd = 'adb pull /datasource/anr/traces.txt .'
    os.popen(cmd)


if __name__ == "__main__":
    init()
    print(get_brand())
    print(get_model())
    print(get_os_version())
    print(get_dpi())
    print(get_device_id())
