from base_aux.aux_dict.m4_dict_diff import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
class Base_AttrDiff(Base_DiffResolve):
    """
    GOAL
    ----
    cmp several objects by attr values.
    MAIN GOAL - cmp several states of one obj after DumpAttrObj.
        but it seems cant be realisable! cause we cant use at same time/in one code line several states for one object!
    so
        1/ for one object - use state dumps with DictDiff
        2/ for several identical objects - use this staff! AttrDiff

    SPECIALLY CREATED FOR
    ---------------------
    """
    ARGS: tuple[Any, ...]
    DIFF: TYPING.DICT_STR_TUPLE_ANY
    __diff: TYPING.DICT_STR_TUPLE_ANY

    CLS_ATTR_DUMPING: type[Base_AttrDictDumping] = AttrDictDumping_Existed

    def resolve(self) -> TYPING.DICT_STR_TUPLE_ANY:
        DICTS = []
        for obj in self.ARGS:
            dict_i = self.CLS_ATTR_DUMPING(obj).resolve()
            DICTS.append(dict_i)

        self.__diff = DictDiff(*DICTS).resolve()
        return self.__diff


# =====================================================================================================================
class AttrDiff_Existed(Base_AttrDiff):
    CLS_ATTR_DUMPING: type[Base_AttrDictDumping] = AttrDictDumping_Existed


class AttrDiff_AnnotsAll(Base_AttrDiff):
    CLS_ATTR_DUMPING: type[Base_AttrDictDumping] = AttrDictDumping_AnnotsAll


class AttrDiff_AnnotsLast(Base_AttrDiff):
    CLS_ATTR_DUMPING: type[Base_AttrDictDumping] = AttrDictDumping_AnnotsLast


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
