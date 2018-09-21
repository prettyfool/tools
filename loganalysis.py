import re
import os
import sys

DOUTU_CARASH = 'log\.gif\?(.*)KeyboardState.*'


class Log(object):
    def __init__(self, querysting, **kwargs):
        """
        :param querysting: 只包含主要信息的消息体，即url中的参数
        :param split: 
        :param kwargs: 
        """
        self.params = {}
        if querysting and isinstance(querysting, str):
            for param in querysting.split('&'):
                p_list = param.split('=')
                if len(p_list) == 2:
                    k, v = p_list
                else:
                    k, v = p_list[0], '='.join(p_list[1:])
                self.params[k] = v
        if kwargs:
            for m, n in kwargs:
                self.set(m, n)

    def set(self, name, value):
        setattr(self, name, value)

    def get(self, name):
        value = getattr(self, name, None)
        if value is None:
            value = self.params.get(name, None)
        return value

    @property
    def ip(self):
        return self.line.split()[0]

    @property
    def date(self):
        re_date = re.compile('(\d+/[a-zA-Z]+/\d+)')
        date = re.search(re_date, self.line).group(1)
        return date.replace('/', '-')


class InputCrashLog(Log):
    def __init__(self, line, **kwargs):
        if isinstance(line, str):
            self.line = line.replace('log=log=', 'log=').strip()
        querystring = self._get_querystring()
        super(InputCrashLog, self).__init__(querystring, **kwargs)

    def _get_querystring(self):
        """
        获取log主体
        :return:
        """
        re_info = re.compile(DOUTU_CARASH)
        q = re.search(re_info, self.line).group(1)
        return q

    @property
    def imei(self):
        return self.get('k')

    @property
    def dpi(self):
        return self.get('h')

    @property
    def crash_log(self):
        return self.get('log')

    @property
    def device(self):
        return self.get('i')

    @property
    def crash_type(self):
        type_name = self.crash_log.split(':')[0]
        return type_name.split('.')[-1]


class Process(object):
    def __init__(self, inputfile):
        self.inputfile = inputfile if os.path.isabs(inputfile) else os.path.abspath(inputfile)
        out_dir, ext = os.path.splitext(self.inputfile)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.output = out_dir
        file_name = os.path.basename(log_file)
        self.imei_file = os.path.join(self.output, 'imei_' + file_name)
        self.doutu_file = os.path.join(self.output, 'total_crash_' + file_name)
        self.without_classnotfind_file = os.path.join(self.output, 'without_classnotfind_' + file_name)
        self.no_repeat_file = os.path.join(self.output, 'crashes_no_repeat_' + file_name)
        self.count = os.path.join(self.output, 'count_' + file_name)
        self.temp = set()
        self.imeis = []
        self.crashs = set()
        self.crashs_list = []
        self.crash_count = {}

    def write_file(self, lines, file_path):
        with open(file_path, 'a+') as fp:
            if isinstance(lines, str):
                fp.write(lines)
            if isinstance(lines, list):
                fp.writelines(lines)
        return file_path

    def read_file(self, file_path):
        with open(file_path) as fp:
            for line in fp:
                if 'doutu' in line:
                    yield line

    def run(self):
        lines = self.read_file(self.inputfile)
        for line in lines:
            crash_info = InputCrashLog(line)
            # print('write lines:%s : %s:' % (self.doutu_file, line))
            self.write_file(line, self.doutu_file)
            if 'ClassNotFoundException' not in line:
                self.write_file(line, self.without_classnotfind_file)
                crash = crash_info.crash_log + '\n'
                flag = crash[:240]
                if flag not in self.crashs:
                    self.crashs.add(flag)
                    self.crashs_list.append(crash)
                    self.crash_count[flag] = 1
                else:
                    self.crash_count[flag] += 1
            date = crash_info.date
            imei = crash_info.imei

            if imei and date:
                # print('date:%s imei: %s' % (date, imei))
                if imei not in self.temp:
                    self.imeis.append(date + '\t' + imei + '\n')
                    self.temp.add(imei)

        self.write_file(self.imeis, self.imei_file)
        self.write_file(self.crashs_list, self.no_repeat_file)

        with open(self.count, 'w+') as count:
            for key, value in self.crash_count.items():
                c = '{0:<3} {1}\n'.format(value, key)
                count.write(c)


if __name__ == '__main__':
    log_path = r'D:\TestData\log_analysis\plugin_crash_log\0920Test'
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    if os.path.isdir(log_path):
        log_list = [os.path.join(log_path, log_file) for log_file in os.listdir(log_path)]
    else:
        log_list = [log_path]
    for log_file in log_list:
        if os.path.isfile(log_file):
            process = Process(log_file)
            process.run()
