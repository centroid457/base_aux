from base_aux.aux_eq.m1_eq_args import *
from base_aux.aux_dict.m1_dict_aux import *
from base_aux.aux_dict.m4_dict_diff import *
from base_aux.aux_attr.m4_dump_dumping import *


# =====================================================================================================================
# TIPING__ATTR_DIFF = dict[Any, tuple[Any, ...]]


# =====================================================================================================================
class Base_AttrDiff(NestCall_Resolve):
    """
    # GOAL
    # ----
    # get diffs from several states,
    # dicts assumed like AttrDumped objects - so keys are STR.
    #
    # NOTE
    # ----
    # if values is ExceptionNested - apply only class!!! for both cls and inst - so next cmparing would cmp only exact classes!
    # and same classes will be equal
    #
    # SPECIALLY CREATED FOR
    # ---------------------
    # cmp two objects by attr values
    """
    OBJS: tuple[Any, ...]
    DIFF: TIPING__DICT_DIFF
    __diff: TIPING__DICT_DIFF = {}

    CLS_ATTR_COLLECT: type[Base_AttrDictDumping] = AttrDictDumping_Existed

    def __init__(self, *objs: Any):
        self.OBJS = objs

    def resolve(self) -> TIPING__DICT_DIFF:
        DICTS = []
        for obj in self.OBJS:
            dict_i = self.CLS_ATTR_COLLECT(obj).resolve()
            DICTS.append(dict_i)

        self.__diff = DictDiff(*DICTS).resolve()
        return self.__diff

    def __bool__(self) -> bool:
        """
        GOAL
        ----
        answer the question - "Are dicts have diffs?":
            TRUE - if Diffs exists! (it looks from class name!)
            False - if NO Diffs!
        """
        return bool(self.DIFF)

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def DIFF(self) -> TIPING__DICT_DIFF:
        """
        GOAL
        ----
        if not exists __diff value - resolve it!
        """
        if not self.__diff:
            self.resolve()
        return self.__diff

    def __str__(self) -> str:
        """
        GOAL
        ----
        print pretty result
        """
        return DictAuxInline(self.DIFF).pretty_str()


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
