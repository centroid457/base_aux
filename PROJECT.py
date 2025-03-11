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
        "fix info content TREE",
    ]
    FIXME: list[str] = [
    ]
    # -----------------------------------------------------------------------------------------------------------------
    VERSION = Version((0, 2, 16))
    NEWS: list[str] = [
        "[TextFormated] create",
        "[ReAttempts] create",
        ["[Attrs+Annots]",
            "combine two classes finally in one",
            "add annots_ensure +annots__append",
            "separate NestRepr__ClsName_SelfStr",
        ],
        "[IterAux] add get_first_is_not_none",
        "[DateTime] add UPDATE_ON_STR+DEF_STR_FORMAT",

        ["[Nest*]",
            "add NestCall_Other",
            "add NestStR_AttrsPattern",
         ],
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
