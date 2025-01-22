import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux

from base_aux.aux_types.m0_primitives import *

from base_aux.valid.m4_valid_chains import *
from base_aux.valid.m2_valid_base2_derivatives import *
from base_aux.aux_values.m2_variants import *
from base_aux.aux_values.m3_unit import *


# =====================================================================================================================
def test__1():
    assert ClsEq(1) == 1
    assert ClsEq(1) != 2

    assert 1 == ClsEq(1)
    assert 2 != ClsEq(1)


# ---------------------------------------------------------------------------------------------------------------------
def test__str():
    victim = Valid(True)
    victim.run()
    print(victim)

    victim = ValidChains([True, ])
    victim.run()
    print(victim)


# =====================================================================================================================
class Test__ValidTypes:
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
            # BOOLS ---------------
            # direct TRUE
            ((0,), False),
            ((2,), False),  # careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)
            (([],), False),
            (([None,],), False),
            (([1,],), False),

            ((0, True), False),
            ((2, True), False),
            (([], True), False),
            (([None, True],), False),
            (([1, ], True), False),

            # active BOOL
            ((0, bool), False),
            ((2, bool), True),
            (([], bool), False),
            (([None, ], bool), True),
            (([1, ], bool), True),

            # -----------------------
            ((LAMBDA_TRUE,), True),
            ((LAMBDA_TRUE, True), True),
            ((LAMBDA_TRUE, False), False),
            ((LAMBDA_TRUE, LAMBDA_TRUE), True),
            ((LAMBDA_TRUE, LAMBDA_FALSE), False),

            ((LAMBDA_NONE,), False),

            ((LAMBDA_FALSE,), False),
            ((LAMBDA_FALSE, False), True),
            ((LAMBDA_FALSE, LAMBDA_TRUE), True),
            ((LAMBDA_FALSE, LAMBDA_EXX), False),

            ((LAMBDA_EXX, True), False),
            ((LAMBDA_EXX, LAMBDA_TRUE), False),
            ((LAMBDA_EXX,), False),
            ((LAMBDA_EXX, LAMBDA_EXX), False),
            ((LAMBDA_EXX, Exception), True),

            ((True, None), True),
            ((lambda: True, None), True),

            ((True, lambda val: val is True), True),
            ((LAMBDA_TRUE, lambda val: val is True), True),

            ((lambda: 1, lambda val: 0 < val < 2), True),
            ((lambda: 1, lambda val: 0 < val < 1), False),

            ((lambda: "1", lambda val: 0 < val < 2), False),
            ((lambda: "1", lambda val: 0 < int(val) < 2), True),
            ((lambda: "1.0", lambda val: 0 < int(val) < 2), False),
            ((lambda: "1.0", lambda val: 0 < float(val) < 2), True),

            # ValueVariants --------------------------
            (("hello", ValueVariants(variants=["hello", 1])), True),
            (("1", ValueVariants(variants=["hello", 1])), True),
            ((1, ValueVariants(variants=["hello", 1])), True),
            (("0", ValueVariants(variants=["hello", 1])), False),
        ]
    )
    def test__validate__types(self, args, _EXPECTED):
        # DIRECT -------
        func_link = Valid(*args)
        PytestAux(func_link).assert_check(_EXPECTED)

        # REVERSE ------
        func_link =  ValidReverse(*args)
        PytestAux(func_link).assert_check(not _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args, _EXPECTED",
        argvalues=[
            (1, (NoValue, lambda x: float(x) >= 1), True),
            ("1", (NoValue, lambda x: float(x) >= 1), True),
            ("0", (NoValue, lambda x: float(x) >= 1), False),
            ("hello", (NoValue, lambda x: float(x) >= 1), False),
        ]
    )
    def test__not_passed(self, source, args, _EXPECTED):
        # assert source == Valid(*valid_args)

        func_link = lambda *_args: source == Valid(*_args)
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args__value, kwargs__value, validate, _EXPECTED",
        argvalues=[
            # bool --------------------
            (0, (), {}, True, False),
            (0, (1,2,), {1:1}, True, Exception),

            (2, (), {}, bool, True),
            (2, (1,2,), {1:1}, bool, Exception),

            # VALUE --------------------
            (LAMBDA_LIST_VALUES, (1,2,), {}, [1,2], True),
            (LAMBDA_LIST_VALUES, (1,2,), {"1":11, }, [1,2,11], True),

            # ARG COLLECTION TYPES --------------------
            (LAMBDA_LIST_VALUES, 1, {}, [1, ], True),
            (LAMBDA_LIST_VALUES, ClsIterYield, {}, [ClsIterYield, ], True),
            (LAMBDA_LIST_VALUES, INST_ITER_YIELD, {}, [INST_ITER_YIELD, ], True),
            (LAMBDA_LIST_VALUES, INST_GEN, {}, [INST_GEN, ], True),
        ]
    )
    def test__value__args_kwargs(self, source, args__value, kwargs__value, validate, _EXPECTED):
        func_link = Valid(value_link=source, validate_link=validate, args__value=args__value, kwargs__value=kwargs__value)
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args__validate, kwargs__validate, validate, _EXPECTED",
        argvalues=[
            # bool --------------------
            (0, (), {}, True, False),
            (0, (1, 2,), {1: 1}, True, False),

            (2, (), {}, bool, True),
            (2, (1, 2,), {1: 1}, bool, Exception),

            # VALUE --------------------
            (LAMBDA_LIST_VALUES, (1, 2,), {}, [1, 2], False),
            (LAMBDA_LIST_VALUES, (1, 2,), {}, [], True),

            (LAMBDA_LIST_VALUES, (1, 2,), {"1": 11, }, [1, 2, 11], False),
            (LAMBDA_LIST_VALUES, (1, 2,), {"1": 11, }, [], True),

            # VALUE --------------------
            # (0, (1, 3,), {}, ValidAux.legt, False),    # FIXME: do smth!
            # (1, (1, 3,), {}, ValidAux.legt, True),
            # (2, (1, 3,), {}, ValidAux.legt, True),
            # (3, (1, 3,), {}, ValidAux.legt, False),
            # (4, (1, 3,), {}, ValidAux.legt, False),
            #
            # (0, (1, None,), {}, ValidAux.legt, False),
            # (1, (1, None,), {}, ValidAux.legt, True),
            # (2, (1, None,), {}, ValidAux.legt, True),
            #
            # (0, (None, 3,), {}, ValidAux.legt, True),
            # (1, (None, 3,), {}, ValidAux.legt, True),
            # (2, (None, 3,), {}, ValidAux.legt, True),
            # (3, (None, 3,), {}, ValidAux.legt, False),
        ]
    )
    def test__validate__args_kwargs(self, source, args__validate, kwargs__validate, validate, _EXPECTED):
        func_link = Valid(value_link=source, validate_link=validate, args__validate=args__validate, kwargs__validate=kwargs__validate)
        PytestAux(func_link).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args",
        argvalues=[
            # BOOLING ---------------
            # direct TRUE
            (0,),
            (2,),  # careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)
            ([],),
            ([None,],),
            ([1,],),

            (0, True),
            (2, True),
            (([], True)),
            ([None, True],),
            ([1, ], True),

            # active BOOL
            (0, bool),
            (2, bool),
            ([], bool),
            ([None, ], bool),
            ([1, ], bool),

            # -----------------------
            (LAMBDA_TRUE,),
            (LAMBDA_TRUE, True),
            (LAMBDA_TRUE, False),
            (LAMBDA_TRUE, LAMBDA_TRUE),
            (LAMBDA_TRUE, LAMBDA_FALSE),

            (LAMBDA_NONE,),

            (LAMBDA_FALSE,),
            (LAMBDA_FALSE, False),
            (LAMBDA_FALSE, LAMBDA_TRUE),
            (LAMBDA_FALSE, LAMBDA_EXX),

            (LAMBDA_EXX, True),
            (LAMBDA_EXX, LAMBDA_TRUE),
            (LAMBDA_EXX,),
            (LAMBDA_EXX, LAMBDA_EXX),
            (LAMBDA_EXX, Exception),

            (True, None),
            (lambda: True, None),

            (True, lambda val: val is True),
            (LAMBDA_TRUE, lambda val: val is True),

            (lambda: 1, lambda val: 0 < val < 2),
            (lambda: 1, lambda val: 0 < val < 1),

            (lambda: "1", lambda val: 0 < val < 2),
            (lambda: "1", lambda val: 0 < int(val) < 2),
            (lambda: "1.0", lambda val: 0 < int(val) < 2),
            (lambda: "1.0", lambda val: 0 < float(val) < 2),
        ]
    )
    def test__str(self, args):
        assert str(Valid(*args)) is not None

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, validate_link, retry, _EXPECTED",
        argvalues=[
            # bool --------------------
            ([True, False, False], list.pop, 0, False),
            ([True, False, False], list.pop, 1, False),
            ([True, False, False], list.pop, 2, True),
        ]
    )
    def test__retry(self, source, validate_link, retry, _EXPECTED):
        func_link = Valid(value_link=source, validate_link=validate_link, validate_retry=retry).run
        PytestAux(func_link).assert_check(_EXPECTED)


# =====================================================================================================================
