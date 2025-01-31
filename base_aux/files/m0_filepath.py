import pathlib
from typing import *

from base_aux.aux_types.m0_types import *
from base_aux.aux_types.m2_info import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.base_inits.m1_source import *


# =====================================================================================================================
class Resolve_DirPath(InitSource, Resolver):
    """
    GOAL
    ----
    resolve dirpath by draft

    SPECIALLY CREATED FOR
    ---------------------
    Resolve_FilePath init dirpath
    """
    SOURCE: TYPE__PATH_DRAFT | None

    def resolve(self) -> TYPE__PATH_FINAL:
        if self.SOURCE is not None:
            return pathlib.Path(self.SOURCE)
        if self.SOURCE is None:
            return pathlib.Path().cwd()


# =====================================================================================================================
class Resolve_FilePath(Resolver):
    """
    GOAL
    ----
    resolve filepath by draft

    SPECIALLY CREATED FOR
    ---------------------
    base_aux.files
    """
    NAME: str = None
    EXTLAST: str = None
    DIRPATH: pathlib.Path = None

    # PROPERTIES ------------------------------------------------------------------------------------------------------
    NAMEEXT: str
    FILEPATH: pathlib.Path

    @property
    def NAMEEXT(self) -> str:
        result = ""
        if self.NAME is not None:
            result += f"{self.NAME}"
        if self.EXTLAST is not None:
            result += f".{self.EXTLAST}"
        return result

    @property
    def FILEPATH(self) -> pathlib.Path:
        return self.DIRPATH.joinpath(self.NAMEEXT)

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            # separated -----
            name: str = None,
            extlast: str = None,
            dirpath: TYPE__PATH_DRAFT = None,
            nameext: str = None,

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
            self.EXTLAST = extlast

    def set_filepath(self, filepath: TYPE__PATH_DRAFT) -> None:
        if filepath is not None:
            filepath = pathlib.Path(filepath)
            self.DIRPATH = filepath.parent
            self.NAME = filepath.stem
            self.EXTLAST = filepath.suffix.rsplit(".", 1)[-1]

    def set_dirpath(self, dirpath: TYPE__PATH_DRAFT) -> None:
        self.DIRPATH = Resolve_DirPath(dirpath).resolve()

    def set_nameext(self, nameext: str) -> None:
        if nameext is not None:
            name_ext: list[str] = nameext.rsplit(".", 1)
            if len(name_ext) == 2:  # DOT exists!
                _name, _extlast = name_ext
                if _extlast:
                    self.EXTLAST = _extlast
                if _name:
                    self.NAME = _name
            else:
                self.NAME = nameext

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> TYPE__PATH_FINAL:
        return self.FILEPATH


# =====================================================================================================================
if __name__ == '__main__':
    obj = pathlib.Path("hello.")
    ObjectInfo(obj).print()


# =====================================================================================================================
