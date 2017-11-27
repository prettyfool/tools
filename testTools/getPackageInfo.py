# -*- coding:utf-8 -*-
import os, re


def get_lunch_activity_name(pkg_name):
    if not is_install(pkg_name):
        return
    cmd = 'adb shell dumpsys package %s' % pkg_name
    lines = os.popen(cmd).readlines()
    for i in lines:
        if 'android.intent.action.MAIN' in i:
            get_index = lines.index(i)
            dest = lines[get_index + 1]
            lunch = re.search(r'(%s\S+)' % pkg_name, dest)
            return lunch.group(1)
            break


def get_installed(isUserApp=True):
    cmd = 'adb shell pm list packages'
    if isUserApp:
        cmd += ' -3'
    installed = [app.split(':')[1].rstrip() for app in os.popen(cmd) if app.startswith('p')]
    if len(installed) == 0:
        print 'app installed no get,please check %s' % cmd
    return installed


def is_install(pkg_name):
    if pkg_name in get_installed():
        return True
    else:
        print '%s not installed' % pkg_name
        return False


if __name__ == '__main__':
    pkg_info = {}
    pkg_info['pkg_name'] = 'com.xp.tugele'
    pkg_info['lunch_activity'] = get_lunch_activity_name(pkg_name='%(pkg_name)s' % pkg_info)
    cmd = {}
    cmd['lunch'] = 'adb shell am start %(lunch_activity)s' % pkg_info
    os.popen('%(lunch)s' % cmd)
