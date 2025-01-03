import pytest
from base_aux.base_argskwargs import *
from base_aux.base_objects import *

from base_aux.pytester import *
from base_aux.funcs.value_0_explicit import Default
from base_aux.cmp.cmp import CmpInst


# =====================================================================================================================
class Cls(CmpInst):
    def __init__(self, value):
        self.VALUE = value

    def __cmp__(self, other):
        other = Cls(other)
        if self.VALUE == other.VALUE:
            return 0
        if self.VALUE > other.VALUE:
            return 1
        if self.VALUE < other.VALUE:
            return -1


# =====================================================================================================================
class Test__Args:
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
            (Default, ()),
            (Default(), (None, )),
            (Default(None), (None, )),

            # None --------------
            (None, (None, )),
            ((None, ), (None, )),

            ((None, True), ()),
            (((None, ), True), (None, )),

            # INT --------------
            (0, (0, )),
            ((0, ), (0, )),
            (1, (1, )),
            (1+1, (2, )),

            ((), ()),
            ([], ()),
            ({}, ()),

            ((1,), (1,)),
            ([1,], (1,)),
            ({1:1}, (1,)),

            # CALLABLES --------------
            (LAMBDA_TRUE, (LAMBDA_TRUE, )),
            (LAMBDA_NONE, (LAMBDA_NONE, )),
            (LAMBDA_EXX, (LAMBDA_EXX, )),

            (ClsGen, (ClsGen, )),
            (INST_GEN, (INST_GEN, )),
        ]
    )
    def test__ensure_tuple(self, args, _EXPECTED):
        func_link = args__ensure_tuple
        pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


# =====================================================================================================================

