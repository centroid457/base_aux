from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *
from base_aux.aux_attr.m5_attr_diff import *
from base_aux.aux_expect.m1_expect_aux import *

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *
from base_aux.aux_attr.m0_static import *


# =====================================================================================================================













# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, other, _EXPECTED",
    argvalues=[
        # (att, [], {"AE1": 1, "_AE1": 11}),
    ]
)
def test__names(source, other, _EXPECTED):
    ExpectAux(AttrDiff_Existed).check_assert(_EXPECTED)


# =====================================================================================================================
