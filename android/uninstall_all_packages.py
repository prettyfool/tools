# -*- coding:utf-8 -*-
import os
"""
# 卸载所有已安装的应用
"""

# 保留不卸载的应用
package_keep = [
    'com.sohu.inputmethod.sogou',
    'com.xp.tugele',
    'com.tencent.mobileqq',
    'com.tencent.mm',
    'com.sina.weibo'
]

# 获取所有已安装的第三方应用
installed_app = [app.split(':')[1].rstrip() for app in os.popen('adb shell pm list packages -3') if app.startswith('p')]

if len(installed_app) > 0:
    for app in installed_app:
        if app not in package_keep:
            cmd = 'adb uninstall %s >nul' % app
            res = os.system(cmd)
            if res == 0:
                print('[success] %s uninstall!' % app)
            else:
                print('[fail] %s uninstall!' % app)
else:
    print('no packages from 3')