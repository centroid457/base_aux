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

"""

import pathlib


file = pathlib.Path(__file__, "..", "nouns5rus.txt")
text = file.read_text(encoding="utf8").lower()

words: set[str] = set(text.split())

lacks_source: str = """
АБОРТ
АВТОР
АГЕНТ
АДРЕС
АКРИЛ
АКТЕР
АКТИВ
АКУЛА
АЛИБИ
АЛМАЗ
АЛЬФА
АНГЕЛ
АНИМЕ
АРБУЗ
АРЕНА
АРМИЯ
АРХИВ
АСКОТ
АТАКА
АТЛАС
АУДИТ
АШРАМ
""".lower()

lacks_words = lacks_source.split()
for test in lacks_words:
    if test not in words:
        print(test)

