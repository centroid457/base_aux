from typing import *
import pytest

from base_aux.pytester import *
from base_aux.classes import *


# =====================================================================================================================
class Victim1(AnnotAux):
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
class VictimDirect_Ok(AnnotAux):
    ATTR1: int = 1
    ATTR2: int = 2


class VictimDirect_Fail(AnnotAux):
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
class DictDirect_Ok(dict, AnnotAux):
    ATTR1: int = 1
    ATTR2: int = 2


class DictDirect_Fail(dict, AnnotAux):
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
    assert AnnotAux.annot__get_not_defined(source) == _EXPECTED

    func_link = source.annot__get_not_defined
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


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
    assert AnnotAux.annot__check_all_defined(source) == _EXPECTED

    func_link = source.annot__check_all_defined
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


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
    try:
        AnnotAux.annot__raise_if_not_defined(source)
        assert _EXPECTED is None
    except:
        assert _EXPECTED == Exception

    func_link = source.annot__raise_if_not_defined
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class Test__Cmp:
    @classmethod
    def setup_class(cls):
        pass
        cls.victim1 = Victim1()
        cls.victim2 = Victim2()    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    def setup_method(self, method):
        pass

    # def teardown_method(self, method):
    #     pass

    # =================================================================================================================
    def test__anycase_getattr(self):
        assert self.victim2.ATTR2 == 2
        assert self.victim2.attr2 == 2

    def test__anycase_getitem(self):
        assert self.victim2["ATTR2"] == 2
        assert self.victim2["attr2"] == 2

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="asker, source, _EXPECTED",
        argvalues=[
            (victim1, None, VICTIM1_DICT_TYPES),
            (victim1, victim1, VICTIM1_DICT_TYPES),
            (victim2, victim1, VICTIM1_DICT_TYPES),
            (AnnotAux, victim1, VICTIM1_DICT_TYPES),

            (victim2, None, VICTIM2_DICT_TYPES),
            (victim2, victim2, VICTIM2_DICT_TYPES),
            (victim1, victim2, VICTIM2_DICT_TYPES),
            (AnnotAux, victim2, VICTIM2_DICT_TYPES),
        ]
    )
    def test__dict_types(self, asker, source, _EXPECTED):
        func_link = asker.annot__get_nested__dict_types
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="asker, source, _EXPECTED",
        argvalues=[
            (victim1, None, VICTIM1_DICT_VALUES),
            (victim1, victim1, VICTIM1_DICT_VALUES),
            (victim2, victim1, VICTIM1_DICT_VALUES),
            (AnnotAux, victim1, VICTIM1_DICT_VALUES),

            (victim2, None, VICTIM2_DICT_VALUES),
            (victim2, victim2, VICTIM2_DICT_VALUES),
            (victim1, victim2, VICTIM2_DICT_VALUES),
            (AnnotAux, victim2, VICTIM2_DICT_VALUES),
        ]
    )
    def test__dict_values(self, asker, source, _EXPECTED):
        func_link = asker.annot__get_nested__dict_values
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="asker, source, _EXPECTED",
        argvalues=[
            (victim1, None, list(VICTIM1_DICT_VALUES.values())),
            (victim1, victim1, list(VICTIM1_DICT_VALUES.values())),
            (victim2, victim1, list(VICTIM1_DICT_VALUES.values())),
            (AnnotAux, victim1, list(VICTIM1_DICT_VALUES.values())),

            (victim2, None, list(VICTIM2_DICT_VALUES.values())),
            (victim2, victim2, list(VICTIM2_DICT_VALUES.values())),
            (victim1, victim2, list(VICTIM2_DICT_VALUES.values())),
            (AnnotAux, victim2, list(VICTIM2_DICT_VALUES.values())),
        ]
    )
    def test__iter_values(self, asker, source, _EXPECTED):
        func_link = lambda arg: list(asker.annot__iter_values(arg))
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="asker, source, _EXPECTED",
        argvalues=[
            (victim1, None, False),
            (victim1, victim1, False),
            (victim2, victim1, False),
            (AnnotAux, victim1, False),

            (victim2, None, False),
            (victim2, victim2, False),
            (victim1, victim2, False),
            (AnnotAux, victim2, False),
        ]
    )
    def test__all_defined(self, asker, source, _EXPECTED):
        func_link = asker.annot__check_all_defined
        pytest_func_tester__no_kwargs(func_link, source, _EXPECTED)


# =====================================================================================================================
def test__all_defined2():
    class Victim11(AnnotAux):
        ATTR1: int = 1
        ATTR2: int = 2
        ATTR01 = 11

    victim11 = Victim11()
    assert victim1.annot__check_all_defined() == False
    assert victim11.annot__check_all_defined() == True


# =====================================================================================================================
class Test__NamedTuple:
    def test__NT(self):
        try:
            class Victim(AnnotRequired, NamedTuple):
                ATTR1: int
                ATTR2: int = 2
            assert False
        except TypeError:
            # TypeError: can only inherit from a NamedTuple type and Generic
            pass

    @pytest.mark.skip   # seems its not need
    def test__NT_by_obj(self):
        class Victim(NamedTuple):
            ATTR1: int
            ATTR2: int = 2

        victimNT = Victim(1)

        assert AnnotAux().annot__get_not_defined(victimNT) == ["ATTR1", ]
        assert AnnotAux().annot__check_all_defined(victimNT) == False
        assert AnnotAux().annot__get_nested__dict_types(victimNT) == {"ATTR1": int, }
        assert AnnotAux().annot__get_nested__dict_values(victimNT) == {"ATTR1": 1, }


# =====================================================================================================================
