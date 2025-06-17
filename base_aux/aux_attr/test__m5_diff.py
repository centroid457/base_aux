from typing import *
import pytest

from base_aux.aux_attr.m5_attr_diff import *
from base_aux.aux_expect.m1_expect_aux import *


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
