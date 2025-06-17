from base_aux.aux_dict.m1_dict_aux import *
from base_aux.aux_dict.m4_dict_diff import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *


# =====================================================================================================================
class Base_AttrDiff(Base_DiffResolve):
    """
    GOAL
    ----
    cmp several objects by attr values.
    usually cmp several states of one obj after DumpAttrObj.

    SPECIALLY CREATED FOR
    ---------------------
    """
    ARGS: tuple[Any, ...]
    CLS_ATTR_DUMPING: type[Base_AttrDictDumping] = AttrDictDumping_Existed

    def resolve(self) -> TIPING__DICT_DIFF:
        DICTS = []
        for obj in self.ARGS:
            dict_i = self.CLS_ATTR_DUMPING(obj).resolve()
            DICTS.append(dict_i)

        self.__diff = DictDiff(*DICTS).resolve()
        return self.__diff


# =====================================================================================================================
class AttrDiff_Existed(NestCall_Resolve):
    CLS_ATTR_COLLECT: type[Base_AttrDictDumping] = AttrDictDumping_Existed


class AttrDiff_AnnotsAll(NestCall_Resolve):
    CLS_ATTR_COLLECT: type[Base_AttrDictDumping] = AttrDictDumping_AnnotsAll


class AttrDiff_AnnotsLast(NestCall_Resolve):
    CLS_ATTR_COLLECT: type[Base_AttrDictDumping] = AttrDictDumping_AnnotsLast


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
