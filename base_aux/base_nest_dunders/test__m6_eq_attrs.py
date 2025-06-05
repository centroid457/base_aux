from base_aux.base_nest_dunders.m6_eq1_attrs import *
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class VictimBase:
    o = 1
    _h = 1
    __p = 1


class VictimEqNotPivate(VictimBase, NestEq_AttrsNotPrivate):
    pass


class VictimEqNotHidden(VictimBase, NestEq_AttrsNotHidden):
    pass


# =====================================================================================================================
def test__base():
    victim = AttrKit_Blank()
    assert victim == VictimBase
    assert victim == VictimBase()
    assert VictimBase == victim
    assert VictimBase() == victim

    victim = AttrKit_Blank(o=1)
    assert victim == VictimBase
    assert victim == VictimBase()
    assert VictimBase == victim
    assert VictimBase() == victim

    victim = AttrKit_Blank(o=111)
    assert victim != VictimBase
    assert victim != VictimBase()
    assert VictimBase != victim
    assert VictimBase() != victim

    victim = AttrKit_Blank(o2=111)
    assert victim != VictimBase
    assert victim != VictimBase()
    assert VictimBase != victim
    assert VictimBase() != victim


def test__nested_p():
    victim = AttrKit_Blank(o=1, _h=1, __p=1)
    assert victim == VictimEqNotPivate
    assert victim == VictimEqNotPivate()
    assert VictimEqNotPivate == victim
    assert VictimEqNotPivate() == victim

    assert victim == VictimEqNotHidden
    assert victim == VictimEqNotHidden()
    assert VictimEqNotHidden == victim
    assert VictimEqNotHidden() == victim


def test__nested_h():
    victim = AttrKit_Blank(o=1, _h=1, __p=111)
    assert victim == VictimEqNotPivate
    assert victim == VictimEqNotPivate()
    assert VictimEqNotPivate == victim
    assert VictimEqNotPivate() == victim

    assert victim == VictimEqNotHidden
    assert victim == VictimEqNotHidden()
    assert VictimEqNotHidden == victim
    assert VictimEqNotHidden() == victim


def test__nested_o():
    victim = AttrKit_Blank(o=1, _h=111, __p=111)
    assert victim == VictimEqNotPivate
    assert victim == VictimEqNotPivate()
    assert VictimEqNotPivate == victim
    assert VictimEqNotPivate() != victim    # NOTE!

    assert victim == VictimEqNotHidden
    assert victim == VictimEqNotHidden()
    assert VictimEqNotHidden == victim
    assert VictimEqNotHidden() == victim


def test__nested_():
    victim = AttrKit_Blank(o=111, _h=111, __p=111)
    assert victim != VictimEqNotPivate
    assert victim != VictimEqNotPivate()
    assert VictimEqNotPivate != victim
    assert VictimEqNotPivate() != victim

    assert victim != VictimEqNotHidden
    assert victim != VictimEqNotHidden()
    assert VictimEqNotHidden != victim
    assert VictimEqNotHidden() != victim


# =====================================================================================================================
