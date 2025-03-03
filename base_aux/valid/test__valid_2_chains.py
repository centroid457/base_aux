import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.base_statics.m3_primitives import *

from base_aux.valid.m3_valid_chains import *
from base_aux.valid.m2_valid_base2_derivatives import *


# =====================================================================================================================
class Test__ValidChains:
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
        ]
    )
    def test__types_single(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ([ValidNoCum(False), ], True),
        ]
    )
    def test__nocum(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        ExpectAux(func_link).check_assert(_EXPECTED)

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
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ([ValidSleep(), True], True),
            ([ValidSleep(0.1), True], True),
            ([ValidSleep(0.1), False], False),

            ([ValidSleep(2, True), ], True),
        ]
    )
    def test__util1_sleep(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="chains, _EXPECTED",
        argvalues=[
            ([False, ValidBreak(True), True], False),

            ([True, ValidBreak(True), False], True),
            ([True, ValidBreak(False), False], False),
            ([True, ValidBreak(False), True], True),

            ([ValidBreak(True), False], True),
            ([ValidBreak(False), False], False),
            ([ValidBreak(False), True], True),
        ]
    )
    def test__util2_break(self, chains, _EXPECTED):
        func_link = ValidChains(chains).run
        ExpectAux(func_link).check_assert(_EXPECTED)

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
