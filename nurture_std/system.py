import os
import platform
import socket

class SystemAPI:
    def os(self): return platform.system()
    def kernel(self): return platform.release()
    def cpu(self): return platform.processor()
    def memory(self):
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            return {"disk_total": total, "disk_used": used, "disk_free": free}
        except Exception:
            return {}
    def hostname(self): return socket.gethostname()
    def architecture(self): return platform.machine()
    def env(self, name): return os.environ.get(name)

API = SystemAPI()
