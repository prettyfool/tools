# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def get_installed_app_list():
    """
    : 获取已安装的第三方应用列表
    """
    cmd = "adb shell pm list packages -3"
    return [re.search('package:(\S+)', line).group(1) for line in os.popen(cmd) if line and line.startswith('package')]


def get_app_pid(package_name):
    """
    : 获取应用的 进程号 PID
    """
    cmd = 'adb shell ps | findstr %s' % package_name
    std = os.popen(cmd).readline()
    PID = std.split()[1]
    return PID


def get_app_uid(package_name):
    """
    : 获取应用的uid
    """
    cmd = 'adb shell dumpsys package %s | findstr userId' % package_name
    std = os.popen(cmd).readline()
    return std.split('=')[1]


def get_flow_from_pid(package_name, pid=None):
    """
    : 获取应用当前消耗的流量
    : return KB
    """
    if not pid:
        pid = get_app_pid(package_name)
    cmd = 'adb shell cat /proc/%s/net/dev | findstr wlan' % pid
    std = os.popen(cmd).readline()
    data = std.split(':')[1].split()
    rec, trans = int(data[0]), int(data[8])
    return float((rec + trans) / 1024)


def get_flow_from_uid(package_name, uid=None):
    """
    : 通过应用uid，获取应用当前消耗的流量
    : return (rcv,snd)
    """
    if uid is None:
        uid = get_app_uid(package_name)
    cmd = 'adb shell cat /proc/net/xt_qtaguid/stats | findstr %s' % uid
    std = os.popen(cmd)
    d_flow = []
    u_flow = []
    for line in std:
        if 'wlan' in line and '0x0' in line:
            data = line.split()
            d_flow.append(int(data[5]))
            u_flow.append(int(data[7]))
    return sum(d_flow) + sum(u_flow)


if __name__ == '__main__':
    from datetime import datetime

    start = datetime.now()
    print(get_installed_app_list())
    time = datetime.now() - start
    print(time)

    package_name = 'com.xp.tugele'
    print(get_app_pid(package_name))
    print(get_app_uid(package_name))
    print(get_flow_from_pid(package_name))
    print(get_flow_from_uid(package_name))
