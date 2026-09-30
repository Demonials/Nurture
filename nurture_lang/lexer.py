from dataclasses import dataclass

@dataclass
class Token:
    kind: str
    value: str
    line: int
    indent: int

def lex(source):
    out = []
    for number, raw in enumerate(source.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        out.append(Token("LINE", raw.strip(), number, indent))
    return out
