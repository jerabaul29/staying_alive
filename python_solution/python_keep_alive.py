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


def launch_and_keep_alive(command, frequency_check=1.0, time_to_start_s=60.0):

    process_active = False

    while(True):

        # if no process active, restart one
        if not process_active:
            yielder = run_command(command, pooling_frequency=2.0 * frequency_check)
            time.sleep(time_to_start_s)
            process_active = True

        time.sleep(1.0 / frequency_check)

        # at this stage, the process is active; need to check if some output has
        # come out; if not, kill and restart

        try:
            # try to get one more; if exhausted of dead, it will except
            print(next(yielder))

            # if not exhausted or dead, empty
            for crrt_elem in yielder:
                print(crrt_elem)

        except:
            print("dead or stalled processed!")
            process_active = False


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


#  for line in run_command('python3 python_ping.py'):
#      print(line)

launch_and_keep_alive('python3 python_ping.py', time_to_start_s=0.5)
