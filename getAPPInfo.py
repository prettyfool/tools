# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def getInstalledAPP():
    # 获取已安装的第三方应用列表
    installed = []
    cmd = "adb shell pm list packages -3"
    std = os.popen(cmd)
    for line in std:
        if line and line.startswith('package'):
            package = re.search('package:(\S+)', line).group(1)
            installed.append(package)
    return installed
