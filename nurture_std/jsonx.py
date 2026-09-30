import json

class JSONAPI:
    def read(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    def write(self, path, value):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(value, f, indent=2)
        return True
    def make(self, value):
        return json.dumps(value)
    def parse(self, text):
        return json.loads(text)

API = JSONAPI()
