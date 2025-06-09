import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_values.m4_primitives import *

from base_aux.aux_eq.m2_eq_aux import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, args, _EXPECTED",
    argvalues=[
        (1, 1,              (True, True, False,     True, True, False)),
        (1, 2,              (False, False, True,    False, False, True)),
        (LAMBDA_TRUE, True, (False, False, True,    False, False, True)),

        # __EQ__=in single obj!
        (ClsEq(1), 1,       (True, True, False,     True, True, False)),
        (ClsEq(1), 2,       (False, False, True,    False, False, True)),
        (1, ClsEq(1),       (True, True, False,    True, True, False)),
        (2, ClsEq(1),       (False, False, True,    False, False, True)),

        (INST_EQ_RAISE, 1,  (Exception, False, True,    Exception, False, True)),
        (1, INST_EQ_RAISE,  (Exception, False, True,    Exception, False, True)),

        # __EQ__=in both objs!
        (INST_EQ_TRUE, INST_EQ_FALSE, (True, True, False,   True, True, False)),
        (INST_EQ_FALSE, INST_EQ_TRUE, (False, False, True,  True, True, False)),

    ]
)
def test__eq_aux(source, args, _EXPECTED):
    ExpectAux(EqAux(source).check_oneside__exx, args).check_assert(_EXPECTED[0])
    ExpectAux(EqAux(source).check_oneside__bool, args).check_assert(_EXPECTED[1])
    ExpectAux(EqAux(source).check_oneside__reverse, args).check_assert(_EXPECTED[2])

    ExpectAux(EqAux(source).check_doubleside__exx, args).check_assert(_EXPECTED[3])
    ExpectAux(EqAux(source).check_doubleside__bool, args).check_assert(_EXPECTED[4])
    ExpectAux(EqAux(source).check_doubleside__reverse, args).check_assert(_EXPECTED[5])


# =====================================================================================================================
