import hashlib

class CryptoAPI:
    def sha256(self, value):
        return hashlib.sha256(str(value).encode()).hexdigest()

API = CryptoAPI()
