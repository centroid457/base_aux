import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux
from base_aux.aux_attr.m2_annot5_init import *
from base_aux.aux_values.m1_explicit import *

from base_aux.aux_types.m2_info import *


# =====================================================================================================================
class Victim1(AnnotsInitByTypes_All):
    NONE: None
    BOOL: bool
    INT: int
    FLOAT: float
    STR: str
    BYTES: bytes
    TUPLE: tuple
    LIST: list
    SET: set
    DICT: dict

    OPTIONAL: Optional
    OPTIONAL_BOOL: Optional[bool]

    # UNION: Union
    UNION_BOOL_INT: Union[bool, int]


victim1 = Victim1()


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ("NONE", None),
        ("BOOL", False),
        ("INT", 0),
        ("FLOAT", 0.0),
        ("STR", ""),
        ("BYTES", b""),
        ("TUPLE", ()),
        ("LIST", []),
        ("SET", set()),
        ("DICT", dict()),

        ("OPTIONAL", None),
        ("OPTIONAL_BOOL", None),
        ("UNION_BOOL_INT", False),

        ("NEVER", Exception),
    ]
)
def test__all(args, _EXPECTED):
    func_link = lambda attr: getattr(victim1, attr)
    PytestAux(func_link, args).assert_check(_EXPECTED)


# =====================================================================================================================
class Victim2(AnnotsInitByTypes_NotExisted):
    NOTEXIST: int
    EXIST: int = 100


victim2 = Victim2()

@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        ("NOTEXIST", 0),
        ("EXIST", 100),

        ("NEVER", Exception),
    ]
)
def test__not_existed(args, _EXPECTED):
    func_link = lambda attr: getattr(victim2, attr)
    PytestAux(func_link, args).assert_check(_EXPECTED)


# =====================================================================================================================

if __name__ == "__main__":
    # print(AnnotsAux(victim).dump__dict_types())
    # print(AnnotsAux(victim).dump__dict_values())

    ObjectInfo(victim1.__annotations__["UNION_BOOL_INT"]).print()


# =====================================================================================================================
