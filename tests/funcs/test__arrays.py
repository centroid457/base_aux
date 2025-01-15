import numpy as np
import pytest

from base_aux.funcs import *


# =====================================================================================================================
STR_EXCEPTION_MARK = "***STR_EXCEPTION_MARK***"


# =====================================================================================================================
# !!!!!!!!!!!!!!!!!!!!!!! ТИПОВОЙ ПРИМЕР РАБОТЫ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @pytest.mark.parametrize(
#     argnames="p1,_func_result,EXPECTED,_EXPECT_COMPARE",   #_EXPECT_COMPARE=ожидание по сравнению
#     argvalues=[
#         (None, None, {}, True),       # BLANK input
#         ({}, None, {}, True),
#
#         ({1: 1}, None, {1: 1}, True),   # exact input
#         ({"a": "a"}, None, {"a": "a"}, True),
#
#         (None, lambda r: r.abc, None, True),  # ACCESS KEYS
#         ({}, lambda r: r.abc, None, True),
#         ({1: 1}, lambda r: r.abc, None, True),
#         ({"abc": 1}, lambda r: r.abc, 1, True),
#
#         ({}, str, "{}", True),  # STR
#         ({1: 1}, str, "{1: 1}", True),
#         ({1: 1, "a": "a"}, str, "{1: 1, 'a': 'a'}", True),
#     ])
# def test__DictDotAttrAccess(p1, _func_result, EXPECTED, _EXPECT_COMPARE):  # starichenko
#     test_obj_link = UFU.DictDotAttrAccess
#
#     if _func_result is None:
#         result_func_link = lambda i: i
#     else:
#         result_func_link = _func_result
#
#     try:
#         if p1 is None:
#             result = result_func_link(test_obj_link())
#         else:
#             result = result_func_link(test_obj_link(p1))
#     except:
#         result = UFU.STR_EXCEPTION_MARK
#
#     assert (result == EXPECTED) == _EXPECT_COMPARE


# =====================================================================================================================
class Test__np:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="p1,p2,p3,p4,p5,_func_result,EXPECTED,_EXPECT_COMPARE",
        argvalues=[
            (np.array([[1, 2, ], [1, 2, ]]), None, None, None, None, None, "12\n12", True),
            (np.array([[1, 2, ], [1, 2, ]]), {1: "#"}, None, None, None, None, "#2\n#2", True),
            (np.array([[1, 2, ], [1, 2, ]]), None, 1, None, None, None, "12\n\n12", True),
            (np.array([[1, 2, ], [1, 2, ]]), None, None, True, None, None, "==\n12\n12\n==", True),
            (np.array([[1, 2, ], [1, 2, ]]), None, None, None, True, None, "1   12\n2   12", True),
        ])
    def test__array_2d_get_compact_str(self, p1, p2, p3, p4, p5, _func_result, _EXPECTED, _EXPECT_COMPARE):
        test_obj_link = array_2d_get_compact_str

        if _func_result is None:
            _func_result = lambda i: i

        try:
            result = _func_result(test_obj_link(array=p1, interpreter=p2, separate_rows=p3, wrap=p4, use_rows_num=p5))
        except:
            result = STR_EXCEPTION_MARK

        assert (result == _EXPECTED) == _EXPECT_COMPARE


# =====================================================================================================================
