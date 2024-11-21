from typing import *


# =====================================================================================================================
class PROJECT:
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
