from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *
from base_aux.aux_attr.m5_attr_diff import *

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *
from base_aux.aux_attr.m0_static import *

from base_aux.aux_values.m2_value_special import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source1, source2, _EXPECTED",
    argvalues=[
        (
                AttrKit_Blank(),
                AttrKit_Blank(),
                [
                    {},
                    {},
                    {},
                ]
        ),
        (
                ExampleAttrs1_Existed(),
                ExampleAttrs1_Existed(),
                [
                    {},
                    {},
                    {},
                ]
        ),
        (
                ExampleAttrs1_Existed(),
                ExampleAttrs21_AnnotMiddle(),
                [
                    {'AN2': (NoValue, 2), '_AN2': (NoValue, 22), '_meth2': (NoValue, 22), 'meth2': (NoValue, 2)},
                    {'AN2': (NoValue, 2), '_AN2': (NoValue, 22), '_meth2': (NoValue, 22), 'meth2': (NoValue, 2)},
                    {},
                ]
        ),

    ]
)
def test__names(source1, source2, _EXPECTED):
    ExpectAux(AttrDiff_Existed(source1, source2)).check_assert(_EXPECTED[0])
    ExpectAux(AttrDiff_AnnotsAll(source1, source2)).check_assert(_EXPECTED[1])
    # ExpectAux(AttrDiff_AnnotsLast(source1, source2)).check_assert(_EXPECTED[2])


# =====================================================================================================================
