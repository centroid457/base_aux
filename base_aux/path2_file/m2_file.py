from typing import *

from base_aux.path1_dir.m2_dir import *
from base_aux.aux_text.m1_text_aux import *


# =====================================================================================================================
class FileAux:
    """
    GOAL
    ----
    single file INTERNAL work!

    textWork use by yourself with TextAux
    """
    FILEPATH: TYPING.PATH_FINAL
    TEXT: str = ""       # keep here just for TextAux work!

    def __init__(self, filepath: TYPING.PATH_DRAFT, *args, **kwargs) -> None | NoReturn:
        self.FILEPATH = pathlib.Path(filepath)
        if self.check_exists():
            if self.FILEPATH.is_file():
                # self.read__text()     # NOTE: dont read here! it maybe Bytes! read only in TextFile!
                pass
            else:
                raise Exx__Incompatible(f"{self.FILEPATH=}")
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def check_exists(self) -> bool:
        return self.FILEPATH.exists()

    def ensure_dir(self) -> None:
        DirAux(self.FILEPATH.parent).create_dirtree()

    def delete_file(self) -> bool:
        self.TEXT = ""
        return DirAux.delete_items(self.FILEPATH)

    def clear_file(self) -> bool:
        self.TEXT = ""
        return self.write__text("") == 0

    # READ/WRITE ======================================================================================================
    # READ ---------------------------------
    def read__text(self) -> Optional[str]:
        if self.FILEPATH.exists() and self.FILEPATH.is_file():
            self.TEXT = self.FILEPATH.read_text(encoding="utf-8")
            return self.TEXT

    def read__bytes(self) -> Optional[bytes]:
        if self.FILEPATH.exists() and self.FILEPATH.is_file():
            return self.FILEPATH.read_bytes()

    # WRITE ---------------------------------
    def write__text(self, text: TYPING.STR_DRAFT = None) -> int:
        if text is not None:
            self.TEXT = str(text)
        self.ensure_dir()
        return self.FILEPATH.write_text(data=self.TEXT, encoding="utf-8")

    def append__lines(self, *lines: TYPING.STR_DRAFT) -> int | NoReturn:
        count = 0

        if lines:
            self.ensure_dir()
            with open(file=self.FILEPATH, encoding="UTF-8", mode="a") as file:
                # if file NOT EXISTS - it creates!!!
                for line in lines:
                    line = str(line).strip("\n")
                    if self.TEXT:
                        line = f"\n{line}"

                    if file.write(line):
                        count += 1

                    self.TEXT += line
        return count

    def write__bytes(self, data: bytes) -> Optional[int]:
        if self.FILEPATH:
            self.ensure_dir()
            return self.FILEPATH.write_bytes(data=data)


# =====================================================================================================================
