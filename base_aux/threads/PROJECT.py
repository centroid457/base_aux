from typing import *
from _aux__release_files import release_files_update


# =====================================================================================================================
VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize attrs


# =====================================================================================================================
class PROJECT:
    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "threading_manager"
    KEYWORDS: List[str] = [
        "threading", "threads", "thread",
        "thread manager",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "manage spawned threads"
    DESCRIPTION_LONG: str = """
    Designed to working with spawned threads

    NOTE: maybe you dont need use it if you need only one class method - use direct QThread
    """
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "use different managers for different funcs/methods if needed",
        "use just one decorator to spawn threads from func / methods",
        "keep all spawned threads in list by ThreadItem objects",
        "ThreadItem keeps result/exx/is_alive attributes!",
        "use wait_all/terminate_all()",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 0, 9)
    TODO: List[str] = [
        "add SERIAL execution as method wait_all_piped! paired up with wait_all_parallel()",
        "add meta cumulative funks",
        "add GROUP threads - in decorator+wait+...",
        "maybe AUTO CLEAR if decorator get new funcName?",
        "TIME item+group",
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "[__INIT__.py] fix import",
        "apply last pypi template",
    ]

    # FINALIZE -----------------------------------------------
    VERSION_STR: str = ".".join(map(str, VERSION))
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
