from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m7_cmp import *
import operator

from base_aux.base_values.m6_operator import gtlt, gtle, gelt, gele


# =====================================================================================================================
class Victim(NestCmp_GLET_DigitAccuracy):
    def __init__(self, source: float | int, **kwargs):
        self.SOURCE = source
        super().__init__(**kwargs)

    @property
    def CMP_VALUE(self) -> TYPING.DIGIT_FLOAT_INT:
        return self.SOURCE


# =====================================================================================================================
# TODO: add tests for percent!!!

@pytest.mark.parametrize(
    argnames="source, accuracy_value, other, _EXP_GLET, _EXP_EQ",
    argvalues=[
        # TRIVIAL ---------------------------------
        ("exc", 0, 1, (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, "exc", 1, (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, 0, "exc", (Exception, Exception, Exception, Exception), (Exception, Exception)),

        # 1+1--------------------------------------
        (1, None, 1, (False, True, True, False), (True, False)),
        (1, None, 1.0, (False, True, True, False), (True, False)),
        (1.0, None, 1.0, (False, True, True, False), (True, False)),
        (1.0, None, 1, (False, True, True, False), (True, False)),

        (1, 0, 1, (False, True, True, False), (True, False)),
        (1, 0, 1.0, (False, True, True, False), (True, False)),
        (1.0, 0.0, 1.0, (False, True, True, False), (True, False)),
        (1.0, 0, 1, (False, True, True, False), (True, False)),

        # 1+0.9/1.1---------------------------------
        (1, 0.2, 0.9, (True, True, True, True), (True, False)),
        (1, 0.1, 0.9, (True, True, True, False), (True, False)),
        (1, 0, 0.9, (True, True, False, False), (False, True)),
        (1, 0, 1.1, (False, False, True, True), (False, True)),
        (1, 0.1, 1.1, (False, True, True, True), (True, False)),
        (1, 0.2, 1.1, (True, True, True, True), (True, False)),
    ]
)
def test__cmp_glet(
        source: float | int,
        accuracy_value: float | None,
        other: float | int,
        _EXP_GLET: tuple[bool | Exception, ...],
        _EXP_EQ: tuple[bool | Exception, ...],
):
    # ACC init- meth- -----------------------------------------------
    if not accuracy_value:
        victim = Victim(source=source)

        Lambda(victim.cmp_gt, other).expect__check_assert(_EXP_GLET[0])
        Lambda(victim.cmp_ge, other).expect__check_assert(_EXP_GLET[1])
        Lambda(victim.cmp_le, other).expect__check_assert(_EXP_GLET[2])
        Lambda(victim.cmp_lt, other).expect__check_assert(_EXP_GLET[3])

        Lambda(victim.cmp_eq, other).expect__check_assert(_EXP_EQ[0])
        Lambda(victim.cmp_ne, other).expect__check_assert(_EXP_EQ[1])

        Lambda(operator.gt, victim, other).expect__check_assert(_EXP_GLET[0])
        Lambda(operator.ge, victim, other).expect__check_assert(_EXP_GLET[1])
        Lambda(operator.le, victim, other).expect__check_assert(_EXP_GLET[2])
        Lambda(operator.lt, victim, other).expect__check_assert(_EXP_GLET[3])

        Lambda(operator.eq, victim, other).expect__check_assert(_EXP_EQ[0])
        Lambda(operator.ne, victim, other).expect__check_assert(_EXP_EQ[1])

    # ACC init+ meth- -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(victim.cmp_gt, other).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other).expect__check_assert(_EXP_EQ[1])

    # ACC init- meth+ -----------------------------------------------
    victim = Victim(source=source)

    Lambda(victim.cmp_gt, other, accuracy_value).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, accuracy_value).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, accuracy_value).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, accuracy_value).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, accuracy_value).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, accuracy_value).expect__check_assert(_EXP_EQ[1])

    # ACC init+ meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(victim.cmp_gt, other, accuracy_value).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, accuracy_value).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, accuracy_value).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, accuracy_value).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, accuracy_value).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, accuracy_value).expect__check_assert(_EXP_EQ[1])

    # ACC init0 meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=0)

    Lambda(victim.cmp_gt, other, accuracy_value).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, accuracy_value).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, accuracy_value).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, accuracy_value).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, accuracy_value).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, accuracy_value).expect__check_assert(_EXP_EQ[1])

    # OPERATOR -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(operator.gt, victim, other).expect__check_assert(_EXP_GLET[0])
    Lambda(operator.ge, victim, other).expect__check_assert(_EXP_GLET[1])
    Lambda(operator.le, victim, other).expect__check_assert(_EXP_GLET[2])
    Lambda(operator.lt, victim, other).expect__check_assert(_EXP_GLET[3])

    Lambda(operator.eq, victim, other).expect__check_assert(_EXP_EQ[0])
    Lambda(operator.ne, victim, other).expect__check_assert(_EXP_EQ[1])


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, accuracy_value, other1, other2, _EXPECTED",
    argvalues=[
        # TRIVIAL ---------------------------------
        ("exc", 0, 1, 1, (Exception, Exception, Exception, Exception)),
        (1, "exc", 1, 1, (Exception, Exception, Exception, Exception)),

        (1, 0, "exc", 1, (Exception, Exception, Exception, Exception)),
        (1, 0, 1, "exc", (False, False, Exception, Exception)),

        # 1+1--------------------------------------
        (1, None, 1, 1, (False, False, False, True)),
        (1, None, 1.0, 1.0, (False, False, False, True)),
        (1.0, None, 1.0, 1.0, (False, False, False, True)),
        (1.0, None, 1, 1, (False, False, False, True)),

        (1, 0, 1, 1, (False, False, False, True)),
        (1, 0, 1.0, 1.0, (False, False, False, True)),
        (1.0, 0, 1.0, 1.0, (False, False, False, True)),
        (1.0, 0, 1, 1, (False, False, False, True)),

        # 1+0.9/1.1---------------------------------
        (1, 0.2, 0.9, 0.9, (True, True, True, True)),
        (1, 0.1, 0.9, 0.9, (False, True, False, True)),
        (1, 0, 0.9, 0.9, (False, False, False, False)),
        (1, 0, 1.1, 1.1, (False, False, False, False)),
        (1, 0.1, 1.1, 1.1, (False, False, True, True)),
        (1, 0.2, 1.1, 1.1, (True, True, True, True)),
    ]
)
def test__cmp_glet_double(
        source: float | int,
        accuracy_value: float | None,
        other1: float | int,
        other2: float | int,
        _EXPECTED: tuple[bool | Exception, ...],
):
    # ACC init- meth- -----------------------------------------------
    if not accuracy_value:
        victim = Victim(source=source)

        Lambda(victim.cmp_gtlt, other1, other2).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_gtle, other1, other2).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_gelt, other1, other2).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_gele, other1, other2).expect__check_assert(_EXPECTED[3])

        Lambda(gtlt, other1, victim, other2).expect__check_assert(_EXPECTED[0])
        Lambda(gtle, other1, victim, other2).expect__check_assert(_EXPECTED[1])
        Lambda(gelt, other1, victim, other2).expect__check_assert(_EXPECTED[2])
        Lambda(gele, other1, victim, other2).expect__check_assert(_EXPECTED[3])

    # ACC init+ meth- -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(victim.cmp_gtlt, other1, other2).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2).expect__check_assert(_EXPECTED[3])

    # ACC init- meth+ -----------------------------------------------
    victim = Victim(source=source)

    Lambda(victim.cmp_gtlt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[3])

    # ACC init+ meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(victim.cmp_gtlt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[3])

    # ACC init0 meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=0)

    Lambda(victim.cmp_gtlt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, accuracy_value).expect__check_assert(_EXPECTED[3])

    # OPERATOR -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_value)

    Lambda(gtlt, other1, victim, other2).expect__check_assert(_EXPECTED[0])
    Lambda(gtle, other1, victim, other2).expect__check_assert(_EXPECTED[1])
    Lambda(gelt, other1, victim, other2).expect__check_assert(_EXPECTED[2])
    Lambda(gele, other1, victim, other2).expect__check_assert(_EXPECTED[3])


