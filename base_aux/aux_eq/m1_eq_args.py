from typing import *
import pytest

from base_aux.base_nest_dunders.m1_init0_args_kwargs import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.base_statics.m3_primitives import *
from base_aux.aux_expect.m1_expect_aux import ExpectAux


# =====================================================================================================================
@final
class EqArgs(NestInit_Args_Implicit, NestCall_Resolve):
    """
    GOAL
    ----
    return True if all Args equal (with first arg)
    """
    def resolve(self) -> bool | NoReturn:
        # only one chans for Raise - not enough count --------------
        if len(self.ARGS) < 2:
            msg = f"need at least 2 args {self.ARGS=}"
            raise Exx__WrongUsage(msg)

        arg_0 = self.ARGS[0]

        # any raise on comparisons - return False! --------------
        for arg_next in self.ARGS[1:]:
            try:
                if arg_0 != arg_next:
                    return False
            except:
                return False

        return True


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ((), Exception),
        ((1, ), Exception),
        ((1, 1), True),
        ((1, 1, 1, 1), True),

        ((1, 1, 1, 11), False),
        ((1, 1, 11, 1), False),
        ((1, INST_EQ_RAISE), False),
        ((1, INST_EQ_FALSE), False),
        ((1, INST_EQ_TRUE), True),
    ]
)
def test__1(args, _EXPECTED):
    ExpectAux(EqArgs(*args)).check_assert(_EXPECTED)


# =====================================================================================================================
