from typing import *
import pytest

from base_aux.aux_dict.m1_dict_aux import *
from base_aux.aux_dict.m4_dict_diff import *
from base_aux.lambdas.m1_lambda import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="dicts, _EXPECTED",
    argvalues=[
        # blank ------------
        ([{}, ], {}),
        ([{}, {}], {}),
        ([{}, {}, {}], {}),

        # diffs ------------
        ([{1:1}, {1:1}], {}),
        ([{1: 1}, {1: 11}], {1: (1, 11)}),
        ([{1: 1}, {1: 11}, {1: 111}], {1: (1, 11, 111)}),

        # NOVALUE ------------
        ([{1: 1}, {}], {1: (1, VALUE_SPECIAL.NOVALUE)}),
        ([{1: 1}, {}, {1:11}], {1: (1, VALUE_SPECIAL.NOVALUE, 11)}),

        # EXX ------------
        ([{1: Exception}, {1: Exception}], {}),
        ([{1: Exception}, {1: Exception()}], {}),
        ([{1: Exception()}, {1: Exception}], {}),
        ([{1: Exception()}, {1: Exception()}], {}),

        ([{1: 1}, {1: Exception}], {1: (1, Exception)}),
        ([{1: 1}, {1: Exception()}], {1: (1, Exception)}),
        ([{1: Exx__GetattrPrefix}, {1: Exception}], {1: (Exx__GetattrPrefix, Exception)}),
        ([{1: Exx__GetattrPrefix()}, {1: Exception()}], {1: (Exx__GetattrPrefix, Exception)}),
        ([{1: Exx__GetattrPrefix()}, {1: Exx__GetattrPrefix}], {}),
    ]
)
def test__resolve(dicts, _EXPECTED):
    func_link = lambda: DictDiff(*dicts).resolve()
    Lambda(func_link).expect__check_assert(_EXPECTED)


# =====================================================================================================================
