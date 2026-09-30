from pathlib import Path

class FileAPI:
    def read(self, path):
        return Path(path).read_text(encoding="utf-8")
    def write(self, path, data):
        Path(path).write_text(str(data), encoding="utf-8")
        return True
    def append(self, path, data):
        with Path(path).open("a", encoding="utf-8") as f:
            f.write(str(data))
        return True
    def exists(self, path):
        return Path(path).is_file()
    def delete(self, path):
        p = Path(path)
        if p.is_file():
            p.unlink()
            return True
        return False

API = FileAPI()
