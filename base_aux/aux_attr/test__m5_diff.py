from typing import *
import pytest

from base_aux.aux_attr.m5_attr_diff import *
from base_aux.aux_expect.m1_expect_aux import *


# =====================================================================================================================
class Victim1_Existed:
    # ANE
    AE = 1
    _AE = 11
    __AE = 111


class Victim2_AnnotMiddle(Victim1_Existed):
    AM: int = 2
    _AM: int = 22
    __AM: int = 222


class Victim3_AnnotLast(Victim2_AnnotMiddle):
    AL: int = 3
    _AL: int = 33
    __AL: int = 333


# TODO: ADD INTO PRIMITIVES!!!


# =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="dicts, _EXPECTED",
#     argvalues=[
#         # blank ------------
#         ([{}, ], {}),
#         ([{}, {}], {}),
#         ([{}, {}, {}], {}),
#
#         # diffs ------------
#         ([{1:1}, {1:1}], {}),
#         ([{1: 1}, {1: 11}], {1: (1, 11)}),
#         ([{1: 1}, {1: 11}, {1: 111}], {1: (1, 11, 111)}),
#
#         # NOVALUE ------------
#         ([{1: 1}, {}], {1: (1, VALUE_SPECIAL.NOVALUE)}),
#         ([{1: 1}, {}, {1:11}], {1: (1, VALUE_SPECIAL.NOVALUE, 11)}),
#
#         # EXX ------------
#         ([{1: Exception}, {1: Exception}], {}),
#         ([{1: Exception}, {1: Exception()}], {}),
#         ([{1: Exception()}, {1: Exception}], {}),
#         ([{1: Exception()}, {1: Exception()}], {}),
#
#         ([{1: 1}, {1: Exception}], {1: (1, Exception)}),
#         ([{1: 1}, {1: Exception()}], {1: (1, Exception)}),
#         ([{1: Exx__GetattrPrefix}, {1: Exception}], {1: (Exx__GetattrPrefix, Exception)}),
#         ([{1: Exx__GetattrPrefix()}, {1: Exception()}], {1: (Exx__GetattrPrefix, Exception)}),
#         ([{1: Exx__GetattrPrefix()}, {1: Exx__GetattrPrefix}], {}),
#     ]
# )
# def test__resolve(dicts, _EXPECTED):
#     func_link = lambda: DictDiff(*dicts).resolve()
#     ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
