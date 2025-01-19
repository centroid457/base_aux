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
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_attr.m2_annot5_init import *


# =====================================================================================================================
def check_lack_words() -> None:
    applicants: list[str] = """
проверка_СТАРТ 

ЯГОДА
ЯГУАР

проверка_ФИНИШ
    """.lower().split()

    file = pathlib.Path(__file__, "..", "nouns5rus.txt")
    text = file.read_text(encoding="utf8").lower()

    words: set[str] = set(TextAux(text).get_lines(True))

    for item in applicants:
        if item and item not in words:
            print(item)


# =====================================================================================================================
@final
class CharMask(AnnotsInitByTypes_NotExisted):
    # HIDDEN: str
    # ATTEMPTS: list[str]
    POS: list[str]
    INCL: set[str]
    EXCL: set[str]

    def __init__(self, length: int):
        super().__init__()
        self.POS = ["", ] * length

    @property
    def POS_WM(self) -> str:
        result = ""
        for pos in self.POS:
            if not pos:
                pos = "*"
            result += pos
        return result

    def __str__(self):
        incl = f"[{''.join(self.INCL)}]"
        excl = f"[{''.join(self.EXCL)}]"
        return f"{self.__class__.__name__}({self.POS_WM},{incl=},{excl=})"


# ---------------------------------------------------------------------------------------------------------------------
class FilterMask(InitSourceKwArgs_Implicite):
    SOURCE: str
    ARGS: tuple[str]    # ATTEMPTS

    CHARMASK: CharMask

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.get_mask()

    def get_mask(self) -> CharMask:
        self.CHARMASK = CharMask(5)
        self.CHARMASK.HIDDEN = self.SOURCE
        # result = CharMask(5)
        for attempt in self.ARGS:
            self.attemtp_apply(attempt)

        return self.CHARMASK

    def attemtp_apply(self, word: str) -> None:
        for index, char_i in enumerate(word):
            # POS ------
            if self.SOURCE[index] == char_i:
                self.CHARMASK.POS[index] = char_i

            # HAVE ------
            if char_i in self.SOURCE:
                self.CHARMASK.INCL.update(char_i)
            else:
                self.CHARMASK.EXCL.update(char_i)


# ---------------------------------------------------------------------------------------------------------------------
def check_mask() -> None:
    pass


# =====================================================================================================================
if __name__ == "__main__":
    check_lack_words()


# =====================================================================================================================
