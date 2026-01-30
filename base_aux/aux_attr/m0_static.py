from typing import *


# =====================================================================================================================
def check_name__buildin(name: str) -> bool:
    return name.startswith("__") and name.endswith("__") and len(name) > 4


# =====================================================================================================================
"""
GOAL
----
collect all variants for attr-names which better to skip cause of damage/break/make irreversible changes in original object
"""
NAMES__SKIP_PARTS: list[str] = [
    # DANGER
    "init", "new", "create", "enter", "install",
    "set",
    "clone", "copy", "move",
    "next",
    "clear", "reduce",
    "close", "del", "exit", "kill", "abort",

    # GIT
    "commit",
    "checkout",

    "attach", "detach",

    # threads/process/execution
    "connect", "disconnect",
    "exec", "exec_", "pyqtConfigure",   # PyQt5 Qthread
    "run", "start",
    "wait", "pause", "continue",
    "join",
    "terminate", "quit", "stop",

    # change collection content/count/order
    "pop", "popleft",
    "put", "input",
    "extend", "extendleft",
    "append", "appendleft",
    "update",
    "add", "insert",
    "reverse", "rotate", "sort",

    # data
    "load", "reload",
    "dump",  # 'dumpObjectInfo' from PyQt5.QMenu
    "move", "remove",

    # RE*
    "rename",
    "remove",
    "resize",
    "restart",
    "reload",

    # UN*
    "unpause"
    
    # SYS
    "breakpointhook",
    "hook",
    # "__subclasshook__",   # bs4
    # "__unicode__",
]


# =====================================================================================================================
class ExampleAttrs1_Existed:
    """
    just a set of exact attrs
    """
    AE1 = 1
    _AE1 = 11
    __AE1 = 111
    __AE1__ = 1111

    def meth1(self):
        return 1

    def _meth1(self):
        return 11

    def __meth1(self):
        return 111

    def __meth1__(self):
        return 1111


# ---------------------------------------------------------------------------------------------------------------------
class ExampleAttrs21_AnnotMiddle(ExampleAttrs1_Existed):
    AN2: int = 2
    _AN2: int = 22
    __AN2: int = 222
    __AN2__: int = 2222

    def meth2(self) -> int:
        return 2

    def _meth2(self) -> int:
        return 22

    def __meth2(self) -> int:
        return 222

    def __meth2__(self) -> int:
        return 2222


# ---------------------------------------------------------------------------------------------------------------------
class ExampleAttrs321_AnnotLast(ExampleAttrs21_AnnotMiddle):
    AN3: int = 3
    _AN3: int = 33
    __AN3: int = 333
    __AN3__: int = 3333

    def meth3(self) -> int:
        return 3

    def _meth3(self) -> int:
        return 33

    def __meth3(self) -> int:
        return 333

    def __meth3__(self) -> int:
        return 3333


# =====================================================================================================================
