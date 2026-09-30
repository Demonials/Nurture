from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

class Response:
    def __init__(self, response, body):
        self.status = response.status
        self.headers = dict(response.headers.items())
        self.cookies = response.headers.get("Set-Cookie", "")
        self.text = body.decode("utf-8", errors="replace")
    def __repr__(self):
        return f"<Response {self.status}>"

class WebAPI:
    def request(self, method, url, data=None, headers=None):
        headers = headers or {}
        payload = None
        if data is not None:
            if isinstance(data, (dict, list)):
                payload = json.dumps(data).encode()
                headers = {"Content-Type": "application/json", **headers}
            else:
                payload = str(data).encode()
        req = Request(url, data=payload, headers=headers, method=method.upper())
        with urlopen(req, timeout=15) as r:
            return Response(r, r.read())

    def get(self, url, headers=None, params=None):
        if params:
            url += ("&" if "?" in url else "?") + urlencode(params)
        return self.request("GET", url, headers=headers)

    def post(self, url, data=None, headers=None):
        return self.request("POST", url, data, headers)

    def put(self, url, data=None, headers=None):
        return self.request("PUT", url, data, headers)

    def delete(self, url, headers=None):
        return self.request("DELETE", url, headers=headers)

    def download(self, url, filename):
        with urlopen(url, timeout=30) as r, open(filename, "wb") as f:
            f.write(r.read())
        return True

    def status(self, url):
        return self.get(url).status

    def headers(self, url):
        return self.get(url).headers

    def cookies(self, url):
        return self.get(url).cookies

    def screenshot(self, url, filename, full=True):
        raise RuntimeError("web.screenshot needs a browser backend and is not included yet")

API = WebAPI()
