# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def getInstalledAPP():
    # 获取已安装的第三方应用列表
    cmd = "adb shell pm list packages -3"
    return [re.search('package:(\S+)', line).group(1) for line in os.popen(cmd) if line and line.startswith('package')]


def getPID(packagename):
    '''
    # 获取应用的 进程号 PID
    '''
    cmd = 'adb shell ps | findstr %s' % packagename
    std = os.popen(cmd).readline()
    PID = std.split()[1]
    return PID


def getUserId(packagename):
    '''
    # 获取应用的uid
    '''
    cmd = 'adb shell dumpsys package %s | findstr userId' % packagename
    std = os.popen(cmd).readline()
    return std.split('=')[1]


def getFlow(packagename):
    '''
    # 获取应用当前消耗的流量
    # return KB
    '''
    PID = getPID(packagename)
    cmd = 'adb shell cat /proc/%s/net/dev | findstr wlan' % PID
    std = os.popen(cmd).readline()
    data = std.split(':')[1].split()
    rec, trans = int(data[0]), int(data[8])
    return float((rec + trans) / 1024)


if __name__ == '__main__':
    # from datetime import datetime
    #
    # start = datetime.now()
    # print getInstalledAPP()
    # time = datetime.now() - start
    # print time

    packagename = 'com.xp.tugele'
    # print _getPID(packagename)
    print getFlow(packagename)
