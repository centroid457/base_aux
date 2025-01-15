import pytest

from base_aux.base_objects import *

from base_aux.aux_pytester import *
from base_aux.valid import *


# =====================================================================================================================
class Test__ValidChains:
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
        argnames="chains, _EXPECTED",
        argvalues=[
            ([True, ], True),
            ([False, ], False),
            ([None, ], False),

            ([0, ], False),
            ([1, ], True),      # CAREFUL assert 1 == True, assert 2 == False, assert 0 == False
            ([2, ], False),

            ([[], ], False),
            ([[None, ], ], False),

            ([Valid(True), ], True),
            ([Valid(False), ], False),
            ([Valid(False, skip_link=True), ], True),
            ([Valid(False, chain__cum=False), ], True),

            ([ValidNoCum(False), ], True),

            ([ValidSleep(), ], True),
            ([ValidSleep(0.1), ], True),
            ([ValidSleep(), ], True),
        ]
    )
    def test__types_single(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ([True, True, True], True),
            ([True, False, True], False),

            ([True, LAMBDA_TRUE, True], True),
            ([True, LAMBDA_TRUE, ClsCallTrue()], True),

            ([Valid(True), Valid(True)], True),
            ([Valid(True), Valid(False)], False),
            ([Valid(True), Valid(False, skip_link=True)], True),
            ([Valid(True), Valid(False, chain__cum=False)], True),

            ([True, ValidChains([True, True])], True),
            ([True, ValidChains([False, ], skip_link=True)], True),
            ([True, ValidChains([False, ], chain__cum=False)], True),
        ]
    )
    def test__chains(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains",
        argvalues=[
            [True, True, True],
            [True, False, True],

            [True, LAMBDA_TRUE, True],
            [True, LAMBDA_TRUE, ClsCallTrue()],

            [Valid(True), Valid(True)],
            [Valid(True), Valid(False)],
            [Valid(True), Valid(False, skip_link=True)],
            [Valid(True), Valid(False, chain__cum=False)],

            [True, ValidChains([True, True])],
            [True, ValidChains([False, ], skip_link=True)],
            [True, ValidChains([False, ], chain__cum=False)],
        ]
    )
    def test__str(self, chains):
        assert str(ValidChains(chains)) is not None


# =====================================================================================================================
