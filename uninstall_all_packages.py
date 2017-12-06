# -*- coding:utf-8 -*-
import os

# 打算保留的应用列表
package_keep = [
    'com.sohu.inputmethod.sogou',
    'com.tencent.mobileqq',
    'com.xp.tugele'
]
apps = os.popen('adb shell pm list packages -3').readlines()
installed_app = [app.split(':')[1].rstrip() for app in apps]

if len(installed_app) > 0:
    for app in installed_app:
        if app not in package_keep:
            cmd = 'adb uninstall ' + app + ' >nul'
            res = os.system(cmd)
            if res == 0:
                print '[success] %s uninstalled' % app
            else:
                print '[fail] %s uninstalled' % app
    else:
        print 'uninstalled all app'
else:
    print 'no packages from 3'
