from typing import *
import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_attr.m4_dump1_dumping1_dict import *
from base_aux.aux_attr.m0_static import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, skip_names, _EXPECTED",
    argvalues=[
        (ExampleAttrs1_Existed(), [], [
            {"AE1": 1, "_AE1": 11, 'meth1': 1, '_meth1': 11},
            {},
            {}
        ]),
        (ExampleAttrs21_AnnotMiddle(), [], [
            {
                "AE1": 1, "_AE1": 11, 'meth1': 1, '_meth1': 11,
                "AN2": 2, "_AN2": 22, 'meth2': 2, '_meth2': 22,
            },
            {"AN2": 2, "_AN2": 22},
            {"AN2": 2, "_AN2": 22}
        ]),
        (ExampleAttrs321_AnnotLast(), [], [
            {
                "AE1": 1, "_AE1": 11, 'meth1': 1, '_meth1': 11,
                "AN2": 2, "_AN2": 22, 'meth2': 2, '_meth2': 22,
                "AN3": 3, "_AN3": 33, 'meth3': 3, '_meth3': 33,
            },
            {"AN2": 2, "_AN2": 22, "AN3": 3, "_AN3": 33},
            {"AN3": 3, "_AN3": 33}]),
    ]
)
def test__names(source, skip_names, _EXPECTED):
    Lambda(AttrDictDumping_Existed(source)(*skip_names)).expect__check_assert(_EXPECTED[0])
    Lambda(AttrDictDumping_AnnotsAll(source)(*skip_names)).expect__check_assert(_EXPECTED[1])
    Lambda(AttrDictDumping_AnnotsLast(source)(*skip_names)).expect__check_assert(_EXPECTED[2])


# =====================================================================================================================
