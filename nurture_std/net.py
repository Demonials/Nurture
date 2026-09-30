import platform
import socket
import subprocess

class NetAPI:
    def resolve(self, host):
        return socket.gethostbyname(host)

    def localip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    def hostname(self):
        return socket.gethostname()

    def interfaces(self):
        try:
            return socket.if_nameindex()
        except Exception:
            return []

    def ping(self, host):
        flag = "-n" if platform.system().lower() == "windows" else "-c"
        return subprocess.run(["ping", flag, "1", host], capture_output=True).returncode == 0

class CheckAPI:
    def port(self, host, port, timeout=1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            return s.connect_ex((host, int(port))) == 0
        finally:
            s.close()

API = NetAPI()
CHECK = CheckAPI()
