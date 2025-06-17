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

    # PyQt5 Qthread
    "exec", "exec_", "pyqtConfigure",
    "dump",  # 'dumpObjectInfo' from PyQt5.QMenu

    # GIT
    "checkout", "detach",

    # threads
    "run", "start", "wait", "join", "terminate", "quit", "disconnect",

    # change collection content/count/order
    "pop", "popleft",
    "append", "appendleft",
    "extend", "extendleft",
    "add", "insert",
    "reverse", "rotate", "sort",

    # SYS
    "breakpointhook",
]


# =====================================================================================================================
class ExampleAttrs1_Existed:
    """
    just a set of exact attrs
    """
    AE1 = 1
    _AE1 = 11
    __AE1 = 111


class ExampleAttrs2_AnnotMiddle:
    AN2: int = 2
    _AN2: int = 22
    __AN2: int = 222


class ExampleAttrs32_AnnotLast(ExampleAttrs2_AnnotMiddle):
    AN3: int = 3
    _AN3: int = 33
    __AN3: int = 333


class ExampleAttrs0321(ExampleAttrs32_AnnotLast, ExampleAttrs1_Existed):
    """
    GOAL
    ----
    keep one class with all specially marked attrs/annots
    for exploring/testing attrs/annots on one object

    SPECIALLY CREATED FOR
    ---------------------
    Base_AttrDictDumping/Base_AttrDiff
    """
    pass


# =====================================================================================================================
