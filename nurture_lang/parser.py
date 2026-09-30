from .lexer import lex

class Node:
    def __init__(self, kind, text="", children=None, line=0):
        self.kind = kind
        self.text = text
        self.children = children or []
        self.line = line

def parse(source):
    root = Node("program")
    stack = [(-1, root)]

    for token in lex(source):
        while stack[-1][0] >= token.indent:
            stack.pop()

        parent = stack[-1][1]
        text = token.value

        if text.endswith("->"):
            node = Node("block", text[:-2].strip(), [], token.line)
            parent.children.append(node)
            stack.append((token.indent, node))
        elif text.endswith(":"):
            node = Node("block", text[:-1].strip(), [], token.line)
            parent.children.append(node)
            stack.append((token.indent, node))
        elif "->" in text:
            head, body = text.split("->", 1)
            parent.children.append(
                Node("inline", head.strip(), [Node("line", body.strip(), [], token.line)], token.line)
            )
        else:
            parent.children.append(Node("line", text, [], token.line))

    return root
