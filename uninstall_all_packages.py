# -*- coding:utf-8 -*-
import os, re

package_keep = [
    # 打算保留的应用列表
    'com.sohu.inputmethod.sogou',
    'com.tencent.mobileqq',
    'com.xp.tugele'
]
# 卸载不在package_keep 中的所有app
[os.popen('adb uninstall %s' % app) for app in
 (re.search('package:(\S+)', line).group(1) for line in os.popen("adb shell pm list packages -3") if
  line and line.startswith('package')) if app not in package_keep]
