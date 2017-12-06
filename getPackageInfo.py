# -*- coding:utf-8 -*-
import os, re


def getLaunchActivity(packagename):
    cmd = 'aapt d badging %s | findstr launch' % packagename
    std = os.popen(cmd)
    for line in std:
        if 'launchable' in line:
            launch_activity = re.search("name='(\S+)'", line).group(1)
            return launch_activity



if __name__ == '__main__':
    apk = r'E:\package\PKG_tugele\SGTugele_v4.0.0_Build_964_20171205_test_tugele_debug.apk'
    print getLaunchActivity(apk)
