from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m7_cmp import *
import operator

# =====================================================================================================================
class Victim(NestCmp_GLET_DigitAccuracy):
    def __init__(self, source: float | int, **kwargs):
        self.SOURCE = source
        super().__init__(**kwargs)

    @property
    def CMP_VALUE(self) -> TYPING.DIGIT_FLOAT_INT:
        return self.SOURCE


# =====================================================================================================================
class Test_CmpDigit:
    @pytest.mark.parametrize(
        argnames="source, accuracy, other, _EXPECTED",
        argvalues=[
            (1, None, 1, (True, False, True, False)),
            (1, None, "hello", (Exception, Exception, Exception, Exception)),
        ]
    )
    def test__cmp_glet(
            self,
            source: float | int,
            accuracy: float | None,
            other: float | int,
            _EXPECTED: bool | Exception,
    ):
        # -----------------------------------------------
        victim = Victim(source=source, cmp_accuracy=accuracy)

        Lambda(victim.cmp_ge, other=other).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_gt, other=other).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        victim = Victim(source=source)

        Lambda(victim.cmp_ge, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_gt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        victim = Victim(source=source, cmp_accuracy=accuracy)

        Lambda(victim.cmp_ge, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_gt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        # try:      # NOTE: USE OPERATOR instead!!!
        #     result = victim >= other
        # except Exception as exc:
        #     TypeAux(exc).check__subclassed_or_isinst__from_cls_or_inst(_EXPECTED[0])
        # else:
        #     assert result is _EXPECTED[0]

        victim = Victim(source=source, cmp_accuracy=accuracy)

        Lambda(operator.ge, victim, other).expect__check_assert(_EXPECTED[0])
        Lambda(operator.gt, victim, other).expect__check_assert(_EXPECTED[1])
        Lambda(operator.le, victim, other).expect__check_assert(_EXPECTED[2])
        Lambda(operator.lt, victim, other).expect__check_assert(_EXPECTED[3])


# =====================================================================================================================
