from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_statics.m4_enums import *


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

    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ATTRS_EXISTED
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.ALL_NESTED

    def __init__(self, source: Any = NoValue, *skip_names: str | Base_EqValid) -> None:
        super().__init__(source)
        self.SKIP_NAMES = skip_names

    def resolve(self) -> dict[str, Any | Exception] | NoReturn:
        # select -----
        result_obj = None

        if self._ATTRS_STYLE == Enum_AttrAnnotsOrExisted.ATTRS_EXISTED:
            result_obj = AttrAux(self.SOURCE, *self.SKIP_NAMES)
        elif self._ATTRS_STYLE == Enum_AttrAnnotsOrExisted.ANNOTS_ONLY:
            if self._ANNOTS_DEPTH == Enum_AnnotsDepthAllOrLast.ALL_NESTED:
                result_obj = AnnotsAllAux(self.SOURCE, *self.SKIP_NAMES)
            elif self._ANNOTS_DEPTH == Enum_AnnotsDepthAllOrLast.LAST_CHILD:
                result_obj = AnnotsLastAux(self.SOURCE, *self.SKIP_NAMES)
        else:
            raise Exx__Incompatible(f"{self._ATTRS_STYLE=}/{self._ANNOTS_DEPTH=}")

        # result -----
        return result_obj.dump_dict()


# ---------------------------------------------------------------------------------------------------------------------
@final
class AttrDictDumping(Base_AttrDictDumping):
    """
    NOTE
    ----
    main class! most used
    next derivatives is not useful i think!
    """
    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ATTRS_EXISTED
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.ALL_NESTED


@final
class AnnotsAllDictDumping(Base_AttrDictDumping):
    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.ALL_NESTED


@final
class AnnotsLastDictDumping(Base_AttrDictDumping):
    _ATTRS_STYLE: Enum_AttrAnnotsOrExisted = Enum_AttrAnnotsOrExisted.ANNOTS_ONLY
    _ANNOTS_DEPTH: Enum_AnnotsDepthAllOrLast = Enum_AnnotsDepthAllOrLast.LAST_CHILD


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
from base_aux.aux_expect.m1_expect_aux import *


class VictimAt:
    at1 = 1
    _at1 = 11
    __at1 = 111


class VictimAn:
    an2: int = 2
    _an2: int = 22
    __an2: int = 222


class VictimAnNest(VictimAn):
    an3: int = 3
    _an3: int = 33
    __an3: int = 333


@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (VictimAt(), [], [{"at1": 1, "_at1": 11}, {}, {}]),
        (VictimAn(), [], [{"an2": 2, "_an2": 22}, {"an2": 2, "_an2": 22}, {"an2": 2, "_an2": 22}]),
        (VictimAnNest(), [], [{"an2": 2, "_an2": 22, "an3": 3, "_an3": 33}, {"an2": 2, "_an2": 22, "an3": 3, "_an3": 33}, {"an3": 3, "_an3": 33}]),
    ]
)
def test__names(source, skip_names, _EXPECTED):
    ExpectAux(AttrDictDumping(source)(*skip_names)).check_assert(_EXPECTED[0])
    ExpectAux(AnnotsAllDictDumping(source)(*skip_names)).check_assert(_EXPECTED[1])
    ExpectAux(AnnotsLastDictDumping(source)(*skip_names)).check_assert(_EXPECTED[2])


# =====================================================================================================================