# ---------------------------------------------------------------------------------------------------------------------
def test__accuracy_in_levels():
    # COULВ BE DELETED!!! not need!

    # 1=NONE
    victim = Victim(source=1, cmp_accuracy_value=None)

    assert victim >= 1
    assert victim.cmp_ge(1)
    assert victim.cmp_le(1)
    assert victim.cmp_ge(1, accuracy_value=0.1)
    assert victim.cmp_le(1, accuracy_value=0.1)

    assert not victim > 1
    assert not victim.cmp_gt(1)
    assert not victim.cmp_lt(1)
    assert victim.cmp_gt(1, accuracy_value=0.1)
    assert victim.cmp_lt(1, accuracy_value=0.1)

    # 2=0.1
    victim = Victim(source=1, cmp_accuracy_value=0.1)

    assert victim >= 1
    assert victim.cmp_ge(1)
    assert victim.cmp_le(1)
    assert victim.cmp_ge(1, accuracy_value=0.1)
    assert victim.cmp_le(1, accuracy_value=0.1)

    assert victim > 1
    assert victim.cmp_gt(1)
    assert victim.cmp_lt(1)
    assert victim.cmp_gt(1, accuracy_value=0.1)
    assert victim.cmp_lt(1, accuracy_value=0.1)

    other = 0.9
    assert victim >= other
    assert victim.cmp_ge(other)
    assert victim.cmp_le(other)
    assert victim.cmp_ge(other, accuracy_value=0.1)
    assert victim.cmp_le(other, accuracy_value=0.1)


# =====================================================================================================================
