from typing import *
import pytest
from dataclasses import dataclass

from base_aux.classes import *


# =====================================================================================================================
def test__raise():
    class Victim(AnnotRequired):
        ATTR1: int
        ATTR2: int = 2

    try:
        Victim()
        assert False
    except Exx__AnnotNotDefined:
        assert True


def test__ok():
    class Victim(AnnotRequired):
        ATTR1: int = 1
        ATTR2: int = 2

    try:
        Victim()
        assert True
    except Exx__AnnotNotDefined:
        assert False
    except:
        assert False


# =====================================================================================================================
# @pytest.mark.skip
# class Test:
#     # FIXME: make a ref!
#     # -----------------------------------------------------------------------------------------------------------------
#     def test__dataclass(self):
#         @dataclass
#         class Cls(AnnotRequired):
#             ATTR1: int
#             ATTR2: int = 2
#
#         assert Cls(1).annots_get_set() == {"ATTR1", }
#         assert Cls(1).annots_get_dict() == {"ATTR1": 1, }
#
#     def test__dataclass_by_obj(self):
#         # 10------------------
#         @dataclass
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#         class Cls2(Cls):
#             ATTR2: int = 22
#             ATTR3: int = 33
#
#         obj = Cls2(1)
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#         assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#
#         # 01------------------
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#         @dataclass
#         class Cls2(Cls):
#             ATTR2: int = 22
#             ATTR3: int = 33
#
#         obj = Cls2(1)
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#         try:
#             assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#         except Exx__AnnotNotDefined:
#             pass   # its GOOD!!!
#         else:
#             assert False
#
#         # 11------------------
#         @dataclass
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#         @dataclass
#         class Cls2(Cls):
#             ATTR2: int = 22
#             ATTR3: int = 33
#
#         obj = Cls2(1)
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#         assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#
#     def test__PROPERTY_w_ITER_w_VALUES(self):
#         # 1---------------------------------------------------------
#         # this will work correctly
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#             @property
#             def meth_as_property(self):
#                 return 333
#
#         obj = Cls()
#         obj.ATTR1 = 1
#
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#         assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#         assert list(AnnotRequired().annots_get_values(obj)) == [1, ]
#
#         # 2---------------------------------------------------------
#         # this will RAISE!
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#             @property
#             def meth_as_property(self):
#                 return sum(self)
#
#             def __iter__(self):
#                 yield from AnnotRequired().annots_get_values(self)
#
#         obj = Cls()
#         obj.ATTR1 = 1
#
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#
#         try:
#             assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#             # assert list(AnnotRequired().annots_get_values(obj)) == [1, ]
#         except RecursionError:
#             pass
#         else:
#             assert False
#
#         # 3 FIXED---------------------------------------------------------
#         # this will work correctly!
#         class Cls:
#             ATTR1: int
#             ATTR2: int = 2
#
#             def meth_NO_property(self):
#                 return sum(self)
#
#             def __iter__(self):
#                 yield from AnnotRequired().annots_get_values(self)
#
#         obj = Cls()
#         obj.ATTR1 = 1
#
#         assert AnnotRequired().annots_get_set(obj) == {"ATTR1", }
#         assert AnnotRequired().annots_get_dict(obj) == {"ATTR1": 1, }
#         assert list(AnnotRequired().annots_get_values(obj)) == [1, ]


# =====================================================================================================================
