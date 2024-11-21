from typing import *


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "logger_aux"
    KEYWORDS: List[str] = [
        "logger",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "simple logging"
    DESCRIPTION_LONG: str = """designed for DRY simple/easy usage logging"""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "keep all mostly used code in hidden class",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 0, 11)
    TODO: List[str] = [
        "..."
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "fix annotation for LOGGER"
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
