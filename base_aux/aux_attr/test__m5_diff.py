from typing import *
import pytest

from base_aux.aux_attr.m4_kits import *
from base_aux.aux_attr.m5_attr_diff import *

from base_aux.aux_callable.m2_lambda import *
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
                    {
                        'AN2': (NoValue, 2), '_AN2': (NoValue, 22), 'meth2': (NoValue, 2), '_meth2': (NoValue, 22),
                    },
                    {
                        'AN2': (NoValue, 2), '_AN2': (NoValue, 22),
                    },
                    {
                        'AN2': (NoValue, 2), '_AN2': (NoValue, 22),
                    },
                ]
        ),
        (
                ExampleAttrs1_Existed(),
                ExampleAttrs321_AnnotLast(),
                [
                    {
                        'AN2': (NoValue, 2), '_AN2': (NoValue, 22), 'meth2': (NoValue, 2), '_meth2': (NoValue, 22),
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33), 'meth3': (NoValue, 3), '_meth3': (NoValue, 33),
                    },
                    {
                        'AN2': (NoValue, 2), '_AN2': (NoValue, 22),
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33),
                    },
                    {
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33),
                    },
                ]
        ),
        (
                ExampleAttrs21_AnnotMiddle(),
                ExampleAttrs321_AnnotLast(),
                [
                    {
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33), 'meth3': (NoValue, 3), '_meth3': (NoValue, 33),
                    },
                    {
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33),
                    },
                    {
                        'AN2': (2, NoValue), '_AN2': (22, NoValue),
                        'AN3': (NoValue, 3), '_AN3': (NoValue, 33),
                    },
                ]
        ),
    ]
)
def test__names(source1, source2, _EXPECTED):
    Lambda(AttrDiff_Existed(source1, source2)).expect__check_assert(_EXPECTED[0])
    Lambda(AttrDiff_AnnotsAll(source1, source2)).expect__check_assert(_EXPECTED[1])
    Lambda(AttrDiff_AnnotsLast(source1, source2)).expect__check_assert(_EXPECTED[2])


# =====================================================================================================================
