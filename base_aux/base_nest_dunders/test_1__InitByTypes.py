import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m1_init2_annots2_by_types import *

from base_aux.base_types.m2_info import *


# =====================================================================================================================
class Victim1(NestInit_AnnotsByTypes_All):
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
    argnames="arg, _EXPECTED",
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
def test__all(arg, _EXPECTED):
    Lambda(getattr, victim1, arg).check_expected__assert(_EXPECTED)


# =====================================================================================================================
class Victim2(NestInit_AnnotsByTypes_NotExisted):
    NOTEXIST: int
    EXIST: int = 100


victim2 = Victim2()

@pytest.mark.parametrize(
    argnames="arg, _EXPECTED",
    argvalues=[
        ("NOTEXIST", 0),
        ("EXIST", 100),

        ("NEVER", Exception),
    ]
)
def test__not_existed(arg, _EXPECTED):
    Lambda(getattr, victim2, arg).check_expected__assert(_EXPECTED)


# =====================================================================================================================

if __name__ == "__main__":
    # print(AttrAux_AnnotsAll(victim).dump__dict_types())
    # print(AttrAux_AnnotsAll(victim).dump__dict_values())

    ObjectInfo(victim1.__annotations__["UNION_BOOL_INT"]).print()


# =====================================================================================================================
