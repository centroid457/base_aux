import time

import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_datetime.m2_datetime import *
import operator


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
            ("2025.02.26 25.00.00", Exception),     # inappropriate

            ("2025.02.26 17.00", Exception),        # incomplete

            ("2025.1.1 1.1.1", datetime.datetime(2025, 1, 1, 1, 1, 1)),
        ]
    )
    def test__init(self, source, _EXPECTED):
        func_link = lambda: DateTimeAux(source).SOURCE
        Lambda(func_link).check_expected__assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, other, cmp_func, _EXPECTED",
        argvalues=[
            (True, True, operator.eq, Exception),
            ("2025.1.1 1.1.1", True, operator.eq, Exception),
            ("2025.1.1 1.1.1", "2025.2.", operator.lt, Exception),

            ("2025.1.1 1.1.1", "2025.1.1 1.1.1", operator.eq, True),
            ("2025.1.1 1.1.1", "2025.1.1 2.1.1", operator.lt, True),

            ("2025.1.1 1.1.1", "1.2.1", operator.lt, True),
            ("2025.1.1 1.1.1", "1.0.1", operator.lt, False),

            ("2025.1.1 1.1.1", "2025.2.1", operator.lt, True),
            ("2025.1.2 1.1.1", "2025.1.1", operator.lt, False),

            (NOW_TD, NOW_TD, operator.eq, True),
            (NOW_TD, NOW_TS, operator.eq, True),
            (NOW_TS, NOW_TD, operator.eq, True),
            (NOW_TS, NOW_TS, operator.eq, True),

            (NOW_TS, str(NOW_TS), operator.eq, True),
            (str(NOW_TS), NOW_TS, operator.eq, True),
            (str(NOW_TS), str(NOW_TS), operator.eq, True),
        ]
    )
    def test__cmp(self, source, other, cmp_func, _EXPECTED):
        func_link = lambda: cmp_func(DateTimeAux(source), other)
        Lambda(func_link).check_expected__assert(_EXPECTED)

    def test__cmp_ms(self):
        victim1 = DateTimeAux()
        victim2 = DateTimeAux()
        assert victim1 == victim2
        assert victim1.DTm == victim2.DTm

        victim1 = DateTimeAux()
        time.sleep(0.1)
        victim2 = DateTimeAux()
        print(victim1.DTm)
        print(victim2.DTm)
        # assert str(victim1) == str(victim2)
        assert victim1.DTm != victim2.DTm
        assert victim1 != victim2

    def test__update_on_str(self):
        # victim = DateTimeAux(update_on_str=True, def_str_pattern="DTm")
        # for sleep in [0, 0.2]:
        #     str1 = str(victim)
        #     if sleep:
        #         time.sleep(sleep)
        #     str2 = str(victim)
        #     print(str1)
        #     print(str2)
        #     if sleep:
        #         assert str1 != str2
        #     else:
        #         assert str1 == str2   # not always work!

        victim = DateTimeAux(update_on_str=True, def_str_pattern="DTm")
        str1 = str(victim)
        time.sleep(0.1)
        str2 = str(victim)
        print(str1)
        print(str2)
        assert str1 != str2


# =====================================================================================================================
