import pytest

from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_attr.m2_annot3_gacls_keys_as_values import *


# =====================================================================================================================
class VictimCs(NestGaCls_AnnotNamesAsValuesCs):
    ATTR1: str
    ATTR2: str


class VictimIc(NestGaCls_AnnotNamesAsValuesIc):
    ATTR1: str
    ATTR2: str


Victim_VALUES = ("ATTR1", "ATTR2")


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ("ATTR1", ["ATTR1", "ATTR1"]),
        ("attr1", [AttributeError, "ATTR1"]),

        ("ATTR2", ["ATTR2", "ATTR2"]),
        ("notExists", [AttributeError, AttributeError]),
        ("use spaces", [AttributeError, AttributeError]),
    ]
)
@pytest.mark.parametrize(argnames="Victim", argvalues=[VictimCs, VictimIc])
def test__ga(Victim, args, _EXPECTED):
    exp_index = 0
    if Victim is VictimCs:
        exp_index = 0
    elif Victim is VictimIc:
        exp_index = 1

    func_link = lambda value: getattr(Victim, value)
    Lambda(func_link, args).expect__check_assert(_EXPECTED[exp_index])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        # INDEX ------
        (0, ["ATTR1", "ATTR1"]),
        (1, ["ATTR2", "ATTR2"]),
        (2, [IndexError, IndexError]),
        (-1, ["ATTR2", "ATTR2"]),
        (-2, ["ATTR1", "ATTR1"]),
        (-3, [IndexError, IndexError]),

        # ITEM ------
        ("ATTR1", ["ATTR1", "ATTR1"]),
        ("attr1", [AttributeError, "ATTR1"]),
        ("notExists", [AttributeError, AttributeError]),
        ("use spaces", [AttributeError, AttributeError]),
    ]
)
@pytest.mark.parametrize(argnames="Victim", argvalues=[VictimCs, VictimIc])
def test__gi(Victim, args, _EXPECTED):
    exp_index = 0
    if Victim is VictimCs:
        exp_index = 0
    elif Victim is VictimIc:
        exp_index = 1

    func_link = lambda value: Victim[value]
    Lambda(func_link, args).expect__check_assert(_EXPECTED[exp_index])


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ("ATTR1", [True, True]),
        ("attr1", [False, True]),
        ("notExists", [False, False]),
        ("use spaces", [False, False]),
    ]
)
@pytest.mark.parametrize(argnames="Victim", argvalues=[VictimCs, VictimIc])
def test__in(Victim, args, _EXPECTED):
    exp_index = 0
    if Victim is VictimCs:
        exp_index = 0
    elif Victim is VictimIc:
        exp_index = 1

    func_link = lambda value: value in Victim
    Lambda(func_link, args).expect__check_assert(_EXPECTED[exp_index])


# =====================================================================================================================
def test__iter():
    assert tuple(VictimCs) == Victim_VALUES
    assert tuple(VictimIc) == Victim_VALUES


def test__len():
    assert len(VictimCs) == len(Victim_VALUES)
    assert len(VictimIc) == len(Victim_VALUES)

def test__str_repr():
    assert str(VictimCs) == str(Victim_VALUES) == "('ATTR1', 'ATTR2')"
    assert repr(VictimCs) == f"VictimCs{Victim_VALUES}" == "VictimCs('ATTR1', 'ATTR2')"

    assert str(VictimIc) == str(Victim_VALUES) == "('ATTR1', 'ATTR2')"
    assert repr(VictimIc) == f"VictimIc{Victim_VALUES}" == "VictimIc('ATTR1', 'ATTR2')"


# =====================================================================================================================
