import sys

from typing import Any
from pathlib import Path
from importlib import import_module

# from base_aux.base_nest_dunders.m1_init1_source import NestInit_Source
from base_aux.aux_types.m2_info import ObjectInfo
# from base_aux.path1_dir.m2_dir import *


# =====================================================================================================================
class ModuleLocalAux:
    OBJ: Any

    PKG: Path = "TESTPLANS"
    SUBMOD: str = "TCS_PSU800"
    FILE: Path = "tc2_reverse"

    def __init__(self, pkg: Path = None) -> None:
        if pkg is not None:
            self.PKG = pkg

        self.PKG = Path(self.PKG)

        if self.PKG:
            try:
                self.OBJ = import_module(f"{self.PKG.name}.{self.SUBMOD}.{self.FILE}")
                # ObjectInfo(self.PKG, log_iter=True, names__skip_parts=[
                #     "QAbstract", "Q", "transform", "Valid", "TypeAux", "TextIO", "TYPING", "TYPES", "Signals", "Protocol"]).print()
            except Exception as exx:
                print(f"1111{exx!r}")

        # ----------------
        # print(dir(self.PKG))
        # print(self.PKG.__name__)

        # print(getattr(self.PKG, self.SUBMOD))  # AttributeError: module 'TESTPLANS' has no attribute 'TCS_PSU800'

        # from self.PKG import self.SUBMOD
        # self.PKG.TCS_PSU800

    def list__variants(self) -> dict[Path, list[Path]]:
        result = {}
        for path in self.PKG.glob("*"):
            path: Path
            if path.is_dir() and path.name not in ["__pycache__", ]:
                result.update({path: [*path.glob("load*__*.py")]})

        return result

    def list__submod_sets(self) -> list[str]:
        set


# =====================================================================================================================
if __name__ == "__main__":
    # ModuleAux(sys)
    # ModuleAux("sys")
    mod = ModuleLocalAux()
    # print(mod.OBJ.TestCase)
    print(mod.list__variants())

    # print([*DirAux("../testplans/TESTPLANS").iter_dirs()])

    # ObjectInfo(sys).print()
    # ObjectInfo().print()
    print()
    for item in dir(mod.OBJ):
        if not item.startswith("__"):
            print(item)


# =====================================================================================================================
