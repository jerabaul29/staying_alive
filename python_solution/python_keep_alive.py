from __future__ import print_function
import subprocess
import shlex
import time


class command_runner(object):
    def __init__(self):
        """No init needed."""
        pass

    def start_command(self, exe):
        """Start a new process for the command to execute."""
        self.proc = subprocess.Popen(shlex.split(exe), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def pool(self):
        """Check if some standard output and provide it as a generator."""
        while(True):
            retcode = self.proc.poll()
            line = self.proc.stdout.readline()

            if line is not b'':
                yield line

            if retcode is not None:
                break

    def kill(self):
        """Kill the process."""
        self.proc.kill()


def launch_and_keep_alive(command, frequency_check=1.0, time_to_start_s=60.0):
    """Launch the process corresponding to command in a separate thread. Give it
    time_to_start_s seconds to start. Following this, check at frequency_check that
    some standard output is provided. If not standard output provided, assume dead or
    stalled so kill and restart."""

    process_active = False
    command_runner_instance = command_runner()

    while(True):

        # if no process active, restart one
        if not process_active:
            command_runner_instance.start_command(command)
            time.sleep(time_to_start_s)
            process_active = True

        time.sleep(1.0 / frequency_check)

        # at this stage, the process is active; need to check if some output has
        # come out; if not, kill and restart

        try:
            yielder = command_runner_instance.pool()

            # try to get one more; if exhausted of dead, it will except
            print(next(yielder))

            # if not exhausted or dead, empty all of it
            for crrt_elem in yielder:
                print(crrt_elem)

        except:
            print("dead or stalled processed!")
            command_runner_instance.kill()
            process_active = False


if __name__ == "__main__":
    launch_and_keep_alive('python3 python_ping.py', time_to_start_s=0.5)
