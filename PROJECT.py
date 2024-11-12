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

        # classes
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

        # requirements
        "check requirements (systemOs), raise/bool if no match",
        "create fuck(?)/source and is it for check for settings",
        ["[python PACKAGES/MODULES]", "upgrade", "delete", "version_get_installed", "check_installed)", "upgrade pip"],
        ["[VERSION]",
         "parse",
         "check",
         "compare",
         ],

        # cli
        "send commands into OS terminal",
        "check if cli commands are accessible (special utilities is installed)",
        "access to standard parts of result in a simple ready-to-use form (stdout/stderr/retcode/full state)",
        "use batch timeout for list",
        "till_first_true",
        "counter/counter_in_list",

        # bits
        "designed for common work with bitfields-like objects",
        "Flags",
        "Bits",

        # privates
        """
        Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
        And not open it in public.  
    
        **CAUTION:**  
        in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.
        """,

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

        # threads
        "use different managers for different funcs/methods if needed",
        "use just one decorator to spawn threads from func / methods",
        "keep all spawned threads in list by ThreadItem objects",
        "ThreadItem keeps result/exx/is_alive attributes!",
        "use wait_all/terminate_all()",

        # servers
        ["[SERVERS]",
         "[aiohttp] (try not to use, as old)",
         "[FastApi] (preferred)",
         ],
        "client_requests item+stack",

        # buses
        ["[SerialClient]",
         "keep all found ports in base class!",
         ],
        ["Serial",
         "Client+Server",
         "connect with Type__AddressAutoAcceptVariant FIRST_FREE/FIRST_FREE__ANSWER_VALID",
         "set/get params by SlashOrSpacePath addressing",
         "handle BackSpace send manually from terminal",
         ],
        ["SerialServer values",
         "as Callable",
         "ValueUnit",
         "ValueVariants",
         "list_results",
         ],
        ["SerialServer cmd",
         "NONE is equivalent for SUCCESS",
         "no need params (like line_parsed as before)",
         "help - for show all variants (Units/Variants/Callables)!"
         ],

        # monitors
        "Threading each monitor",

        ["monitor",
         "website data changes (tag text/attribute)",
         "email received with subject (by regexp) in exact folder", ],

        ["Email/Telegram alert if",
         "monitored data changed (from last state)",
         "html structure was changed so parsing can't be finished",
         "url became unreachable", ],

        # alerts
        ["send alert msgs", "emails", "telegram",],
        "threading",

        # pyqt
        "pyqt help examples and some other useful objects (overloaded pyqt classes)",
        "good template for TableView/Model/Signals",
        "add Events for TM/TV/PTE/...",
    ]

    # HISTORY -----------------------------------------------
    TODO: list[str] = [
        "fix info content TREE",

    ]
    FIXME: list[str] = [
    ]

    # -----------------------------------------------------------------------------------------------------------------
    VERSION: tuple[int, int, int] = (0, 0, 15)
    NEWS: list[str] = [
        "[DictDotsAnnotRequired] add",
        "[_SAND] create and add first content",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
