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
