from datetime import datetime

class TimeAPI:
    def now(self):
        return datetime.now().astimezone().isoformat(timespec="seconds")

API = TimeAPI()
