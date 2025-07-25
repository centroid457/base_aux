import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m4_gsai_ic__annots import NestGAI_AnnotAttrIC
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class Victim1:
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
class VictimDirect_Ok(NestGAI_AnnotAttrIC):
    ATTR1: int = 1
    ATTR2: int = 2


class VictimDirect_Fail(NestGAI_AnnotAttrIC):
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
class DictDirect_Ok(dict, NestGAI_AnnotAttrIC):
    ATTR1: int = 1
    ATTR2: int = 2

class DictDirect_Fail(dict, NestGAI_AnnotAttrIC):
    ATTR1: int


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (Victim1(), ["ATTR1", ]),
        (Victim2(), ["ATTR1", "ATTR3"]),

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
    func_link = AttrAux_AnnotsAll(source).annots__get_not_defined
    Lambda(func_link).expect__check_assert(_EXPECTED)


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
    func_link = AttrAux_AnnotsAll(source).annots__check_all_defined
    Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (VictimDirect_Ok(), True),
        (VictimDirect_Fail(), Exception),

        (VictimNested_FailParent(), Exception),
        (VictimNested_FailChild(), Exception),

        (VictimNested_OkParent(), True),
        (VictimNested_OkCHild(), True),

        (DictDirect_Ok(), True),
        (DictDirect_Fail(), Exception),
    ]
)
def test__annot__raise_if_not_defined(source, _EXPECTED):
    func_link = AttrAux_AnnotsAll(source).annots__check_all_defined_or_raise
    Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class Test__1:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.victim1 = Victim1()
    #     cls.victim2 = Victim2()    # @classmethod

    # =================================================================================================================
    # def test__anycase_getattr(self):
    #     assert self.victim2.ATTR2 == 2
        # assert self.victim2.attr2 == 2

    # def test__anycase_getitem(self):
    #     assert self.victim2["ATTR2"] == 2
        # assert self.victim2["attr2"] == 2

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, VICTIM1_DICT_TYPES),
            (victim2, VICTIM2_DICT_TYPES),
        ]
    )
    def test__dict_types(self, source, _EXPECTED):
        func_link = AttrAux_AnnotsAll(source).dump_dict__annot_types
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, VICTIM1_DICT_VALUES),
            (victim2, VICTIM2_DICT_VALUES),
        ]
    )
    def test__dict_values(self, source, _EXPECTED):
        func_link = AttrAux_AnnotsAll(source).dump_dict
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, list(VICTIM1_DICT_VALUES.values())),
            (victim2, list(VICTIM2_DICT_VALUES.values())),
        ]
    )
    def test__iter_values(self, source, _EXPECTED):
        func_link = list(AttrAux_AnnotsAll(source).iter__annot_values())
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (victim1, False),
            (victim2, False),
        ]
    )
    def test__all_defined(self, source, _EXPECTED):
        func_link = AttrAux_AnnotsAll(source).annots__check_all_defined
        Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
def test__all_defined2():
    class Victim11(NestGAI_AnnotAttrIC):
        ATTR1: int = 1
        ATTR2: int = 2
        ATTR01 = 11

    victim11 = Victim11()
    assert AttrAux_AnnotsAll(victim1).annots__check_all_defined() == False
    assert AttrAux_AnnotsAll(victim11).annots__check_all_defined() == True


# =====================================================================================================================
class VictimSet:
    A0 = 1
    A1: int
    A2: int = 1


@pytest.mark.parametrize(
    argnames="data, _EXPECTED",
    argvalues=[
        # only_annot=FALSE
        (dict(), (1, Exception, 1, Exception)),
        (dict(A0=11), (11, Exception, 1, Exception)),
        (dict(a0=11), (11, Exception, 1, Exception)),

        # (dict(a0=11, a1=11, a2=11, a3=11), (11, 11, 11, Exception)),
        # (dict(a0=11, a1=11, a2=11, a3=11), (11, 11, 11, 11)),
        (dict(A0=11, A1=11, A2=11, A3=11), (11, 11, 11, 11)),
    ]
)
def test__set(data, _EXPECTED):
    victim = VictimSet()

    AttrAux_AnnotsAll(victim).sai__by_kwargs(**data)
    for index in range(4):
        Lambda(getattr, victim, f"A{index}").expect__check_assert(_EXPECTED[index])


# =====================================================================================================================
def test__annots_ensure():
    victim = AttrDumped()
    try:
        victim.__annotations__
    except:
        pass
    else:
        assert False

    try:
        victim.__annotations__
    except:
        pass
    else:
        assert False

    AttrAux_AnnotsAll(victim).annots__ensure()
    assert victim.__annotations__ == {}


def test__annots_append():
    # ---------------------------------------------------------
    victim = AttrAux_AnnotsAll().annots__append(astr=str, aint=1)
    assert victim.aint == 1

    try:
        victim.astr
    except:
        pass
    else:
        assert False

    # ---------------------------------------------------------
    victim2 = AttrAux_AnnotsAll().annots__append(astr="hello")
    try:
        victim2.aint
    except:
        pass
    else:
        assert False

    assert victim2.astr == "hello"
    assert victim.__annotations__ != victim2.__annotations__

    # ---------------------------------------------------------
    victim3 = AttrAux_AnnotsAll(victim).annots__append(astr="hello")
    assert victim3.aint == 1
    assert victim3.astr == "hello"

    assert victim.__annotations__ == victim3.__annotations__


# =====================================================================================================================
class Test__SpecialObjects:
    def test__NamedTuple(self):
        class Victim(NamedTuple):
            ATTR1: int
            ATTR2: int = 2

        try:
            victimNT = Victim() # will not need! raised just on NamedTuple!
        except:
            pass
        else:
            assert False

        victimNT = Victim(1)

        assert AttrAux_AnnotsAll(victimNT).annots__get_not_defined() == []
        assert AttrAux_AnnotsAll(victimNT).annots__check_all_defined() == True
        assert AttrAux_AnnotsAll(victimNT).dump_dict__annot_types() == {"ATTR1": int, "ATTR2": int, }
        # assert AttrAux_AnnotsAll(victimNT).dump_dict() == {"ATTR1": 1, "ATTR2": 2, }

    @pytest.mark.skip
    def test__DataClass(self):
        pass


# =====================================================================================================================
def test__zero():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
