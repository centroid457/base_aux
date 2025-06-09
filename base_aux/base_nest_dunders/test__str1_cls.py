from typing import *

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *

from base_aux.base_nest_dunders.m2_str1_cls import *


# =====================================================================================================================
class VictimBare:
    STR: str

    def __init__(self, STR):
        self.STR = str(STR)


class VictimMod(NestStRCls_ClsName):
    STR: str

    def __init__(self, STR):
        self.STR = str(STR)

    def __str__(self) -> str:
        return self.STR

    def __repr__(self) -> str:
        return str(self)


# =====================================================================================================================
class Test__StrCls:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (VictimBare, EqValid_RegexpAnyTrue(r"<class '.*\.VictimBare'>")),
            (VictimBare(1), EqValid_RegexpAnyTrue(r"<.*\.VictimBare object at 0x.*>")),

            (VictimMod, "VictimMod"),
            (VictimMod(1), "1"),
        ]
    )
    def test__inst__cmp__lg(self, source, _EXPECTED):
        ExpectAux(str(source)).check_assert(_EXPECTED)
        ExpectAux(repr(source)).check_assert(_EXPECTED)


# =====================================================================================================================

