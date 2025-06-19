import pathlib

from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.aux_values.m2_typing import TYPING
from base_aux.path2_file.m2_file import FileAux

from base_aux.aux_text.m0_patterns import *


# =====================================================================================================================
class TextFile(FileAux, TextAux):
    """
    GOAL
    ----
    same as FileAux but with TextAux methods applied inplace!
    """
    def __init__(
            self,
            filepath: TYPING.PATH_DRAFT = None,
            text: TYPING.STR_DRAFT = None,
            # *args, **kwargs
    ) -> None | NoReturn:
        # super().__init__(*args, **kwargs)     # NOTE: dont use here!??? because init is overWriten here!

        if filepath is not None:
            self.FILEPATH = pathlib.Path(filepath)
        if self.check_exists() and not self.FILEPATH.is_file():
            raise Exx__Incompatible(f"{self.FILEPATH=}")

        if text is not None:
            self.TEXT = str(text)
        else:
            if self.check_exists():
                self.read__text()


# =====================================================================================================================
