import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_datetime.m1_datetime import *


# =====================================================================================================================
NOW_TD = datetime.datetime.now()
NOW_TS = NOW_TD.timestamp()


# =====================================================================================================================
class Test__DateTime:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (True, Exception),
            # (None, Exception),

            (datetime.datetime(1,2, 3, 11, 22, 33), datetime.datetime(1,2,3, 11, 22, 33)),

            (datetime.date(1,2,3) , datetime.date(1,2,3)),
            (datetime.time(11,22,33), datetime.time(11,22,33)),

            (NOW_TD, NOW_TD),
            (str(NOW_TD), NOW_TD),

            # float -----------
            (NOW_TS, NOW_TD),

            # str -------------
            ("2025.02.26 17.00.56", datetime.datetime(2025,2,26, 17, 0, 56)),
            ("2025.202.26 17.00.00", Exception),
            ("2025.02.26 25.00.00", Exception),

            ("2025.02.26 17.00", Exception),    # incomplete
        ]
    )
    def test__init(self, source, _EXPECTED):
        func_link = lambda: DateTimeAux(source).SOURCE
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, other, _EXPECTED",
        argvalues=[
            (True, True, Exception),
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
            # TODO: FINISH!!!
        ]
    )
    def test__eq(self, source, other, _EXPECTED):
        func_link = lambda: DateTimeAux(source) == other
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
