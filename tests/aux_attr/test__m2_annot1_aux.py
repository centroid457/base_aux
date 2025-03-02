from typing import *
import pytest

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_attr.m2_annot1_aux import AnnotsAux
from base_aux.aux_attr.m1_attr2_nest1_gsai_anycase import *


# =====================================================================================================================
class Victim1(NestGAI_AttrIC):
    ATTR1: int
    ATTR2: int = 2
    ATTR01 = 11


class Victim2(Victim1):
    ATTR3: int
    ATTR4: int = 4
    ATTR02 = 22


VICTIM1_DICT_TYPES = {"ATTR1": int, "ATTR2": int}
VICTIM2_DICT_TYPES = {"ATTR1": int, "ATTR2": int, "ATTR3": int, "ATTR4": int}

VICTIM1_DICT_VALUES = {"ATTR2": 2}
VICTIM2_DICT_VALUES = {"ATTR2": 2, "ATTR4": 4}

victim1 = Victim1()
victim2 = Victim2()


# =====================================================================================================================
class VictimDirect_Ok(NestGAI_AttrIC):
    ATTR1: int = 1
    ATTR2: int = 2


class VictimDirect_Fail(NestGAI_AttrIC):
    ATTR1: int
    ATTR2: int = 2

# -----------------------------------------------
class VictimNested_FailParent(VictimDirect_Fail):
    ATTR2: int = 2

class VictimNested_FailChild(VictimDirect_Ok):
    ATTR3: int

# -----------------------------------------------
class VictimNested_OkParent(VictimDirect_Ok):
    ATTR1: int

class VictimNested_OkCHild(VictimDirect_Fail):
    ATTR1: int = 1

# -----------------------------------------------
class DictDirect_Ok(dict, NestGAI_AttrIC):
    ATTR1: int = 1
    ATTR2: int = 2


class DictDirect_Fail(dict, NestGAI_AttrIC):
    ATTR1: int


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (VictimDirect_Ok(), []),
        (VictimDirect_Fail(), ["ATTR1", ]),

        (VictimNested_FailParent(), ["ATTR1", ]),
        (VictimNested_FailChild(), ["ATTR3", ]),

        (VictimNested_OkParent(), []),
        (VictimNested_OkCHild(), []),

        (DictDirect_Ok(), []),
        (DictDirect_Fail(), ["ATTR1", ]),
    ]
)
def test__annot__get_not_defined(source, _EXPECTED):
    func_link = AnnotsAux(source).get_not_defined
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (VictimDirect_Ok(), True),
        (VictimDirect_Fail(), False),

        (VictimNested_FailParent(), False),
        (VictimNested_FailChild(), False),

        (VictimNested_OkParent(), True),
        (VictimNested_OkCHild(), True),

        (DictDirect_Ok(), True),
        (DictDirect_Fail(), False),
    ]
)
def test__annot__check_all_defined(source, _EXPECTED):
    func_link = AnnotsAux(source).check_all_defined
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (VictimDirect_Ok(), None),
        (VictimDirect_Fail(), Exception),

        (VictimNested_FailParent(), Exception),
        (VictimNested_FailChild(), Exception),

        (VictimNested_OkParent(), None),
        (VictimNested_OkCHild(), None),

        (DictDirect_Ok(), None),
        (DictDirect_Fail(), Exception),
    ]
)
def test__annot__raise_if_not_defined(source, _EXPECTED):
    func_link = AnnotsAux(source).check_all_defined_or_raise
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class Test__1:
    @classmethod
    def setup_class(cls):
        pass
        cls.victim1 = Victim1()
        cls.victim2 = Victim2()    # @classmethod

    # =================================================================================================================
    def test__anycase_getattr(self):
        assert self.victim2.ATTR2 == 2
        assert self.victim2.attr2 == 2

    def test__anycase_getitem(self):
        assert self.victim2["ATTR2"] == 2
        assert self.victim2["attr2"] == 2

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, VICTIM1_DICT_TYPES),
            (victim2, VICTIM2_DICT_TYPES),
        ]
    )
    def test__dict_types(self, source, _EXPECTED):
        func_link = AnnotsAux(source).get__dict_types
        ExpectAux(func_link).check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, VICTIM1_DICT_VALUES),
            (victim2, VICTIM2_DICT_VALUES),
        ]
    )
    def test__dict_values(self, source, _EXPECTED):
        func_link = AnnotsAux(source).get__dict_values
        ExpectAux(func_link).check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, list(VICTIM1_DICT_VALUES.values())),
            (victim2, list(VICTIM2_DICT_VALUES.values())),
        ]
    )
    def test__iter_values(self, source, _EXPECTED):
        func_link = list(AnnotsAux(source).iter_values())
        ExpectAux(func_link).check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, False),
            (victim2, False),
        ]
    )
    def test__all_defined(self, source, _EXPECTED):
        func_link = AnnotsAux(source).check_all_defined
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
def test__all_defined2():
    class Victim11(NestGAI_AttrIC):
        ATTR1: int = 1
        ATTR2: int = 2
        ATTR01 = 11

    victim11 = Victim11()
    assert AnnotsAux(victim1).check_all_defined() == False
    assert AnnotsAux(victim11).check_all_defined() == True


# =====================================================================================================================
class VictimSet:
    A0 = 1
    A1: int
    A2: int = 1


@pytest.mark.parametrize(
    argnames="data, only_annot, _EXPECTED",
    argvalues=[
        # only_annot=TRUE
        (dict(), True, (1, Exception, 1, Exception)),
        (dict(A0=11), True, (1, Exception, 1, Exception)),
        (dict(a0=11), True, (1, Exception, 1, Exception)),

        (dict(a0=11, a1=11, a2=11, a3=11), True, (1, 11, 11, Exception)),
        (dict(A0=11, A1=11, A2=11, A3=11), True, (1, 11, 11, Exception)),

        # only_annot=FALSE
        (dict(), False, (1, Exception, 1, Exception)),
        (dict(A0=11), False, (11, Exception, 1, Exception)),
        (dict(a0=11), False, (11, Exception, 1, Exception)),

        (dict(a0=11, a1=11, a2=11, a3=11), False, (11, 11, 11, Exception)),
        (dict(A0=11, A1=11, A2=11, A3=11), False, (11, 11, 11, 11)),
    ]
)
def test__set(data, only_annot, _EXPECTED):
    victim = VictimSet()

    AnnotsAux(victim).set_values__by_dict(data, only_annot=only_annot)
    for index in range(4):
        ExpectAux(getattr, (victim, f"A{index}")).check_assert(_EXPECTED[index])


# =====================================================================================================================
class Test__SpecialObjects:
    def test__NamedTuple(self):
        class Victim(NamedTuple):
            ATTR1: int
            ATTR2: int = 2

        try:
            victimNT = Victim() # will not need! raised just on NamedTuple!
            assert False
        except:
            pass

        victimNT = Victim(1)

        assert AnnotsAux(victimNT).get_not_defined() == []
        assert AnnotsAux(victimNT).check_all_defined() == True
        assert AnnotsAux(victimNT).get__dict_types() == {"ATTR1": int, "ATTR2": int, }
        assert AnnotsAux(victimNT).get__dict_values() == {"ATTR1": 1, "ATTR2": 2, }

    @pytest.mark.skip
    def test__DataClass(self):
        pass


# =====================================================================================================================
