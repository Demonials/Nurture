import math
import random

class MathAPI:
    sqrt = staticmethod(math.sqrt)
    sin = staticmethod(math.sin)
    cos = staticmethod(math.cos)
    tan = staticmethod(math.tan)
    floor = staticmethod(math.floor)
    ceil = staticmethod(math.ceil)
    round = staticmethod(round)
    abs = staticmethod(abs)
    random = staticmethod(random.random)

API = MathAPI()
