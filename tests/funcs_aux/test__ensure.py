import pytest

from base_aux.funcs_aux import *
from base_aux.classes_aux import *
from base_aux.object_aux import *


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
        argnames="args, _EXPECTED",
        argvalues=[
            # DEF --------------
            (None, TYPE__NONE),
            (((None,), ), tuple),

            (0, int),
            ((0, ),int),
            (((0,),), tuple),

            (((),), tuple),
            (([],), list),
            (({},), dict),
            ({1:1}, int),
            (({1:1},), dict),

            # CALLABLES --------------
            (LAMBDA_TRUE, TYPE__FUNCTION),
            (LAMBDA_NONE, TYPE__FUNCTION),
            (LAMBDA_EXX, TYPE__FUNCTION),

            (CALLABLE_METH_INST, TYPE__METHOD),
            (CALLABLE_METH_CLS, TYPE__FUNCTION),

            (ClsGen, ClsGen),
            (INST_GEN, ClsGen),
        ]
    )
    def test__ensure_class(self, args, _EXPECTED):
        func_link = ensure_class
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
