import sys
from typing import Union, Any, Callable, NoReturn

from base_aux.aux_attr.m3_getattr1_prefix_1_inst import NestGa_Prefix_RaiseIf
from base_aux.aux_types.m1_type_aux import TypeAux
from base_aux.versions.m2_version import Version


# =====================================================================================================================
class CheckVersion(NestGa_Prefix_RaiseIf):
    SOURCE: Union[Any, Callable[..., Any]] = sys.version.split()[0]
    # print(sys.version_info)   # sys.version_info(major=3, minor=8, micro=10, releaselevel='final', serial=0)
    # return sys.version_info[:3]     # (3, 8, 10)

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, source: Any | Callable | None = None):
        if source is not None:
            self.SOURCE = source

    @property
    def ACTUAL(self) -> Version:
        if TypeAux(self.SOURCE).check__callable_func_meth_inst():
            value = self.SOURCE()
        else:
            value = self.SOURCE

        return Version(value)

    # ---------------------------------------
    def check_eq(self, target: Any):
        return self.ACTUAL == target

    def check_ne(self, target: Any):
        return self.ACTUAL != target

    # ---------------------------------------
    def check_le(self, target: Any):
        return self.ACTUAL <= target

    def check_lt(self, target: Any):
        return self.ACTUAL < target

    # ---------------------------------------
    def check_ge(self, target: Any):
        return self.ACTUAL >= target

    def check_gt(self, target: Any):
        return self.ACTUAL > target


# =====================================================================================================================
class CheckVersion_Python(CheckVersion):
    """
    check version of python interpreter.

    USAGE
    -----
    CheckVersion_Python().raise_if_not__check_ge("2")
    CheckVersion_Python().raise_if_not__check_ge("3.11")
    CheckVersion_Python().raise_if_not__check_ge("3.11rc1", _comment="need Python GRATER EQUAL")
    """
    SOURCE = sys.version.split()[0]

    raise_if__check_eq: Callable[..., NoReturn | None]
    raise_if_not__check_eq: Callable[..., NoReturn | None]

    raise_if__check_ne: Callable[..., NoReturn | None]
    raise_if_not__check_ne: Callable[..., NoReturn | None]

    raise_if__check_le: Callable[..., NoReturn | None]
    raise_if_not__check_le: Callable[..., NoReturn | None]

    raise_if__check_lt: Callable[..., NoReturn | None]
    raise_if_not__check_lt: Callable[..., NoReturn | None]

    raise_if__check_ge: Callable[..., NoReturn | None]
    raise_if_not__check_ge: Callable[..., NoReturn | None]

    raise_if__check_gt: Callable[..., NoReturn | None]
    raise_if_not__check_gt: Callable[..., NoReturn | None]


# =====================================================================================================================
