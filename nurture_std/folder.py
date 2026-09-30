from pathlib import Path

class FolderAPI:
    def create(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    def exists(self, path):
        return Path(path).is_dir()
    def list(self, path="."):
        return [p.name for p in Path(path).iterdir()]
    def delete(self, path):
        Path(path).rmdir()
        return True

API = FolderAPI()
