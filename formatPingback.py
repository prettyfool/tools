#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import time

file_name = 'pb.sogou.com_access_log'
ip = '10.129.192.228'
if len(sys.argv) > 0:
    ip = str(sys.argv[1])
p = 0
while True:
    try:
        f = open(file_name)
        f.seek(p)
        for line in f:
            if ip in line:
                # print line,
                pat = re.search('GET\s(\S+)\s', line)
                event, parms = pat.group(1).split('?')
                now = time.strftime('%Y-%m-%d %H:%M:%S')
                print '\n', now, ip, '\n', event
                for parm in parms.split('&'):
                    print '\t', parm.replace('=', ' = ')
        p2 = f.tell()
        if p2 > p:
            p = p2
        f.close()
    except KeyboardInterrupt:
        f.close()
        break
