class Registry:
    def __init__(self):
        self.items = {}

    def add(self, name, syntax, description, example="", category="core"):
        self.items[name] = {"syntax": syntax, "description": description, "example": example, "category": category}

    def roots(self):
        keywords = {"if", "elif", "else", "while", "loop", "function", "return", "try", "except", "link"}
        roots = {x.split(".")[0] for x in self.items}
        return sorted(roots | keywords)

    def members(self, prefix):
        p = prefix.lower()
        call_names = {"get","post","put","delete","request","download","screenshot","status","headers","cookies","resolve","localip","hostname","interfaces","ping","port","read","write","append","exists","create","list","make","parse","sha256","os","kernel","cpu","memory","architecture","env","sqrt","sin","cos","tan","floor","ceil","round","abs","random","now","info","start","stop"}
        return sorted({name + ("()" if name.split(".")[-1] in call_names else "") for name in self.items if name.lower().startswith(p)})

    def documentation(self):
        lines = ["NURTURE COMMAND REGISTRY", ""]
        for name in sorted(self.items):
            d = self.items[name]
            lines.extend([name, "  Syntax: " + d["syntax"], "  " + d["description"], ("  Example: " + d["example"]) if d["example"] else "", ""])
        return "\n".join(lines)

registry = Registry()

DATA = [
("write","write(value)","Print a value","write('Hello')","core"),
("input","input(prompt)","Read a line from the command line","name = input('Name: ')","core"),
("int","int(value)","Convert a value to integer","age = int(input('Age: '))","core"),
("float","float(value)","Convert a value to float","x = float(input('Number: '))","core"),
("str","str(value)","Convert a value to text","write(str(123))","core"),
("bool","bool(value)","Convert a value to boolean","write(bool(1))","core"),
("len","len(value)","Get length","write(len('Nurture'))","core"),
("type","type(value)","Get Nurture value type","write(type(123))","core"),
("web.get","web.get(url, headers={}, params={})","HTTP GET","r = web.get(url)","web"),
("web.post","web.post(url, data={}, headers={})","HTTP POST","r = web.post(url, {})","web"),
("web.put","web.put(url, data={}, headers={})","HTTP PUT","r = web.put(url, {})","web"),
("web.delete","web.delete(url, headers={})","HTTP DELETE","r = web.delete(url)","web"),
("web.request","web.request(method, url, data={}, headers={})","Generic HTTP request","r = web.request('GET', url)","web"),
("web.download","web.download(url, filename)","Download a file","web.download(url, 'a.txt')","web"),
("web.screenshot","web.screenshot(url, filename, full=true)","Browser screenshot backend placeholder","web.screenshot(url, 'page.png')","web"),
("web.status","web.status(url)","Get HTTP status","write(web.status(url))","web"),
("web.headers","web.headers(url)","Get response headers","write(web.headers(url))","web"),
("web.cookies","web.cookies(url)","Get response cookies","write(web.cookies(url))","web"),
("net.resolve","net.resolve(host)","Resolve hostname","write(net.resolve('example.com'))","net"),
("net.localip","net.localip()","Get local IP","write(net.localip())","net"),
("net.hostname","net.hostname()","Get hostname","write(net.hostname())","net"),
("net.interfaces","net.interfaces()","List network interfaces","write(net.interfaces())","net"),
("net.ping","net.ping(host)","Basic reachability test","write(net.ping('example.com'))","net"),
("check.port","check.port(host, port)","Basic TCP connectivity check","write(check.port('127.0.0.1', 8080))","security"),
("file.read","file.read(path)","Read UTF-8 text","write(file.read('a.txt'))","file"),
("file.write","file.write(path, data)","Write UTF-8 text","file.write('a.txt', 'hello')","file"),
("file.append","file.append(path, data)","Append text","file.append('a.txt', 'line')","file"),
("file.exists","file.exists(path)","Check file existence","write(file.exists('a.txt'))","file"),
("file.delete","file.delete(path)","Delete file","file.delete('a.txt')","file"),
("folder.create","folder.create(path)","Create folder","folder.create('data')","folder"),
("folder.exists","folder.exists(path)","Check folder","write(folder.exists('data'))","folder"),
("folder.list","folder.list(path)","List folder","write(folder.list('.'))","folder"),
("folder.delete","folder.delete(path)","Delete empty folder","folder.delete('data')","folder"),
("json.read","json.read(path)","Read JSON","data = json.read('a.json')","json"),
("json.write","json.write(path, value)","Write JSON","json.write('a.json', data)","json"),
("json.make","json.make(value)","Convert value to JSON","text = json.make(data)","json"),
("json.parse","json.parse(text)","Parse JSON text","data = json.parse(text)","json"),
("math.sqrt","math.sqrt(value)","Square root","write(math.sqrt(25))","math"),
("math.sin","math.sin(value)","Sine","write(math.sin(1))","math"),
("math.cos","math.cos(value)","Cosine","write(math.cos(1))","math"),
("math.tan","math.tan(value)","Tangent","write(math.tan(1))","math"),
("math.floor","math.floor(value)","Floor","write(math.floor(2.8))","math"),
("math.ceil","math.ceil(value)","Ceiling","write(math.ceil(2.2))","math"),
("math.round","math.round(value)","Round","write(math.round(2.6))","math"),
("math.abs","math.abs(value)","Absolute value","write(math.abs(-4))","math"),
("math.random","math.random()","Random number","write(math.random())","math"),
("crypto.sha256","crypto.sha256(value)","SHA-256 hash","write(crypto.sha256('hello'))","crypto"),
("system.os","system.os()","Operating system","write(system.os())","system"),
("system.kernel","system.kernel()","Kernel release","write(system.kernel())","system"),
("system.cpu","system.cpu()","CPU information","write(system.cpu())","system"),
("system.memory","system.memory()","Basic memory information","write(system.memory())","system"),
("system.hostname","system.hostname()","Hostname","write(system.hostname())","system"),
("system.architecture","system.architecture()","Architecture","write(system.architecture())","system"),
("system.env","system.env(name)","Environment variable","write(system.env('PATH'))","system"),
("process.list","process.list()","List local processes","write(process.list())","process"),
("process.info","process.info(pid)","Process information","write(process.info(1))","process"),
("process.start","process.start(command)","Start local process","process.start('python --version')","process"),
("process.stop","process.stop(pid)","Stop local process","process.stop(1234)","process"),
("time.now","time.now()","Current date/time","write(time.now())","time"),
]

for item in DATA:
    registry.add(*item)

def root_suggestions(prefix):
    p = prefix.lower()
    return [x for x in registry.roots() if x.lower().startswith(p)]

def member_suggestions(prefix):
    return registry.members(prefix)
