from typing import *


class Cls:
    pass
class Cls2(Cls):
    pass

obj = Cls()
obj2 = Cls2()
print(type(obj))
print(type(obj2))

print(Cls == type(obj))
print(Cls == type(obj2))
print(Cls2 == type(obj))
print(Cls2 == type(obj2))



class TpExecutor:
    def __init__(self, index: int):
        self.index: int = index     # separate stand index!


class TP_SCHEMA:
    TP: Any         # | type    ?????       # group_cls
    TCS_GROUPED: dict[type, list[type]]     # group_cls: list[tc_cls]


