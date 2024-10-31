from typing import *
import pathlib

import pytest
from pytest import mark
from pytest_aux import *

from PRJ_NEW__ import *


# =====================================================================================================================
def func_example(arg1: Any, arg2: Any) -> str:
    return f"{arg1}{arg2}"


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[int, ])
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED",
    argvalues=[
        (("1", ), 1),
        (("hello", ), Exception),
    ]
)
def test__short_variant(func_link, args, _EXPECTED):
    pytest_func_tester(func_link, args, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="args, kwargs, _EXPECTED, _MARK, _COMMENT",
    argvalues=[
        # TRIVIAL -------------
        ((1, None), {}, "1None", None, "ok"),
        ((1, 2), {}, "12", None, "ok"),

        # LIST -----------------
        ((1, []), {}, "1[]", None, "ok"),

        # MARKS -----------------
        ((1, 2), {}, None, mark.skip, "skip"),
        ((1, 2), {}, None, mark.skipif(True), "skip"),
        ((1, 2), {}, "12", mark.skipif(False), "ok"),
        ((1, 2), {}, None, mark.xfail, "ok"),
        ((1, 2), {}, "12", mark.xfail, "SHOULD BE FAIL!"),
    ]
)
@pytest.mark.parametrize(argnames="func_link", argvalues=[func_example, ])
def test__long_variant(func_link, args, kwargs, _EXPECTED, _MARK, _COMMENT):
    pytest_func_tester(func_link, args, kwargs, _EXPECTED, _MARK, _COMMENT)


# =====================================================================================================================
