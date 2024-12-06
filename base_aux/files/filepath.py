import pathlib
from typing import *
from base_aux.objects import *


# =====================================================================================================================
class FilePath:
    NAME: str = None
    EXT: str = None
    DIRPATH: pathlib.Path = None

    # as properties -------
    NAMEEXT: str
    FILEPATH: pathlib.Path

    @property
    def NAMEEXT(self) -> str:
        result = ""
        if self.NAME is not None:
            result += f"{self.NAME}"
        if self.EXT is not None:
            result += f".{self.EXT}"
        return result

    @property
    def FILEPATH(self) -> pathlib.Path:
        return self.DIRPATH.joinpath(self.NAMEEXT)

    def __init__(
            self,
            name: str = None,
            ext: str = None,
            dirpath: str | pathlib.Path = None,
            /,
            filepath: str | pathlib.Path = None,
            nameext: str = None,
    ):

        if filepath is not None:
            filepath = pathlib.Path(filepath)
            self.DIRPATH = filepath.parent
            self.NAME = filepath.stem
            self.EXT = filepath.suffix.rsplit(".", 1)[-1]

        if dirpath is not None:
            self.DIRPATH = pathlib.Path(dirpath)

        if nameext is not None:
            name_ext: list[str] = nameext.rsplit(".", 1)
            if len(name_ext) == 2:  # DOT exists!
                name, ext = name_ext
                if ext:
                    self.EXT = ext
                if name:
                    self.NAME = name
            else:
                self.NAME = nameext

        # most important! overwrite previous set!
        if name is not None:
            self.NAME = name
        if ext is not None:
            self.EXT = ext


# =====================================================================================================================
if __name__ == '__main__':
    obj = pathlib.Path("hello.")
    ObjectInfo(obj).print()


# =====================================================================================================================
