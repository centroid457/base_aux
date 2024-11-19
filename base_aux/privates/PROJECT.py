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
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
