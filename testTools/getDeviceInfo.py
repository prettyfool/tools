# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def getDPI():
    '''
    获取设备分辨率
    '''
    cmd = "adb shell dumpsys window displays"
    std = os.popen(cmd)
    pattern = re.compile('init=(\d+x\d+)')
    for line in std:
        d = re.search(pattern, line)
        if d:
            DPI = d.group(1)
            break
    return DPI


def getInstalledAPP():
    '''
    获取已安装的第三方应用列表
    '''
    installed = []
    cmd = "adb shell pm list packages -3"
    std = os.popen(cmd)
    for line in std:
        if line:
            package = re.search('package:([\.a-zA-Z0-9]+)', line).group(1)
            installed.append(package)
    return installed


def getDeviceId():
    cmd = "adb devices"
    std = os.popen(cmd)
    lines = std.readlines()
    if len(lines) < 2: return None

    # ids = []
    # for line in lines[1:]:
    #     res = re.search('([0-9a-zA-Z]+)', line)
    #     if res:
    #         ids.append(res.group(1))

    ids = [line.split('\t')[0].strip() for line in lines if '\t' in line]
    if len(ids) < 2:
        return ids[0]
    else:
        return ids


def getANR():
    cmd = 'adb pull /data/anr/traces.txt .'
    os.popen(cmd)


if __name__ == "__main__":
    print getDeviceId()
