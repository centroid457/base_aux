from typing import *
from share.release_files import release_files__update


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs
# VERSION = (0, 0, 4)   # add AUTHOR_NICKNAME_GITHUB for badges
# VERSION = (0, 0, 5)   # separate PROJECT_BASE #TODO: need to separate into module!
VERSION = (0, 0, 6)     # group Ver+News just place together


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
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "collect all my previous modules in one package"
    DESCRIPTION_LONG: str = """
"""
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],
    ]

    # HISTORY -----------------------------------------------
    TODO: list[str] = [
        "fix info content TREE",
    ]
    FIXME: list[str] = [
    ]
    # -----------------------------------------------------------------------------------------------------------------
    VERSION: tuple[int, int, int] = (0, 1, 5)
    NEWS: list[str] = [
        "[TP.gui.TV] add summary results footprint",
        "[TP.save_results] use short style",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
