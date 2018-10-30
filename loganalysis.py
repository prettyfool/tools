import re
import os
import sys

REGEX_DOUTU_CARASH = 'log\.gif\?(.*)HTTP'
REGEX_LOG_DATE = '(\d+/[a-zA-Z]+/[\d+|:])'


class Log(object):
    def __init__(self, line, **kwargs):
        """
        :param kwargs: 
        """
        self.line = line
        if kwargs:
            for m, n in kwargs:
                self.set(m, n)

    def set(self, name, value):
        setattr(self, name, value)

    def get(self, name):
        value = getattr(self, name, None)
        return value

    @property
    def ip(self):
        return self.line.split()[0]

    @property
    def time(self):
        try:
            re_date = re.compile(REGEX_LOG_DATE)
            date = re.search(re_date, self.line).group(1)
            return date.replace('/', '-')
        except:
            return None

    def get_querystring(self, pattern):
        """
        获取log中 的querystring
        :return:
        """
        try:
            re_info = re.compile(pattern)
            query = re.search(re_info, self.line).group(1)
            return query
        except:
            return None


class InputCrashLog(Log):
    def __init__(self, line, **kwargs):
        line = line.replace('log=log=', 'log=').strip()
        super(InputCrashLog, self).__init__(line, **kwargs)
        self._querystring = self.get_querystring(REGEX_DOUTU_CARASH)
        if self._querystring:
            for param in self._querystring.split('&'):
                p_list = param.split('=')
                if len(p_list) == 2:
                    k, v = p_list
                    self.set(k, v)
                else:
                    if '||||' in param:
                        other = param.split('||||')
                        for p in other:
                            self.set(*p.split('='))

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
    def write_file(self, lines, file_path):
        with open(file_path, 'a+') as fp:
            if isinstance(lines, str):
                fp.write(lines)
            if isinstance(lines, list):
                fp.writelines(lines)
        return file_path

    def read_file(self, file_path, filter=None):
        with open(file_path) as fp:
            for line in fp:
                if filter is None:
                    yield line
                    continue
                if filter and filter in line:
                    yield line

    def combine_files(self, src_file_list, dst_file):
        """多个文件内容合并成一个文件"""
        for src in src_file_list:
            for line in self.read_file(src):
                self.write_file(line, dst_file)


class InputProcess(Process):
    def __init__(self, inputfile):
        self.inputfile = inputfile if os.path.isabs(inputfile) else os.path.abspath(inputfile)
        out_dir, ext = os.path.splitext(self.inputfile)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.output = out_dir
        file_name = os.path.basename(self.inputfile)
        if not ext:
            file_name = file_name + '.log'
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

    def run(self):
        lines = self.read_file(self.inputfile, 'doutu')
        for line in lines:
            crash_info = InputCrashLog(line)
            if line:
                self.write_file(line, self.doutu_file)
            if 'ClassNotFoundException' not in line:
                self.write_file(line, self.without_classnotfind_file)
                crash = crash_info.crash_log + '\n'
                # flag = re.sub('\d+', '', crash[:240])
                flag = crash[:240]
                if flag not in self.crashs:
                    self.crashs.add(flag)
                    self.crashs_list.append(line)
                    self.crash_count[flag] = 1
                else:
                    self.crash_count[flag] += 1
            date = crash_info.time
            imei = crash_info.imei

            if imei and date:
                i_d_tuple = (imei, date)
                if i_d_tuple not in self.temp:
                    self.imeis.append(date + '\t' + imei + '\t' + crash_info.get('c') + '\n')
                    self.temp.add(i_d_tuple)

        self.write_file(self.imeis, self.imei_file)
        self.write_file(self.crashs_list, self.no_repeat_file)

        with open(self.count, 'w+') as count:
            for key, value in self.crash_count.items():
                c = '{0:<3} {1}\n'.format(value, key)
                count.write(c)


class Count(object):
    """input crash count about every type crash"""

    def __init__(self):
        # 崩溃总次数和人数
        self.total_num = 0
        self.total_imei = 0
        # class_not_found 崩溃的总次数和人数
        self.class_not_found_num = 0
        self.class_not_found_imei = 0

    def add_total_num(self):
        self.total_num += 1

    def add_total_imei(self):
        self.total_imei += 1

    def add_class_not_found_num(self):
        self.class_not_found_num += 1

    def add_class_not_found_imei(self):
        self.class_not_found_imei += 1


class InputCount(Process):
    def __init__(self, inputfile):
        self.inputfile = os.path.abspath(inputfile)
        self.result = Count()
        self.all_imei = set()
        self.not_found_imei = set()

    def run(self):
        lines = self.read_file(self.inputfile, 'doutu')
        for line in lines:
            crash_info = InputCrashLog(line)
            if line:
                imei = crash_info.imei
                self.result.add_total_num()
                if imei not in self.all_imei:
                    self.result.add_total_imei()
                    self.all_imei.add(imei)
                if 'ClassNotFoundException' in line:
                    self.result.add_class_not_found_num()
                    if imei not in self.not_found_imei:
                        self.result.add_class_not_found_imei()
                        self.not_found_imei.add(imei)
        return self

    def get_result(self):
        print("崩溃总次数：{}".format(self.result.total_num))
        print("崩溃总人数：{}".format(self.result.total_imei))
        print("崩溃总次数(classnotfound)：{}".format(self.result.class_not_found_num))
        print("崩溃总人数(classnotfound)：{}".format(self.result.class_not_found_imei))


if __name__ == '__main__':
    # log_path = r'D:\TestData\log_analysis\plugin_crash_log\combine\combine.log'
    # if len(sys.argv) > 1:
    #     log_path = sys.argv[1]
    # if os.path.isdir(log_path):
    #     log_list = [os.path.join(log_path, log_file) for log_file in os.listdir(log_path)]
    # else:
    #     log_list = [log_path]
    # for log_file in log_list:
    #     if os.path.isfile(log_file):
    #         process = InputProcess(log_file)
    #         process.run()

    # log_path = r'D:\TestData\log_analysis\plugin_crash_log\8.21\20181010_8.21_log.log'
    # res = InputCount(log_path)
    # res.run()
    # res.get_result()

    log_path = r'D:\TestData\log_analysis\plugin_crash_log\8.24'
    log = r'D:\TestData\log_analysis\plugin_crash_log\8.24\combine.log'
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    if os.path.isdir(log_path):
        log_list = [os.path.join(log_path, log_file) for log_file in os.listdir(log_path)]
    else:
        log_list = [log_path]

    # process = Process()
    # process.combine_files(log_list, log)
    # p = InputProcess(log)
    # p.run()
    count = InputCount(log)
    count.run()
    count.get_result()
