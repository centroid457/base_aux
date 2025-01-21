import pytest
from base_aux.aux_pytester.m1_pytest_aux import *
from base_aux.base_objects.m0_primitives import *


# =====================================================================================================================
class Test__Args:
    # -----------------------------------------------------------------------------------------------------------------
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
            (None, (None, )),
            ((None, ), (None, )),

            ((None, True), (None, True)),
            (((None, ), True), ((None, ), True)),

            # INT --------------
            (0, (0, )),
            ((0, ), (0, )),
            (1, (1, )),
            (1+1, (2, )),

            # CALLABLES --------------
            (LAMBDA_TRUE, (LAMBDA_TRUE, )),
            (LAMBDA_NONE, (LAMBDA_NONE, )),
            (LAMBDA_EXX, (LAMBDA_EXX, )),

            (ClsGen, (ClsGen, )),
            (INST_GEN, (INST_GEN, )),
        ]
    )
    def test__ensure_tuple(self, source, _EXPECTED):
        func_link = ArgsKwargsAux(source).resolve_args
        PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================

