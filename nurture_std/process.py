import os
import signal
import subprocess

class ProcessAPI:
    def list(self):
        command = ["tasklist"] if os.name == "nt" else ["ps", "-e"]
        return subprocess.run(command, capture_output=True, text=True).stdout

    def info(self, pid):
        if os.name == "nt":
            command = ["tasklist", "/FI", f"PID eq {int(pid)}"]
        else:
            command = ["ps", "-p", str(int(pid)), "-f"]
        return subprocess.run(command, capture_output=True, text=True).stdout

    def start(self, command):
        return subprocess.Popen(command, shell=True).pid

    def stop(self, pid):
        os.kill(int(pid), signal.SIGTERM)
        return True

API = ProcessAPI()
