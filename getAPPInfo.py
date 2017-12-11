# coding=utf-8
__author__ = 'majunfeng'

import os
import re


def getInstalledAPP():
    # 获取已安装的第三方应用列表
    cmd = "adb shell pm list packages -3"
    return [re.search('package:(\S+)', line).group(1) for line in os.popen(cmd) if line and line.startswith('package')]
    # installed = []
    # std = os.popen(cmd)
    # for line in std:
    #     if line and line.startswith('package'):
    #         package = re.search('package:(\S+)', line).group(1)
    #         installed.append(package)
    # return installed


if __name__ == '__main__':
    from datetime import datetime

    start = datetime.now()
    print getInstalledAPP()
    time = datetime.now() - start
    print time
