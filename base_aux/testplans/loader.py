import sys

from typing import *
from pathlib import Path
from importlib import import_module

# from base_aux.base_nest_dunders.m1_init1_source import NestInit_Source
from base_aux.aux_types.m2_info import ObjectInfo
from base_aux.path1_dir.m2_dir import *


# =====================================================================================================================
class ModuleAux:
    ROOT: str = ""
    PKG: str | Any = "TESTPLANS"
    MOD: str = "TCS_PSU800"
    FILE: Path = None

    def __init__(self, pkg: str | Any = None, root = None) -> None:
        if root is not None:
            self.ROOT = root

        if pkg is not None:
            self.PKG = pkg

        if isinstance(self.PKG, str):
            try:
                self.PKG = import_module(f"{self.ROOT}{self.PKG}", self.MOD)
                ObjectInfo(self.PKG).print()
            except Exception as exx:
                print(f"{exx!r}")

        # ----------------
        print(dir(self.PKG))
        print(self.PKG.__name__)

        # print(getattr(self.PKG, self.MOD))  # AttributeError: module 'TESTPLANS' has no attribute 'TCS_PSU800'

        # from self.PKG import self.MOD

    def list__tps(self) -> list[type]:
        pass


# =====================================================================================================================
if __name__ == "__main__":
    # ModuleAux(sys)
    # ModuleAux("sys")
    ModuleAux()

    # print([*DirAux("../testplans/TESTPLANS").iter_dirs()])


# =====================================================================================================================
