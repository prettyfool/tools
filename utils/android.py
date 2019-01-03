# coding=utf-8
__author__ = 'majunfeng'
import subprocess


class Device(object):
    def __init__(self, serial):
        self.initADB()
        self._serial = serial

    def _exec(self, cmd):
        proc = subprocess.Popen(cmd)
        proc.wait()

    def initADB(self):
        '''
        :启动adb
        '''
        cmd = 'adb start-server'
        self._exec(cmd)

    def initAPP(self, packagename):
        cmd = 'adb -s {0} shell pm clear {1}'.format(self._serial, packagename)
        self._exec(cmd)

    def startAPP(self, luanchActivity):
        cmd = 'adb -s {0} shell am start {1}'.format(self._serial, luanchActivity)
        self._exec(cmd)

    def initLog(self):
        cmd = 'adb -s {} logcat -c'.format(self._serial)
        self._exec(cmd)

    def get_serial(self):
        pass


class App(object):
    def __init__(self):
        pass
