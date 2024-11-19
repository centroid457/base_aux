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
    NAME_IMPORT: str = "requirements_checker"
    KEYWORDS: list[str] = [
        "check requirements", "raise/bool if no requirements",
        "check system requirements",
        "python packages/modules aux (upgrade/delete/version get)",
        "version parse", "version check", "version compare",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "check if requirements met"
    DESCRIPTION_LONG: str = """
designed for check requirements (systemOs) and raise/bool if no match
    """
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "check requirements (systemOs), raise/bool if no match",
        "create fuck(?)/source and is it for check for settings",
        ["[python PACKAGES/MODULES]", "upgrade", "delete", "version_get_installed", "check_installed)", "upgrade pip"],
        ["[VERSION]",
            "parse",
            "check",
            "compare",
        ],
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 2, 18)
    TODO: list[str] = [
        "add WARN_if__*/if_not__* (and use message in stderr)",
        "add check_file"
    ]
    FIXME: list[str] = [
        "sometimes modules have incorrect SHARE!!! maybe need check upgrade after installation!!! and show ERROR!",
        "FIX TESTS!"
    ]
    NEWS: list[str] = [
        "[Pkg] add check_prj_installed_latest +apply in upgrade_prj+share",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
