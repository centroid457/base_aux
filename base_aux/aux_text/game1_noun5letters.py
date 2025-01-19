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
if __name__ == "__main__":
    check_lack_words()


# =====================================================================================================================
