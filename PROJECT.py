from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs
# VERSION = (0, 0, 4)   # add AUTHOR_NICKNAME_GITHUB for badges
VERSION = (0, 0, 5)     # separate PROJECT_BASE #TODO: need to separate into module!


# =====================================================================================================================
class PROJECT_BASE:
    NAME_IMPORT: str
    VERSION: tuple[int, int, int]

    # AUTHOR ------------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"
    AUTHOR_NICKNAME_GITHUB: str = "centroid457"

    # AUX ----------------------------------------------------
    CLASSIFIERS_TOPICS_ADD: list[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # FINALIZE -----------------------------------------------
    @classmethod
    @property
    def VERSION_STR(cls) -> str:
        return ".".join(map(str, cls.VERSION))

    @classmethod
    @property
    def NAME_INSTALL(cls) -> str:
        return cls.NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
class PROJECT(PROJECT_BASE):
    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "base_aux"
    KEYWORDS: list[str] = [
        "funcs_aux",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "collect all previous moduls in one package"
    DESCRIPTION_LONG: str = """
    
"""
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        # classes_aux
        "cmp - apply for cmp object with others",
        "getattr prefix",
        "getattr echo",
        "middle group",
        "Number+NumberArithm - use class as number",
        "Annotations - work with annotations +use special abilities+use nested classes",

        # singleton
        "perfect singleton (maybe thread safe!)",
        "collect all instances",
        "check correct instantiating singletons in tree project",
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 0, 0)
    TODO: list[str] = [
        "[Valid*/Value*] ref/make all nested from VALID!!!",
    ]
    FIXME: list[str] = [
        "..."
    ]
    NEWS: list[str] = [
        "[classes_aux]move here",

    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
