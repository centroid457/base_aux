from typing import *
import pathlib

from base_aux.base_statics.m1_types import *
from base_aux.path1_dir.m2_dir import *


# =====================================================================================================================
class FileAux:
    """
    GOAL
    ----
    single file work!
    """
    FILEPATH: TYPE__PATH_FINAL

    def __init__(self, filepath: TYPE__PATH_DRAFT) -> None:
        self.FILEPATH = pathlib.Path(filepath)

    # -----------------------------------------------------------------------------------------------------------------
    def ensure_dir(self) -> None:
        DirAux(self.FILEPATH.parent).create_dirtree()

    # READ/WRITE ======================================================================================================
    # READ ---------------------------------
    def read__text(self) -> Optional[str]:
        if self.FILEPATH.exists() and self.FILEPATH.is_file():
            return self.FILEPATH.read_text(encoding="utf-8")

    def read__bytes(self) -> Optional[bytes]:
        if self.FILEPATH.exists() and self.FILEPATH.is_file():
            return self.FILEPATH.read_bytes()

    # WRITE ---------------------------------
    def write__text(self, text: str) -> int:
        self.ensure_dir()
        return self.FILEPATH.write_text(data=text, encoding="utf-8")

    def append__lines(self, *lines: str) -> int | NoReturn:
        count = 0

        if lines:
            self.ensure_dir()
            with open(file=self.FILEPATH, encoding="UTF-8", mode="a") as file:
                # if file NOT EXISTS - it creates!!!
                for line in lines:
                    line = str(line).strip("\n")
                    line = f"\n{line}"

                    if file.write(line):
                        count += 1

        return count

    def write__bytes(self, data: bytes) -> Optional[int]:
        if self.FILEPATH:
            self.ensure_dir()
            return self.FILEPATH.write_bytes(data=data)


# =====================================================================================================================
