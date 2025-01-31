from typing import *

from base_aux.aux_types.m0_types import *
from base_aux.aux_types.m2_info import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.files.m1_res_dirpath import Resolve_DirPath


# =====================================================================================================================
class Resolve_FilePath(Resolver):
    """
    GOAL
    ----
    1/ resolve filepath by draft
    2/ combyne by any part
    3/ replace any part

    SPECIALLY CREATED FOR
    ---------------------
    base_aux.files
    """
    NAME: str = ""
    EXTLAST: str = ""
    DIRPATH: TYPE__PATH_FINAL = None

    DOT: bool = None

    # PROPERTIES ------------------------------------------------------------------------------------------------------
    NAMEEXT: str
    FILEPATH: TYPE__PATH_FINAL

    @property
    def NAMEEXT(self) -> str:
        result = ""
        if self.NAME:
            result += f"{self.NAME}"
        if self.DOT:
            result += f"."
        if self.EXTLAST:
            result += f"{self.EXTLAST}"
        return result

    @property
    def FILEPATH(self) -> TYPE__PATH_FINAL:
        return self.DIRPATH.joinpath(self.NAMEEXT)

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            # separated -----
            name: str = None,
            extlast: str = None,
            nameext: str = None,
            dirpath: TYPE__PATH_DRAFT = None,

            # full -----
            filepath: TYPE__PATH_DRAFT = None,
    ):
        """
        NOTE
        ----
        you can use "filepath" as base/default and others (name/extlast/...) for overwrite some of them base parts
        """
        self.set_filepath(filepath)
        self.set_dirpath(dirpath or self.DIRPATH)
        self.set_nameext(nameext)

        # most important! overwrite previous set!
        if name is not None:
            self.NAME = name
        if extlast is not None:
            self.DOT = True
            self.EXTLAST = extlast

    def set_filepath(self, filepath: TYPE__PATH_DRAFT) -> None:
        if filepath is None:
            return

        filepath = pathlib.Path(filepath)
        self.DIRPATH = filepath.parent
        self.NAME = filepath.stem
        self.EXTLAST = filepath.suffix.rsplit(".", 1)[-1]

        self.DOT = "." in filepath.name

    def set_dirpath(self, dirpath: TYPE__PATH_DRAFT) -> None:
        self.DIRPATH = Resolve_DirPath(dirpath).resolve()

    def set_nameext(self, nameext: str) -> None:
        if nameext is None:
            return

        if "." in nameext:
            self.DOT = True

        name_ext: list[str] = nameext.rsplit(".", 1)
        if len(name_ext) == 2:  # DOT exists!
            _name, _extlast = name_ext
            if _name:
                self.NAME = _name
            if _extlast:
                self.EXTLAST = _extlast
        else:
            self.NAME = nameext
            self.EXTLAST = ""

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> TYPE__PATH_FINAL:
        return self.FILEPATH


# =====================================================================================================================
if __name__ == '__main__':
    obj = pathlib.Path("hello.")
    ObjectInfo(obj).print()


# =====================================================================================================================
