from typing import *

from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.path2_file.m2_file import FileAux

from base_aux.base_statics.m1_types import *
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
        self.FILEPATH = pathlib.Path(filepath)
        if self.check_exists():
            if self.FILEPATH.is_file():
                self.read__text()
            else:
                raise Exx__Incompatible(f"{self.FILEPATH=}")

        if text is not None:
            self.TEXT = str(text)

        # super().__init__(*args, **kwargs)     # NOTE: dont use here!


# =====================================================================================================================
