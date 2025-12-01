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
            # TRIVIAL ---------------------------------
            (1, None, "hello", (Exception, Exception, Exception, Exception)),

            # 1+1---------------------------------
            (1, 0, 1, (False, True, True, False)),
            (1, 0, 1.0, (False, True, True, False)),
            (1.0, 0.0, 1.0, (False, True, True, False)),
            (1.0, 0, 1, (False, True, True, False)),

            # 1+1.1---------------------------------
            (1, 0.2, 0.9, (True, True, True, True)),
            (1, 0.1, 0.9, (True, True, True, False)),
            (1, 0, 1.1, (False, False, True, True)),
            (1, 0.1, 1.1, (False, True, True, True)),
            (1, 0.2, 1.1, (True, True, True, True)),

            (1, None, 1, (False, True, True, False)),
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

        Lambda(victim.cmp_gt, other=other).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_ge, other=other).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        victim = Victim(source=source)

        Lambda(victim.cmp_gt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_ge, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        victim = Victim(source=source, cmp_accuracy=accuracy)

        Lambda(victim.cmp_gt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_ge, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_le, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_lt, other=other, accuracy=accuracy).expect__check_assert(_EXPECTED[3])

        # -----------------------------------------------
        victim = Victim(source=source, cmp_accuracy=accuracy)

        Lambda(operator.gt, victim, other).expect__check_assert(_EXPECTED[0])
        Lambda(operator.ge, victim, other).expect__check_assert(_EXPECTED[1])
        Lambda(operator.le, victim, other).expect__check_assert(_EXPECTED[2])
        Lambda(operator.lt, victim, other).expect__check_assert(_EXPECTED[3])

    # -----------------------------------------------------------------------------------------------------------------
    def test__accuracy_in_levels(self):
        # 1=NONE
        victim = Victim(source=1, cmp_accuracy=None)

        assert victim >= 1
        assert victim.cmp_ge(1)
        assert victim.cmp_le(1)
        assert victim.cmp_ge(1, accuracy=0.1)
        assert victim.cmp_le(1, accuracy=0.1)

        assert not victim > 1
        assert not victim.cmp_gt(1)
        assert not victim.cmp_lt(1)
        assert victim.cmp_gt(1, accuracy=0.1)
        assert victim.cmp_lt(1, accuracy=0.1)

        # 2=0.1
        victim = Victim(source=1, cmp_accuracy=0.1)

        assert victim >= 1
        assert victim.cmp_ge(1)
        assert victim.cmp_le(1)
        assert victim.cmp_ge(1, accuracy=0.1)
        assert victim.cmp_le(1, accuracy=0.1)

        assert victim > 1
        assert victim.cmp_gt(1)
        assert victim.cmp_lt(1)
        assert victim.cmp_gt(1, accuracy=0.1)
        assert victim.cmp_lt(1, accuracy=0.1)

        other = 0.9
        assert victim >= other
        assert victim.cmp_ge(other)
        assert victim.cmp_le(other)
        assert victim.cmp_ge(other, accuracy=0.1)
        assert victim.cmp_le(other, accuracy=0.1)

        # FIXME: !!!=================================
        # assert victim > other
        # assert victim.cmp_gt(other)
        # assert not victim.cmp_lt(other)
        # assert victim.cmp_gt(other, accuracy=0.1)
        # assert not victim.cmp_lt(other, accuracy=0.1)


# =====================================================================================================================
