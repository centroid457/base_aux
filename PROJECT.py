from base_aux.release.release_files import *


# =====================================================================================================================
# VERSION = (0, 0, 3)   # 1/deprecate _VERSION_TEMPLATE from PRJ object +2/place update_prj here in __main__ +3/separate finalize aux_attr
# VERSION = (0, 0, 4)   # add AUTHOR_NICKNAME_GITHUB for badges
# VERSION = (0, 0, 5)   # separate PROJECT_BASE #TODO: need to separate into module!
# VERSION = (0, 0, 6)   # group Ver+News just place together
VERSION = (0, 0, 7)     # move PRJBase into share +use Version


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
    ]

    # HISTORY -----------------------------------------------
    TODO: list[str] = [
        # "fix info content TREE",
    ]
    FIXME: list[str] = [
    ]
    # -----------------------------------------------------------------------------------------------------------------
    VERSION = Version((0, 3, 0))
    NEWS: list[str] = [
        ["THE BIG REF 2",
            "many renames/moves/regroups/deprecates",
         ],
        ["[GIT]",
            "finish = add recursive rootFind + add check_installed",
            "add DIRTY",
            "add UNTRACKED_FILES + check__status",
        ],
        ["[TPS]",
            "finish TpManager with TpItem",
            "GUI - add CBB zero",
            "GUI - add BTN_tm_update+apply switching tpItem without clearing results",
            "GUI - add TableModel_Devs",
            "GUI - TableModel_Devs show ADDRESS in table",
            "LEDS - add blink Yellow on test",
            "RESULTS save only for existed and presented - finish",
        ],
        ["[FileText]",
            "add pretty__json",
        ],
        ["[TableLine/lines/Columns]",
            "create+apply in Breeders/DevLines/TpItems..."
        ],
        ["[EqValid] big full ref!",
            "1/ use validator a simple func",
            "2/ place IRESULT_CUMULATE into base",
            "3/ separate other_final_calculate",
            "create EqRaise",
            "separate EqValidChain_All/Any",
        ],
        ["[Lambda]",
            "move in all methods from CallableAux(deprecated)",
        ],
        ["[Enums]",
            "separate to EnumAdj+Value",
        ],
        ["CREATE",
             "[EqArgs]",
             "[DictDiff]",
             "[StrIc]",
         ],
        "[Base_KwargsEqValid] deprecate old ReqCheckStr_Os",
        "[RaiseIf] move into ArgsAux + separate to ArgsBoolIf*",
        "[Version] combine VerChecker into Vertion!+add derivatives",
        "[Base_Exx] add autoPrint msg on init!",
        "[TYPING] collect many fro other places",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
