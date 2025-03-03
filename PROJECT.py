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
    VERSION = Version((0, 2, 14))
    NEWS: list[str] = [
        "[ini] add ConfigParserMod",
        "[AttrKit] add",
        [
            "[Text]",
                "add parse__dict_ini",
                "fix__json/parse__json",
                "add delete__cmts_c",
                "add search__group - need fix",
         ],
        "[TextFile] add DictTextFileLoader",
        "[NestInit_AttrsLambdasResolve] use with Resolvers",
        ["[Nest*_Attrs]",
            "separate all for Attrs Contains/Eq/Len/StR",
            "[NestSAI_AttrAnycase] deprecate all Setattrs* cause recursion exx",

         ],
        ["[EqValid]",
            "add EqValid_AnnotsAllExists",
            "add EqValid_AttrsByObjNotPrivate*",
         ],
        "[PV] deprecate old and add new PvLoaderIni/json/env",
        "[Kwargs] ref to simple dict nesting",

    ]


# =====================================================================================================================
if __name__ == '__main__':
    release_files__update(PROJECT)


# =====================================================================================================================
