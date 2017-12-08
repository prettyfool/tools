# -*- coding:utf-8 -*-
import os, re
import shutil


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
    # return {packageName: '%s', versionCode: '%s', versionName: '%s'}
    cmd = 'aapt d badging %s | findstr package' % apk
    std = os.popen(cmd)
    info = {}
    for line in std:
        if 'package' in line:
            pat = re.compile("name='(\S+)'.*?'(\d+)'.*?'(.*?)'?")
            res = re.search(pat, line)
            info['packageName'], info['versionCode'], info['versionName'] = res.group(1), res.group(2), res.group(3)
    return info


def getPackageName(apk):
    # 获取apk 的包名
    return getAPPInfo(apk)['packageName']


def decodeAPK(apk):
    # 反编译apk到当前目录
    cmd = 'java -jar apktool.jar d %s' % apk
    os.popen(cmd)


def getManifest(apk):
    decodeAPK(apk)
    filedir = os.path.join(os.curdir, os.path.splitext(os.path.basename(apk))[0])
    if os.path.isdir(filedir):
        manifest = os.path.join(filedir, 'AndroidManifest.xml')
        return os.path.abspath(manifest)


def getActivities(apk):
    # todo
    pass


if __name__ == '__main__':
    apk = r'E:\test\SGTugele_v4.0.0_Build_967_20171207_test_tugele_debug.apk'
    # print getLaunchActivity(apk)
    # print getPackageName(apk)
    # print getAPPInfo(apk)
    print getManifest(apk)
