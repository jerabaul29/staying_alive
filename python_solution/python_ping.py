from __future__ import print_function
import time
import sys

system_print = print


def print(to_print):
    system_print(to_print, flush=True)


for i in range(2):
    # print("hi", flush=True)
    print("hi")
    time.sleep(1.5)

time.sleep(2)
