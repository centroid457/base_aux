from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs
VERSION = (0, 0, 4)     # add AUTHOR_NICKNAME_GITHUB for badges


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"
    AUTHOR_NICKNAME_GITHUB: str = "centroid457"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "cli_user"
    KEYWORDS: List[str] = [
        "cli", "cli user", "cli sender",
        "os terminal", "os terminal sender", "os terminal user",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "send commands into system terminal"
    DESCRIPTION_LONG: str = """
    Designed to send commands into OS terminal
        """
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "send commands into OS terminal",
        "check if cli commands are accessible (special utilities is installed)",
        "access to standard parts of result in a simple ready-to-use form (stdout/stderr/retcode/full state)",
        "use batch timeout for list",
        "till_first_true",
        "counter/counter_in_list",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 1, 3)
    TODO: List[str] = [
        "..."
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "fix linux tests"
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
