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
    NAME_IMPORT: str = "object_info"
    KEYWORDS: list[str] = [
        "object info",
        "object attributes", "object properties", "object methods",
        "print attributes", "print properties", "print methods",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "print info about object (attributes+properties+methods results)"
    DESCRIPTION_LONG: str = """
Designed to print info about object (properties+methods results)

But why? if we can use debugger directly?  
Reason:  
1. to get and save standard text info,  
it useful to keep this info for future quick eye sight without exact condition like other OS or device/devlist/configuration 
2. in debugger we cant see result of methods!  
try to see for example information from platform module! it have only methods and no one in object tree in debugger!  
```python
import platform

obj = platform
print(platform.platform())
pass    # place debug point here
```  
3. Useful if you wish to see info from remote SOURCE if connecting directly over ssh for example  
    """
    FEATURES: list[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "print all properties/methods results",
        "show exceptions on methods/properties",
        "skip names by full/part names and use only by partnames",
        "separated collections by groups",
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 2, 20)
    TODO: list[str] = [
        "add TIMEOUT (use start in thread!) for print! use timeout for GETATTR!!!",
        [
            "realise PRINT_DIFFS=CHANGE_state/COMPARE_objects (one from different states like thread before and after start)!",
            "this is about to save object STATE!",
            "add parameter show only diffs or show all",
            "add TESTS after this step!",
        ],
        "apply asyncio.run for coroutine?",
        "merge items Property/Meth? - cause it does not matter callable or not (just add type info block)",

        "add check__instance_of_user_class",
    ]
    FIXME: list[str] = [
        "..."
    ]
    NEWS: list[str] = [
        "add TYPE__NONE/func/meth",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
