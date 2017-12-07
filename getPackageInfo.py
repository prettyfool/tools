# -*- coding:utf-8 -*-
import os, re


def getLaunchActivity(apk):
    # 获取app 启动 activity
    cmd = 'aapt d badging %s | findstr launch' % apk
    std = os.popen(cmd)
    for line in std:
        if 'launchable' in line:
            launch_activity = re.search("name='(\S+)'", line).group(1)
            return launch_activity


def getAPPInfo(apk):
    # 获取apk 的包名，版本号，版本名称
    cmd = 'aapt d badging %s | findstr package' % apk
    std = os.popen(cmd)
    info = {}
    for line in std:
        if 'package' in line:
            pat = re.compile("name='(\S+)'\s\S+'(\d+)'\s\S+'([\d\.]+)'\s")
            res = re.search(pat, line)
            info['packageName'], info['versionCode'], info['versionName'] = res.group(1), res.group(2), res.group(3)
    return info


def getPackageName(apk):
    # 获取apk 的包名
    return getAPPInfo(apk)['packageName']


if __name__ == '__main__':
    apk = r'E:\package\PKG_tugele\SGTugele_v4.0.0_Build_964_20171205_test_tugele_debug.apk'
    # print getLaunchActivity(apk)
    print getPackageName(apk)
