# -*- coding:utf-8 -*-
import os
import re


def get_launch_activity(apkpath):
    """
    : 获取app 启动 activity
    """
    cmd = 'aapt d badging %s | findstr launch' % apkpath
    std = os.popen(cmd)
    for line in std:
        if 'launchable' in line:
            launch_activity = re.search("name='(\S+)'", line).group(1)
            return launch_activity


def get_package_info(apkpath):
    """
    : 获取apk 的包名，版本号，版本名称
    : return {packageName: '%s', versionCode: '%s', versionName: '%s'}
    """
    cmd = 'aapt d badging %s | findstr package' % apkpath
    std = os.popen(cmd)
    info = {}
    for line in std:
        if 'package' in line:
            pat = re.compile("name='(\S+)'.*?'(\d+)'.*?'(.*?)'?")
            res = re.search(pat, line)
            info['packageName'], info['versionCode'], info['versionName'] = res.group(1), res.group(2), res.group(3)
    return info


def get_package_name(apkpath):
    """
    : 获取apk 的包名
    """
    return get_package_info(apkpath)['packageName']


def unpack_apk(apkpath):
    """
    : 反编译apk到当前目录
    """
    cmd = 'java -jar .\\lib\\apktool.jar d %s' % apkpath
    os.popen(cmd)


def get_manifest(apkpath):
    """
    : 获取AndroidManifest.xml 的路径
    """
    filedir = os.path.join(os.curdir, os.path.splitext(os.path.basename(apkpath))[0])
    if not os.path.exists(filedir):
        unpack_apk(apkpath)
        print('unpacking...')

    manifest = os.path.join(filedir, 'AndroidManifest.xml')
    return os.path.realpath(manifest)


if __name__ == '__main__':
    apk = r'E:\package\PKG_tugele\SGTugele_v4.3.0_Build_1132_20180416_test_tugele_debug.apk'

    print(get_launch_activity(apk))
    print(get_package_name(apk))
    print(get_package_info(apk))
    print(get_manifest(apk))
