from __future__ import print_function
import subprocess
import shlex
import time


def run_command(exe, pooling_frequency=1.0):
    proc = subprocess.Popen(shlex.split(exe), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        time.sleep(1.0 / pooling_frequency)

        # returns None while subprocess is running
        retcode = proc.poll()
        line = proc.stdout.readline()
        yield line
        if retcode is not None:
            break

#  def run_command(command):
#      p = subprocess.Popen(command,
#                           stdout=subprocess.PIPE,
#                           stderr=subprocess.STDOUT)
#      return iter(p.stdout.readline, b'')

#  def run_command(command):
#      process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
#      while True:
#          output = process.stdout.readline()
#          if output == '' and process.poll() is not None:
#              break
#          if output:
#              print(output.strip())
#      rc = process.poll()
#      return rc


for line in run_command('python3 python_ping.py'):
    print(line)
