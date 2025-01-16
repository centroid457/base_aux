import pytest

from base_aux.base_objects.m0_primitives import *
from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_argskwargs.m2_argskwargs_aux import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ((), ()),
        ([], ()),
        ({}, ()),

        ((1,), (1,)),
        ([1, ], (1,)),
        ({1: 1}, (1,)),

        # None --------------
        (None, (None,)),
        ((None,), (None,)),

        ((None, True), (None, True)),
        (((None,), True), ((None,), True)),

        # INT --------------
        (0, (0,)),
        ((0,), (0,)),
        (1, (1,)),
        (1 + 1, (2,)),

        # CALLABLES --------------
        (LAMBDA_TRUE, (LAMBDA_TRUE,)),
        (LAMBDA_NONE, (LAMBDA_NONE,)),
        (LAMBDA_EXX, (LAMBDA_EXX,)),

        (ClsGen, (ClsGen,)),
        (INST_GEN, (INST_GEN,)),

        (ArgsKwargs(1), (1,)),
        (ArgsKwargs(1, 2), (1, 2)),
    ]
)
def test__args(source, _EXPECTED):
    source = ArgsKwargsAux(source).resolve_args
    PytestAux(source).assert_check(_EXPECTED)


# =====================================================================================================================
