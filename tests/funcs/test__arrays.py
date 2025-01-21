import pytest

from base_aux.aux_pytester.m1_pytest_aux import *
from base_aux.aux_arrays.m1_arrays_aux import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source,p2,p3,p4,p5,_EXPECTED",
    argvalues=[
        (np.array([[1, 2, ], [1, 2, ]]), None, None, None, None, "12\n12"),
        (np.array([[1, 2, ], [1, 2, ]]), {1: "#"}, None, None, None, "#2\n#2"),
        (np.array([[1, 2, ], [1, 2, ]]), None, 1, None, None, "12\n\n12"),
        (np.array([[1, 2, ], [1, 2, ]]), None, None, True, None, "==\n12\n12\n=="),
        (np.array([[1, 2, ], [1, 2, ]]), None, None, None, True, "1   12\n2   12"),
    ])
def test__array_2d_get_compact_str(source, p2, p3, p4, p5, _EXPECTED):
    funk_link = ArrayAux(source).d2_get_compact_str
    PytestAux(funk_link, kwargs=dict(interpreter=p2, separate_rows=p3, wrap=p4, use_rows_num=p5)).assert_check(_EXPECTED)


# =====================================================================================================================
