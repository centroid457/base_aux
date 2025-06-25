import pytest

from base_aux.lambdas.m1_lambda import *
from base_aux.aux_values.m4_primitives import *
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
    Lambda(source).expect__check_assert(_EXPECTED)


# =====================================================================================================================
