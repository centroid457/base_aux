from typing import *
import pytest

from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *
from base_aux.aux_attr.m0_static import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (ExampleAttrs1_Existed(), [], [{"AE1": 1, "_AE1": 11}, {}, {}]),
        (ExampleAttrs2_AnnotMiddle(), [], [{"AN2": 2, "_AN2": 22}, {"AN2": 2, "_AN2": 22}, {"AN2": 2, "_AN2": 22}]),
        (ExampleAttrs32_AnnotLast(), [], [{"AN2": 2, "_AN2": 22, "AN3": 3, "_AN3": 33}, {"AN2": 2, "_AN2": 22, "AN3": 3, "_AN3": 33}, {"AN3": 3, "_AN3": 33}]),
        (ExampleAttrs0321(), [], [{"AE1": 1, "_AE1": 11, "AN2": 2, "_AN2": 22, "AN3": 3, "_AN3": 33}, {"AN2": 2, "_AN2": 22, "AN3": 3, "_AN3": 33}, {}]),
    ]
)
def test__names(source, skip_names, _EXPECTED):
    ExpectAux(AttrDictDumping_Existed(source)(*skip_names)).check_assert(_EXPECTED[0])
    ExpectAux(AttrDictDumping_AnnotsAll(source)(*skip_names)).check_assert(_EXPECTED[1])
    ExpectAux(AttrDictDumping_AnnotsLast(source)(*skip_names)).check_assert(_EXPECTED[2])


# =====================================================================================================================
