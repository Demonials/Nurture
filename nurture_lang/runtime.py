import ast
import operator
import re
import builtins

from .parser import parse
from .errors import RuntimeErrorNurture
from nurture_std import file, folder, jsonx, mathx, net, web, crypto, system, process, gui, time


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Runtime:
    def __init__(self, output=print, input_fn=None):
        self.output = output
        self.input_fn = input_fn or builtins.input
        self.vars = {"true": True, "false": False, "null": None}
        self.functions = {}
        self.modules = {
            "file": file.API,
            "folder": folder.API,
            "json": jsonx.API,
            "math": mathx.API,
            "net": net.API,
            "web": web.API,
            "crypto": crypto.API,
            "system": system.API,
            "process": process.API,
            "gui": gui.API,
            "check": net.CHECK,
            "time": time.API,
        }

        # Core functions are always available. Modules can still be explicitly linked.
        self.vars.update({
            "write": self._write,
            "input": self._input,
            "int": self._int,
            "float": self._float,
            "str": self._str,
            "bool": self._bool,
            "len": self._len,
            "type": self._type,
        })

    def execute(self, source):
        try:
            return self.exec_nodes(parse(source).children)
        except ReturnSignal as exc:
            raise RuntimeErrorNurture("return used outside a function") from exc

    def exec_nodes(self, nodes):
        i = 0
        while i < len(nodes):
            n = nodes[i]

            if n.kind == "inline":
                head = n.text
                if head.startswith("loop"):
                    self.run_loop_header(head, n.children)
                else:
                    raise RuntimeErrorNurture(f"inline block not supported: {head}")
                i += 1
                continue

            if n.kind == "block":
                h = n.text

                if h.startswith("if "):
                    branches = [n]
                    j = i + 1
                    while j < len(nodes) and nodes[j].kind == "block" and (
                        nodes[j].text.startswith("elif ") or nodes[j].text == "else"
                    ):
                        branches.append(nodes[j])
                        j += 1
                    for b in branches:
                        if b.text == "else":
                            cond = True
                        elif b.text.startswith("elif "):
                            cond = self.eval_expr(b.text[5:])
                        else:
                            cond = self.eval_expr(b.text[3:])
                        if cond:
                            self.exec_nodes(b.children)
                            break
                    i = j
                    continue

                if h.startswith("while "):
                    count = 0
                    while self.eval_expr(h[6:]):
                        self.exec_nodes(n.children)
                        count += 1
                        if count > 100000:
                            raise RuntimeErrorNurture("while loop exceeded 100000 iterations")
                    i += 1
                    continue

                if h.startswith("loop"):
                    self.run_loop_header(h, n.children)
                    i += 1
                    continue

                if h.startswith("function "):
                    self.define_function(h[9:], n.children)
                    i += 1
                    continue

                if h == "try":
                    try:
                        self.exec_nodes(n.children)
                    except ReturnSignal:
                        raise
                    except Exception as exc:
                        if i + 1 < len(nodes) and nodes[i + 1].kind == "block" and nodes[i + 1].text.startswith("except"):
                            except_node = nodes[i + 1]
                            # Optional: except ErrorName
                            self.exec_nodes(except_node.children)
                            i += 2
                            continue
                        raise
                    i += 1
                    continue

                if h.startswith("except"):
                    i += 1
                    continue

                raise RuntimeErrorNurture(f"unknown block: {h}")

            self.exec_line(n.text)
            i += 1

    def run_loop_header(self, header, children):
        header = header.strip()
        m = re.fullmatch(r"loop\s*\((.*?)\)", header)
        if m:
            parts = self._split_args(m.group(1))
            if len(parts) not in (2, 3):
                raise RuntimeErrorNurture("loop syntax: loop(start, end) or loop(start, end, step)")
            start = int(self.eval_expr(parts[0]))
            end = int(self.eval_expr(parts[1]))
            if len(parts) == 3:
                step = int(self.eval_expr(parts[2]))
                if step == 0:
                    raise RuntimeErrorNurture("loop step cannot be zero")
            else:
                step = 1 if end >= start else -1
            stop = end + (1 if step > 0 else -1)
            for value in range(start, stop, step):
                self.vars["i"] = value
                self.exec_nodes(children)
            return

        m = re.fullmatch(r"loop\s+([A-Za-z_]\w*)\s+in\s+(.+)", header)
        if m:
            name, expression = m.groups()
            if ".." in expression:
                a, b = expression.split("..", 1)
                start = int(self.eval_expr(a))
                end = int(self.eval_expr(b))
                values = range(start, end + 1) if end >= start else range(start, end - 1, -1)
            else:
                values = self.eval_expr(expression)
            for value in values:
                self.vars[name] = value
                self.exec_nodes(children)
            return

        raise RuntimeErrorNurture("loop syntax: loop i in 1..10 or loop(1, 10)")

    def define_function(self, spec, body):
        m = re.fullmatch(r"([A-Za-z_]\w*)\s*\((.*?)\)", spec.strip())
        if not m:
            raise RuntimeErrorNurture("invalid function declaration")
        name, raw = m.groups()
        params = [x.strip() for x in self._split_args(raw) if x.strip()]
        self.functions[name] = (params, body)

    def call_function(self, name, args):
        params, body = self.functions[name]
        if len(params) != len(args):
            raise RuntimeErrorNurture(f"{name} expects {len(params)} arguments")
        old = self.vars.copy()
        self.vars.update(zip(params, args))
        try:
            self.exec_nodes(body)
        except ReturnSignal as r:
            return r.value
        finally:
            self.vars = old
        return None

    def exec_line(self, line):
        line = line.strip()
        if not line:
            return

        if line.startswith("link "):
            name = line[5:].strip()
            if name not in self.modules:
                raise RuntimeErrorNurture(f"unknown module: {name}")
            self.vars[name] = self.modules[name]
            return

        if line.startswith("return") and (line == "return" or line[6:7].isspace()):
            value = line[6:].strip()
            raise ReturnSignal(self.eval_expr(value) if value else None)

        m = re.fullmatch(r"([A-Za-z_]\w*)\s*=\s*(?![=])(.+)", line)
        if m:
            self.vars[m.group(1)] = self.eval_expr(m.group(2))
            return

        self.eval_expr(line)

    def eval_expr(self, expression):
        expression = expression.strip()
        expression = re.sub(r"\btrue\b", "True", expression, flags=re.I)
        expression = re.sub(r"\bfalse\b", "False", expression, flags=re.I)
        expression = re.sub(r"\bnull\b", "None", expression, flags=re.I)

        try:
            node = ast.parse(expression, mode="eval").body
            return self.eval_ast(node)
        except RuntimeErrorNurture:
            raise
        except Exception as exc:
            raise RuntimeErrorNurture(f"invalid expression: {expression}") from exc

    def eval_ast(self, n):
        if isinstance(n, ast.Constant):
            return n.value

        if isinstance(n, ast.Name):
            if n.id in self.vars:
                return self.vars[n.id]
            if n.id in self.functions:
                return lambda *args: self.call_function(n.id, list(args))
            raise RuntimeErrorNurture(f"unknown name: {n.id}")

        if isinstance(n, ast.Attribute):
            obj = self.eval_ast(n.value)
            try:
                return getattr(obj, n.attr)
            except AttributeError as exc:
                raise RuntimeErrorNurture(f"unknown member: {n.attr}") from exc

        if isinstance(n, ast.Call):
            fn = self.eval_ast(n.func)
            args = [self.eval_ast(x) for x in n.args]
            kwargs = {x.arg: self.eval_ast(x.value) for x in n.keywords}
            return fn(*args, **kwargs)

        if isinstance(n, ast.List):
            return [self.eval_ast(x) for x in n.elts]
        if isinstance(n, ast.Tuple):
            return tuple(self.eval_ast(x) for x in n.elts)
        if isinstance(n, ast.Set):
            return {self.eval_ast(x) for x in n.elts}
        if isinstance(n, ast.Dict):
            return {self.eval_ast(k): self.eval_ast(v) for k, v in zip(n.keys, n.values)}
        if isinstance(n, ast.Subscript):
            return self.eval_ast(n.value)[self.eval_ast(n.slice)]

        if isinstance(n, ast.BinOp):
            a, b = self.eval_ast(n.left), self.eval_ast(n.right)
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.FloorDiv: operator.floordiv,
                ast.Mod: operator.mod,
                ast.Pow: operator.pow,
            }
            fn = ops.get(type(n.op))
            if not fn:
                raise RuntimeErrorNurture("operator not supported")
            try:
                return fn(a, b)
            except Exception as exc:
                raise RuntimeErrorNurture(str(exc)) from exc

        if isinstance(n, ast.UnaryOp):
            v = self.eval_ast(n.operand)
            if isinstance(n.op, ast.USub):
                return -v
            if isinstance(n.op, ast.UAdd):
                return +v
            if isinstance(n.op, ast.Not):
                return not v
            raise RuntimeErrorNurture("unary operator not supported")

        if isinstance(n, ast.BoolOp):
            if isinstance(n.op, ast.And):
                for value in n.values:
                    if not self.eval_ast(value):
                        return False
                return True
            if isinstance(n.op, ast.Or):
                for value in n.values:
                    if self.eval_ast(value):
                        return True
                return False
            raise RuntimeErrorNurture("boolean operator not supported")

        if isinstance(n, ast.Compare):
            left = self.eval_ast(n.left)
            for op_node, right_node in zip(n.ops, n.comparators):
                right = self.eval_ast(right_node)
                try:
                    if isinstance(op_node, ast.Eq): result = left == right
                    elif isinstance(op_node, ast.NotEq): result = left != right
                    elif isinstance(op_node, ast.Lt): result = left < right
                    elif isinstance(op_node, ast.LtE): result = left <= right
                    elif isinstance(op_node, ast.Gt): result = left > right
                    elif isinstance(op_node, ast.GtE): result = left >= right
                    elif isinstance(op_node, ast.In): result = left in right
                    elif isinstance(op_node, ast.NotIn): result = left not in right
                    elif isinstance(op_node, ast.Is): result = left is right
                    elif isinstance(op_node, ast.IsNot): result = left is not right
                    else: raise RuntimeErrorNurture("comparison not supported")
                except TypeError as exc:
                    raise RuntimeErrorNurture(str(exc)) from exc
                if not result:
                    return False
                left = right
            return True

        raise RuntimeErrorNurture(f"expression not supported: {type(n).__name__}")

    def _write(self, value=None):
        self.output(value)
        return value

    def _input(self, prompt=""):
        return self.input_fn(str(prompt))

    @staticmethod
    def _int(value=0):
        return int(value)

    @staticmethod
    def _float(value=0):
        return float(value)

    @staticmethod
    def _str(value=""):
        return str(value)

    @staticmethod
    def _bool(value=False):
        return bool(value)

    @staticmethod
    def _len(value):
        return len(value)

    @staticmethod
    def _type(value):
        return type(value).__name__

    @staticmethod
    def _split_args(text):
        if not text.strip():
            return []
        parts, current = [], []
        depth = 0
        quote = None
        escaped = False
        for ch in text:
            if escaped:
                current.append(ch)
                escaped = False
                continue
            if ch == "\\" and quote:
                current.append(ch)
                escaped = True
                continue
            if quote:
                current.append(ch)
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"":
                quote = ch
                current.append(ch)
            elif ch in "([{":
                depth += 1
                current.append(ch)
            elif ch in ")]}":
                depth -= 1
                current.append(ch)
            elif ch == "," and depth == 0:
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        parts.append("".join(current).strip())
        return parts
