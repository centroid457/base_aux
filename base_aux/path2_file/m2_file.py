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
    FILEPATH: TYPING.PATH_FINAL = None
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
        return self.FILEPATH and self.FILEPATH.exists()

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
    def read__text(self) -> Optional[str] | NoReturn:
        if self.FILEPATH.exists():
            if self.FILEPATH.is_file():
                self.TEXT = self.FILEPATH.read_text(encoding="utf-8")
                return self.TEXT
            else:
                raise Exx__Incompatible(f"{self.FILEPATH=}")

    def read__bytes(self) -> Optional[bytes]:
        if self.FILEPATH.exists() and self.FILEPATH.is_file():
            return self.FILEPATH.read_bytes()

    # WRITE ---------------------------------
    def write__text(self, _text: TYPING.STR_DRAFT = None) -> int:
        if _text is not None:
            self.TEXT = str(_text)
        self.ensure_dir()
        return self.FILEPATH.write_text(data=self.TEXT or "", encoding="utf-8")

    def append__text(self, text: TYPING.STR_DRAFT, new_line: bool = False) -> int | NoReturn:
        data = str(text)

        if data:
            self.ensure_dir()

            if self.TEXT and new_line:
                data = f"\n{data}"

            with open(file=self.FILEPATH, encoding="UTF-8", mode="a") as file:  # use exact append for large files!!!
                # if file NOT EXISTS - it creates!!!
                result = file.write(data)
                if result:
                    self.TEXT += data
                return result
        else:
            return True

    def append__lines(self, *lines: TYPING.STR_DRAFT) -> bool | NoReturn:
        data = "\n".join(map(str, lines))
        return bool(self.append__text(data, new_line=True))

    def write__bytes(self, data: bytes) -> Optional[int]:
        if self.FILEPATH:
            self.ensure_dir()
            return self.FILEPATH.write_bytes(data=data)


# =====================================================================================================================
