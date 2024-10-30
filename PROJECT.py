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
    NAME_IMPORT: str = "base_aux"
    KEYWORDS: list[str] = [
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "collect all previous moduls in one package"
    DESCRIPTION_LONG: str = """
    
    buses
    --------------
NOTE: IT SEEMS THIS IS OLD DATA! see tests for actual usage!
    
!. MOST APPROPRIATE COMMAND PROTOCOL
other protocols mot recommended

1. all cmds must be as params (preferred) in equipment or as special command
2. [<CMD_NAME>] - read param value or run special command  
    [IDN] - read value IDN  
    [DUMP] - run special command 
3. [<CMD_NAME> <VALUE>] - write value in parameter or run special cmd with param  
    [VOUT 12.3] - set value into parameter VOUT  
4. [<CMD_NAME> ?] - get available values to write into parameter  
    [MODE ?] - return [0 1 2 3]
5. all command sent must return answer  
    [OK] - if no value was asked
    [<VALUE>] - if asked some value, returned without measurement unit
    [FAIL] - any common not specified error
    [FAIL 0123] - any specified error without description
    [FAIL 02 VALUE OUT OF RANGE] - any specified error with description (full variant)
    
    
    
    monitors
    --------------
    monitor exact data (urlTag/Email) and alert on changes by email/telegram (threading)
    ## IMPORTANT!
    NOT ALL WEBSITES WORKS! Sportmaster/Acra-rating/...

    ## INSPIRATION
    Suppose you wish to give blood to the Center.
    So nowadays you need to make an appointment by website, BUT you can't do this while the Center actually don't need your group.
    Group necessity shown on Center website and called DonorSvetofor.
    And as result you need monitoring it manually, because there are no news, email notifications, subscriptions.
    It's not difficult but if you do it as day routine (even once a day) its quite distracting.

    So I created it first as Monitor_DonorSvetofor
    
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

        # private_values
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
    ]

    # HISTORY -----------------------------------------------
    VERSION: tuple[int, int, int] = (0, 0, 0)
    TODO: list[str] = [
        # classes
        "create class with autoInit params from ATTRS",
        "[Valid*/Value*] ref/make all nested from VALID!!!",

        # objects
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

        # requirements
        "add check_file",

        # threads
        "add SERIAL execution as method wait_all_piped! paired up with wait_all_parallel()",
        "add meta cumulative funks",
        "add GROUP threads - in decorator+wait+...",
        "maybe AUTO CLEAR if decorator get new funcName?",
        "TIME item+group",

        # monitors
        ["monitors",
            "check requirement for python version!",
            "csv.reader(ofilepath, delimiter=self.CSV_DELIMITER)",
            "module 'private_values.csv' has no attribute 'reader'"
         ],

        # alerts
        "TODO test multyStart by one object (QThread)",
        "FIX NEED SOLVE ABILITY to work without PV.FILE!!! as just a http client",

    ]
    NEWS: list[str] = [
        "[ALL MODULES] move here",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files_update(PROJECT)


# =====================================================================================================================
