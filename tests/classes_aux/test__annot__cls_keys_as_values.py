import pytest

from base_aux.funcs_aux import *
from base_aux.classes_aux import *


# =====================================================================================================================
class Victim(AnnotClsKeysAsValues):
    ATTR1: str
    ATTR2: str
    ATTR3: str


Victim_VALUES = ("ATTR1", "ATTR2", "ATTR3")


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ("ATTR1", "ATTR1"),
        ("attr1", AttributeError),

        ("ATTR2", "ATTR2"),
        ("notExists", AttributeError),
        ("use spaces", AttributeError),
    ]
)
def test__values(args, _EXPECTED):
    func_link = lambda value: getattr(Victim, value)
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (0, "ATTR1"),
        (1, "ATTR2"),
        (2, "ATTR3"),
        (3, IndexError),
        (-1, "ATTR3"),
        (-2, "ATTR2"),
        (-3, "ATTR1"),
        (-4, IndexError),
    ]
)
def test__geitem(args, _EXPECTED):
    func_link = lambda value: Victim[value]
    pytest_func_tester__no_kwargs(func_link, args, _EXPECTED)


def test__iter():
    assert tuple(Victim) == Victim_VALUES


def test__len():
    assert len(Victim) == len(Victim_VALUES)


def test__in():
    assert "attr1" not in Victim
    assert "ATTR1" in Victim
    assert "ATTR2" in Victim


def test__str_repr():
    assert str(Victim) == str(Victim_VALUES) == "('ATTR1', 'ATTR2', 'ATTR3')"
    assert repr(Victim) == f"Victim{Victim_VALUES}" == "Victim('ATTR1', 'ATTR2', 'ATTR3')"


# =====================================================================================================================
