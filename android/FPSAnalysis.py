#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author : majunfeng
# @date   : 2021/1/27 17:25
# @desc   : 测试获取 Android 应用的卡顿率指标和FPS值

import subprocess
import time
from pprint import pprint

PACKAGE_NAME = 'com.sohu.inputmethod.sogou.xiaomi'


class FPS(object):
    def __init__(self, device_id=None):
        self.device_id = device_id
        self.cmd = f'adb shell dumpsys gfxinfo {PACKAGE_NAME}'
        if self.device_id:
            self.cmd = f'adb -s {self.device_id} shell dumpsys gfxinfo {PACKAGE_NAME}'
        self.result = None

    def set_deviceid(self, device_id):
        self.device_id = device_id

    def calculate(self, frames):
        """
        计算当前view 的同步帧率和卡顿率， 每超过16.67ms认为卡顿一次，且每超过一个16.67ms，则有一个垂直同步信号，意味着丢失了一帧
        :param frames: 当前view的数据帧集合，每帧包含draw, prepare, process, execute 四个阶段耗时时间
        :return: 当前fps和卡顿率
        """
        if not frames or not isinstance(frames, list):
            return {}
        jank_times = 0
        vsync_times = 0
        for frame in frames:
            frame = frame.strip()
            draw, prepare, process, execute = frame.strip().split('\t')
            once_time = float(draw) + float(prepare) + float(process) + float(execute)
            if once_time > 16.67:
                jank_times += 1
            # 获取垂直同步信号发生的次数，若一次信号发生时，未绘制完成一帧，则画面会展示旧的帧，也意味着丢失了一帧
            if once_time % 16.67 == 0:
                vsync_times += int(once_time / 16.67) - 1
            else:
                vsync_times += once_time // 16.67
        # 理论总帧数 = 实际帧数 + 执行时间//16.67
        fps = len(frames) / (len(frames) + vsync_times) * 60
        lost_frame_rate = float(jank_times / len(frames))
        return {
            "fps": round(fps, 2),
            "lost_frame_rate": str(round(lost_frame_rate * 100, 2)) + '%'
        }

    def _parse_stdout(self, content):
        """
        临时使用输出结果”暴力“解析
        :param content:
        :return:
        """
        start_flag = 'Profile data in ms:'
        end_flag = 'View hierarchy'
        index = content.find(start_flag) + len(start_flag) + 1
        end = content.find(end_flag)
        views_data = content[index: end].strip()
        result = {}
        for view_data in views_data.split('\r\n\r\n'):
            frames = view_data.split('\r\n')
            head = frames[0].strip()
            key = None
            if ':' in head:
                key = head.split(':')[0]
            elif '/' in head:
                key = head.split('/')[0]
            else:
                key = 'unknown'
            result[key] = self.calculate(frames[2:])
        return result

    def export(self, content, filename=None):
        if filename is None:
            filename = f'{time.time()}.txt'
        with open(filename, 'a+') as fp:
            fp.write(content)

    def _collect_once(self, export=False):
        gfx = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _out = gfx.stdout.read().decode('utf-8')
        if export:
            self.export(_out)
        return self._parse_stdout(_out)

    def collect_once(self):
        res = self._collect_once(True)
        self.result = res

    def collect_long(self, later_time):
        """
        连续执行一估时间，每秒采集一次数据结果，并返回结果列表
        :param later_time: 设置执行时间，单位s
        :return:
        """
        self.result = []
        for i in range(later_time):
            time.sleep(1)
            self.result.append(self._collect_once())

    def report(self):
        pprint(self.result)
        return self.result


if __name__ == '__main__':
    tester = FPS()
    tester.collect_once()
    # tester.collect_long(20)
    tester.report()
