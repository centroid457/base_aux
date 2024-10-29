from typing import *
import pytest

from base_aux.funcs_aux import *
from base_aux.classes_aux import *


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
            class Victim(AnnotAllDefined, NamedTuple):
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
