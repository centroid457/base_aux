from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_enums.m2_enum1_adj import *


# =====================================================================================================================
class Base_AttrDictDumping(NestInit_Source, NestCall_Resolve):
    """
    GOAL
    ----
    separate object to make only one thing - dumping attrs final state
    for exploring objects

    SPECIALLY CREATED FOR
    ---------------------
    replace ObjectInfo State with attrsGroups to simple flat name-value
    for make simplified comparing several states
    """
    SOURCE: Any
    SKIP_NAMES: tuple[str | Base_EqValid, ...]

    _ATTRS_STYLE: EnumAdj_AttrAnnotsOrExisted = EnumAdj_AttrAnnotsOrExisted.ATTRS_EXISTED
    _ANNOTS_DEPTH: EnumAdj_AnnotsDepthAllOrLast = EnumAdj_AnnotsDepthAllOrLast.ALL_NESTED

    def __init__(self, source: Any = NoValue, *skip_names: str | Base_EqValid) -> None:
        super().__init__(source)
        self.SKIP_NAMES = skip_names

    def resolve(self) -> dict[str, Any | Exception] | NoReturn:
        # select -----
        result_obj = None

        if self._ATTRS_STYLE == EnumAdj_AttrAnnotsOrExisted.ATTRS_EXISTED:
            result_obj = AttrAux_Existed(self.SOURCE, *self.SKIP_NAMES)
        elif self._ATTRS_STYLE == EnumAdj_AttrAnnotsOrExisted.ANNOTS_ONLY:
            if self._ANNOTS_DEPTH == EnumAdj_AnnotsDepthAllOrLast.ALL_NESTED:
                result_obj = AttrAux_AnnotsAll(self.SOURCE, *self.SKIP_NAMES)
            elif self._ANNOTS_DEPTH == EnumAdj_AnnotsDepthAllOrLast.LAST_CHILD:
                result_obj = AttrAux_AnnotsLast(self.SOURCE, *self.SKIP_NAMES)
        else:
            raise Exx__Incompatible(f"{self._ATTRS_STYLE=}/{self._ANNOTS_DEPTH=}")

        # result -----
        return result_obj.dump_dict()


# ---------------------------------------------------------------------------------------------------------------------
@final
class AttrDictDumping_Existed(Base_AttrDictDumping):
    """
    NOTE
    ----
    main class! most used
    next derivatives is not useful i think!
    """
    _ATTRS_STYLE: EnumAdj_AttrAnnotsOrExisted = EnumAdj_AttrAnnotsOrExisted.ATTRS_EXISTED
    _ANNOTS_DEPTH: EnumAdj_AnnotsDepthAllOrLast = EnumAdj_AnnotsDepthAllOrLast.ALL_NESTED


@final
class AttrDictDumping_AnnotsAll(Base_AttrDictDumping):
    _ATTRS_STYLE: EnumAdj_AttrAnnotsOrExisted = EnumAdj_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: EnumAdj_AnnotsDepthAllOrLast = EnumAdj_AnnotsDepthAllOrLast.ALL_NESTED


@final
class AttrDictDumping_AnnotsLast(Base_AttrDictDumping):
    _ATTRS_STYLE: EnumAdj_AttrAnnotsOrExisted = EnumAdj_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: EnumAdj_AnnotsDepthAllOrLast = EnumAdj_AnnotsDepthAllOrLast.LAST_CHILD


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
