"""
GAME
----

https://wordleplay.com/ru/octordle
https://wordleplay.com/ru/wordle-solver

CODE REALIZASIONS
-----------------
https://habr.com/ru/articles/818883/


WORDS source
------------
https://github.com/cwaterloo/5bukv/blob/main/russian5.txt   -5letters for exact game
https://gist.github.com/kissarat/bd30c324439cee668f0ac76732d6c825   -all counts (notFull!!!)

NOTE
----
how to find new words

1/ MANUALLY
find combinations
split groupes by first letter
check by this code
"""

import pathlib
from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.base_nest_dunders.m1_init2_annots2_by_types import *


# =====================================================================================================================
def check_lack_words() -> None:
    applicants: list[str] = """
проверка_СТАРТ 

ЯГОДА
ЯГУАР

проверка_ФИНИШ
    """.lower().split()

    file = pathlib.Path(__file__, "..", "game1_nouns5rus.txt")
    text = file.read_text(encoding="utf8").lower()

    words: set[str] = set(TextAux(text).split_lines(True))

    for item in applicants:
        if item and item not in words:
            print(item)


# =====================================================================================================================
@final
class CharMask(NestInit_AnnotsByTypes_NotExisted):
    # HIDDEN: str
    # ATTEMPTS: list[str]
    POS_DET: list[str]
    POS_EXCL: list[set[str]]
    INCL: set[str]
    EXCL: set[str]

    def __init__(self, length: int):
        super().__init__()
        self.POS_DET = ["", ] * length
        self.POS_EXCL = [set(), ] * length

    @property
    def POS_DET_WM(self) -> str:
        result = ""
        for pos in self.POS_DET:
            if not pos:
                pos = "?"
            result += pos
        return result

    def __str__(self):
        INCL = f"[{''.join(self.INCL)}]"
        EXCL = f"[{''.join(self.EXCL)}]"
        POS_EXCL = str(self.POS_EXCL).replace(" ", "")
        return f"{self.__class__.__name__}({self.POS_DET_WM},{POS_EXCL},{INCL=},{EXCL=})"


# ---------------------------------------------------------------------------------------------------------------------
class FilterMask(NestInit_SourceKwArgs_Implicit):
    SOURCE: str
    ARGS: tuple[str, ...]    # ATTEMPTS

    CHARMASK: CharMask

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.get_mask()

    def get_mask(self) -> CharMask:
        self.CHARMASK = CharMask(5)
        # self.CHARMASK.HIDDEN = self.SOURCE
        # result = CharMask(5)
        for attempt in self.ARGS:
            self.attemtp_apply(attempt)

        return self.CHARMASK

    def attemtp_apply(self, attempt: str) -> None:
        for index, char_i in enumerate(attempt):
            if char_i in self.SOURCE:
                self.CHARMASK.INCL.update(char_i)

                if self.SOURCE[index] == char_i:
                    self.CHARMASK.POS_DET[index] = char_i
                else:
                    self.CHARMASK.POS_EXCL[index].update(char_i)
            else:
                self.CHARMASK.EXCL.update(char_i)


# ---------------------------------------------------------------------------------------------------------------------
def check_mask() -> None:
    pass


# =====================================================================================================================
if __name__ == "__main__":
    check_lack_words()


# =====================================================================================================================
