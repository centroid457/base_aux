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
    VERSION = Version((0, 2, 25))
    NEWS: list[str] = [
        ["[pytest]",
            "add ini/settings file in root",
            "hide logs for caught Raises (like in Try sent)",
         ],
        "[Annots] add AttrAux_AnnotsLast =separate last/all nesting parents annotations +add Enum_AnnotsDepthAllOrLast",
        "[DictAux] separate to Base/DictAuxInline/Copy +add walk in keys_rename__by_func",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
