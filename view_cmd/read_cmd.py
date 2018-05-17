__author__ = 'majunfeng'

from sys import stdout
from time import sleep
import os

# Simple example script that counts to 10 at ~2Hz, then stops.
# for count in range(0, 10):
#     print(count + 1)
#     stdout.flush()  # Remember to flush
#     sleep(0.5)
while True:
    cmd = 'adb devices'
    os.popen(cmd)
    stdout.flush()
