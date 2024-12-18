from typing import *


# =====================================================================================================================
class PROJECT:
    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "private_values"
    KEYWORDS: list[str] = [
        "environs", "environment",
        "private",
        "rc", "ini", "csv"
                     "json"
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "update values into class attrs from OsEnvironment or Ini/Json File"
    DESCRIPTION_LONG: str = """
    Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
    And not open it in public.  

    **CAUTION:**  
    in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.
    """
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["load values to instance attrs from",
         "Environment",
         "IniFile",
         "JsonFile",
         "CsvFile",
         "direct text instead of file",
         "direct dict instead of file",
         ],

        ["attr access",
         "via any lettercase",
         "by instance attr",
         "like dict key on instance", ],

        ["work with dict", "apply", "update", "preupdate"],

        "update_dict as cumulative result - useful in case of settings result",
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 6, 1)
    TODO: list[str] = [
        "add Lock param after load?"
    ]
    FIXME: list[str] = [
        "..."
    ]
    NEWS: list[str] = [
        "[pypi.init] add static =NOW IT IS NOT WORKING!!!"
    ]


# =====================================================================================================================
