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
@pytest.mark.parametrize(
    argnames="accuracy_v, accuracy_p, _EXPECTED",
    argvalues=[
        (None, None, True),
        (0, None, True),
        (None, 0, True),

        (0, 0, False),
        ("exc", None, False),
        ("exc", 0, False),
        (None, "exc", False),
        (0, "exc", False),
        ("exc", "exc", False),
    ]
)
def test__cmp_accuracy__check_correctness(
        accuracy_v: float | None,
        accuracy_p: float | None,
        _EXPECTED: bool,
):
    victim = Victim(1)

    Lambda(victim._cmp_accuracy__check_correctness, accuracy_v, accuracy_p, False).expect__check_assert(_EXPECTED)

    Lambda(victim._cmp_accuracy__check_correctness, accuracy_v, accuracy_p).expect__check_assert(True if _EXPECTED else Exception)
    Lambda(victim._cmp_accuracy__check_correctness, accuracy_v, accuracy_p, True).expect__check_assert(True if _EXPECTED else Exception)

    assert Lambda(Victim, 1, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p).check_raise() != _EXPECTED
    Lambda(Victim, 1, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p).expect__check_assert(NestCmp_GLET_DigitAccuracy if _EXPECTED else Exception)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="source, accuracy_p, _EXPECTED",
    argvalues=[
        (0, None, 0),
        (0, 0, 0),
        (1, 0, 0),

        (100, 0, 0),
        (100, 0.1, 0.1),
        (100, 1, 1),
        (100, 10, 10),
        (100, 1000, 1000),

        (0.1, 0, 0),
        (0.1, 0.1, 0.001),  # FIXME! use cmp by percent!
        (0.1, 1, 0.001),
        (0.1, 10, 0.01),
        (0.1, 1000, 1),
    ]
)
def test__cmp_accuracy__translate_from_percent(
        source: float | None,
        accuracy_p: float | None,
        _EXPECTED: float,
):
    victim = Victim(source)

    Lambda(victim._cmp_accuracy__translate_from_percent, accuracy_p).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, accuracy_vp, _EXP_GLET, _EXP_EQ",
    argvalues=[
        # TRIVIAL ---------------------------------
        ("exc", 1,  (0, None), (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, "exc",  (0, None), (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, 1, ("exc", None), (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, 1, (None, "exc"), (Exception, Exception, Exception, Exception), (Exception, Exception)),
        (1, 1, (0, 0), (Exception, Exception, Exception, Exception), (Exception, Exception)),

        # 1+1--------------------------------------
        (1, 1,      (None, None), (False, True, True, False), (True, False)),
        (1, 1.0,    (None, None), (False, True, True, False), (True, False)),
        (1.0, 1.0,  (None, None), (False, True, True, False), (True, False)),
        (1.0, 1,    (None, None), (False, True, True, False), (True, False)),

        (1, 1,      (0, None), (False, True, True, False), (True, False)),
        (1, 1.0,    (0, None), (False, True, True, False), (True, False)),
        (1.0, 1.0,  (0.0, None), (False, True, True, False), (True, False)),
        (1.0, 1,    (0, None), (False, True, True, False), (True, False)),

        (1, 1,      (None, 0), (False, True, True, False), (True, False)),
        (1, 1.0,    (None, 0), (False, True, True, False), (True, False)),
        (1.0, 1.0,  (None, 0.0), (False, True, True, False), (True, False)),
        (1.0, 1,    (None, 0), (False, True, True, False), (True, False)),

        # 1+0.9/1.1---------------------------------
        (1, 0.9, (0.2, None), (True, True, True, True), (True, False)),
        (1, 0.9, (0.1, None), (True, True, True, False), (True, False)),
        (1, 0.9, (0.05, None), (True, True, False, False), (False, True)),
        (1, 0.9, (0, None), (True, True, False, False), (False, True)),
        (1, 1.1, (0, None), (False, False, True, True), (False, True)),
        (1, 1.1, (0.05, None), (False, False, True, True), (False, True)),
        (1, 1.1, (0.1, None), (False, True, True, True), (True, False)),
        (1, 1.1, (0.2, None), (True, True, True, True), (True, False)),

        (1, 0.9, (None, 20), (True, True, True, True), (True, False)),
        (1, 0.9, (None, 10), (True, True, True, False), (True, False)),
        (1, 0.9, (None, 5), (True, True, False, False), (False, True)),
        (1, 0.9, (None, 0), (True, True, False, False), (False, True)),
        (1, 1.1, (None, 0), (False, False, True, True), (False, True)),
        (1, 1.1, (None, 5), (False, False, True, True), (False, True)),
        (1, 1.1, (None, 10), (False, True, True, True), (True, False)),
        (1, 1.1, (None, 20), (True, True, True, True), (True, False)),
    ]
)
def test__cmp_glet__single(
        source: float | int,
        other: float | int,
        accuracy_vp: tuple[float | None, float | None],
        _EXP_GLET: tuple[bool | Exception, ...],
        _EXP_EQ: tuple[bool | Exception, ...],
):
    accuracy_v, accuracy_p = accuracy_vp

    RAISED = not Victim(0)._cmp_accuracy__check_correctness(*accuracy_vp, False)

    # ACC init- meth- -----------------------------------------------
    if accuracy_v is None and accuracy_p is None:
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

    # ACC init- meth+ -----------------------------------------------
    victim = Victim(source=source)

    Lambda(victim.cmp_gt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, *accuracy_vp).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, *accuracy_vp).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, *accuracy_vp).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, *accuracy_vp).expect__check_assert(_EXP_EQ[1])

    # ACC init0 meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=0)

    Lambda(victim.cmp_gt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, *accuracy_vp).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, *accuracy_vp).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, *accuracy_vp).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, *accuracy_vp).expect__check_assert(_EXP_EQ[1])


    Lambda(Victim, 1, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p).expect__check_assert(NestCmp_GLET_DigitAccuracy if not RAISED else Exception)

    if RAISED:
        return

    # ACC init+ meth- -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(victim.cmp_gt, other).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other).expect__check_assert(_EXP_EQ[1])

    # ACC init+ meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(victim.cmp_gt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[0])
    Lambda(victim.cmp_ge, other, *accuracy_vp).expect__check_assert(_EXP_GLET[1])
    Lambda(victim.cmp_le, other, *accuracy_vp).expect__check_assert(_EXP_GLET[2])
    Lambda(victim.cmp_lt, other, *accuracy_vp).expect__check_assert(_EXP_GLET[3])

    Lambda(victim.cmp_eq, other, *accuracy_vp).expect__check_assert(_EXP_EQ[0])
    Lambda(victim.cmp_ne, other, *accuracy_vp).expect__check_assert(_EXP_EQ[1])

    # OPERATOR -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(operator.gt, victim, other).expect__check_assert(_EXP_GLET[0])
    Lambda(operator.ge, victim, other).expect__check_assert(_EXP_GLET[1])
    Lambda(operator.le, victim, other).expect__check_assert(_EXP_GLET[2])
    Lambda(operator.lt, victim, other).expect__check_assert(_EXP_GLET[3])

    Lambda(operator.eq, victim, other).expect__check_assert(_EXP_EQ[0])
    Lambda(operator.ne, victim, other).expect__check_assert(_EXP_EQ[1])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other1, other2, accuracy_vp, _EXPECTED",
    argvalues=[
        # TRIVIAL ---------------------------------
        ("exc", 1, 1, (0, None), (Exception, Exception, Exception, Exception)),
        (1, "exc", 1, (0, None), (Exception, Exception, Exception, Exception)),
        (1, 1, "exc", (0, None), (False, False, Exception, Exception)),
        (1, 1, 1, ("exc", None), (Exception, Exception, Exception, Exception)),
        (1, 1, 1, (None, "exc"), (Exception, Exception, Exception, Exception)),
        (1, 1, 1, (0, 0), (Exception, Exception, Exception, Exception)),

        # 1+1--------------------------------------
        (1, 1, 1, (None, None), (False, False, False, True)),
        (1, 1.0, 1.0, (None, None), (False, False, False, True)),
        (1.0, 1.0, 1.0, (None, None), (False, False, False, True)),
        (1.0, 1, 1, (None, None), (False, False, False, True)),

        (1, 1, 1, (0, None), (False, False, False, True)),
        (1, 1.0, 1.0, (0, None), (False, False, False, True)),
        (1.0, 1.0, 1.0, (0, None), (False, False, False, True)),
        (1.0, 1, 1, (0, None), (False, False, False, True)),

        # 1+0.9/1.1---------------------------------
        (1, 0.9, 0.9, (0.2, None), (True, True, True, True)),
        (1, 0.9, 0.9, (0.1, None), (False, True, False, True)),
        (1, 0.9, 0.9, (0, None), (False, False, False, False)),
        (1, 1.1, 1.1, (0, None), (False, False, False, False)),
        (1, 1.1, 1.1, (0.1, None), (False, False, True, True)),
        (1, 1.1, 1.1, (0.2, None), (True, True, True, True)),
    ]
)
def test__cmp_glet__double(
        source: float | int,
        other1: float | int,
        other2: float | int,
        accuracy_vp: tuple[float | None, float | None],
        _EXPECTED: tuple[bool | Exception, ...],
):
    accuracy_v, accuracy_p = accuracy_vp

    RAISED = not Victim(0)._cmp_accuracy__check_correctness(*accuracy_vp, False)

    # ACC init- meth- -----------------------------------------------
    if accuracy_v is None and accuracy_p is None:
        victim = Victim(source=source)

        Lambda(victim.cmp_gtlt, other1, other2).expect__check_assert(_EXPECTED[0])
        Lambda(victim.cmp_gtle, other1, other2).expect__check_assert(_EXPECTED[1])
        Lambda(victim.cmp_gelt, other1, other2).expect__check_assert(_EXPECTED[2])
        Lambda(victim.cmp_gele, other1, other2).expect__check_assert(_EXPECTED[3])

        Lambda(gtlt, other1, victim, other2).expect__check_assert(_EXPECTED[0])
        Lambda(gtle, other1, victim, other2).expect__check_assert(_EXPECTED[1])
        Lambda(gelt, other1, victim, other2).expect__check_assert(_EXPECTED[2])
        Lambda(gele, other1, victim, other2).expect__check_assert(_EXPECTED[3])

    # ACC init- meth+ -----------------------------------------------
    victim = Victim(source=source)

    Lambda(victim.cmp_gtlt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[3])

    # ACC init0 meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=0)

    Lambda(victim.cmp_gtlt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[3])



    Lambda(Victim, 1, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p).expect__check_assert(NestCmp_GLET_DigitAccuracy if not RAISED else Exception)

    if RAISED:
        return

    # ACC init+ meth- -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(victim.cmp_gtlt, other1, other2).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2).expect__check_assert(_EXPECTED[3])

    # ACC init+ meth+ -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(victim.cmp_gtlt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[0])
    Lambda(victim.cmp_gtle, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[1])
    Lambda(victim.cmp_gelt, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[2])
    Lambda(victim.cmp_gele, other1, other2, *accuracy_vp).expect__check_assert(_EXPECTED[3])

    # OPERATOR -----------------------------------------------
    victim = Victim(source=source, cmp_accuracy_value=accuracy_v, cmp_accuracy_percent=accuracy_p)

    Lambda(gtlt, other1, victim, other2).expect__check_assert(_EXPECTED[0])
    Lambda(gtle, other1, victim, other2).expect__check_assert(_EXPECTED[1])
    Lambda(gelt, other1, victim, other2).expect__check_assert(_EXPECTED[2])
    Lambda(gele, other1, victim, other2).expect__check_assert(_EXPECTED[3])


# =====================================================================================================================
def test__accuracy_in_levels__only_v():
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
