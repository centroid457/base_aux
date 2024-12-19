import pytest

from base_aux.base_objects import *
from base_aux.pytester import *


# =====================================================================================================================
class Test__ensure:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = type("Victim", (ValueUnit,), {})
    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # DEF --------------
            (None, TYPES.NONE),
            ((None, ), tuple),

            (0, int),
            (0,int),
            ((0,), tuple),

            ((), tuple),
            ([], list),
            ({}, dict),
            ({1:1}, dict),

            # CALLABLES --------------
            (LAMBDA_TRUE, TYPES.FUNCTION),
            (LAMBDA_NONE, TYPES.FUNCTION),
            (LAMBDA_EXX, TYPES.FUNCTION),

            (CALLABLE.METH_INST, TYPES.METHOD),
            (CALLABLE.METH_CLS, TYPES.FUNCTION),

            (ClsGen, ClsGen),
            (INST_GEN, ClsGen),
        ]
    )
    def test__ensure_class(self, source, _EXPECTED):
        func_link = TypeCheck(source).ensure__class
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
