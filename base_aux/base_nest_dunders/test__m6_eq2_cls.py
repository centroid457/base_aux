from base_aux.base_nest_dunders.m6_eq2_cls import *
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
def test__incorrect_zero():
    class Victim0:
        ATTR = 1

    class VictimEq(Nest_EqCls):
        ATTR = 1

    assert Victim0 != VictimEq
    assert Victim0 != VictimEq()
    assert Victim0() != VictimEq()
    assert Victim0() != VictimEq

    assert VictimEq != Victim0
    assert VictimEq != Victim0()
    assert VictimEq() != Victim0()
    assert VictimEq() != Victim0


def test__incorrect_direct():
    class Victim0:
        ATTR = 1

    class VictimEq(Nest_EqCls):
        ATTR = 1

        @classmethod
        @property
        def _EQ_CLS__VALUE(cls) -> Any:
            return cls.ATTR

    assert Victim0 != VictimEq
    assert Victim0 != VictimEq()
    assert Victim0() != VictimEq()
    assert Victim0() != VictimEq

    assert VictimEq != Victim0
    assert VictimEq != Victim0()
    assert VictimEq() != Victim0()
    assert VictimEq() != Victim0


# =====================================================================================================================
def test__correct_false():
    class Victim0:
        ATTR = 1

    class VictimEq(Nest_EqCls):
        ATTR = 1

        @classmethod
        @property
        def _EQ_CLS__VALUE(cls) -> Any:
            return cls.ATTR

    assert not VictimEq._eq_cls__check(Victim0)
    assert not VictimEq._eq_cls__check(Victim0())
    assert not VictimEq()._eq_cls__check(Victim0())
    assert not VictimEq()._eq_cls__check(Victim0)


def test__correct_usage():
    class VictimEqBase(Nest_EqCls):
        ATTR1: Any
        ATTR2: Any
        @classmethod
        @property
        def _EQ_CLS__VALUE(cls) -> Any:
            return cls.ATTR1 + cls.ATTR2

    class VictimEq1(VictimEqBase):
        ATTR1 = 1
        ATTR2 = 2

    class VictimEq2(VictimEqBase):
        ATTR1 = 2
        ATTR2 = 1

    assert VictimEq1 != VictimEq2
    assert VictimEq1 != VictimEq2()
    assert VictimEq1() != VictimEq2()
    assert VictimEq1() != VictimEq2

    assert VictimEq1._eq_cls__check(VictimEq2)
    assert VictimEq1._eq_cls__check(VictimEq2())
    assert VictimEq1()._eq_cls__check(VictimEq2())
    assert VictimEq1()._eq_cls__check(VictimEq2)

    VictimEq1().ATTR1 = 100
    assert VictimEq1 != VictimEq2
    assert VictimEq1 != VictimEq2()
    assert VictimEq1() != VictimEq2()
    assert VictimEq1() != VictimEq2

    assert VictimEq1._eq_cls__check(VictimEq2)
    assert VictimEq1._eq_cls__check(VictimEq2())
    assert VictimEq1()._eq_cls__check(VictimEq2())
    assert VictimEq1()._eq_cls__check(VictimEq2)

    VictimEq1.ATTR1 = 100
    assert VictimEq1 != VictimEq2
    assert VictimEq1 != VictimEq2()
    assert VictimEq1() != VictimEq2()
    assert VictimEq1() != VictimEq2

    assert not VictimEq1._eq_cls__check(VictimEq2)
    assert not VictimEq1._eq_cls__check(VictimEq2())
    assert not VictimEq1()._eq_cls__check(VictimEq2())
    assert not VictimEq1()._eq_cls__check(VictimEq2)


def test__staticmethod():
    class VictimEqBase(Nest_EqCls):
        ATTR1: Any
        ATTR2: Any
        @classmethod
        @property
        def _EQ_CLS__VALUE(cls) -> Any:
            return cls.ATTR1 + cls.ATTR2

    class VictimEq1(VictimEqBase):
        ATTR1 = 1
        ATTR2 = 2

    class VictimEq2(VictimEqBase):
        ATTR1 = 2
        ATTR2 = 1

    assert Nest_EqCls._eq_classes__check(VictimEq1, VictimEq2)
    assert Nest_EqCls._eq_classes__check(VictimEq1, VictimEq2())
    assert Nest_EqCls._eq_classes__check(VictimEq1(), VictimEq2())
    assert Nest_EqCls._eq_classes__check(VictimEq1(), VictimEq2)


# =====================================================================================================================
