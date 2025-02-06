from typing import *
import pytest
import re

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_types.m0_primitives import *

from base_aux.base_patterns.m1_pat_nums import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, fpoint, _EXP_int, _EXP_float, _EXP_both",
    argvalues=[
        # trash ----
        ("", None, (None, None), (None, None), (None, None)),
        ("hello", None, (None, None), (None, None), (None, None)),
        ("he.l,lo", None, (None, None), (None, None), (None, None)),

        ("11,22,33", None, (None, None), (None, None), (None, None)),
        ("11,22,33", ",", (None, None), (None, None), (None, None)),
        ("11.22.33", None, (None, None), (None, None), (None, None)),
        ("11.22.33", ",", (None, None), (None, None), (None, None)),

        # INT ------
        ("123", None, ("123", "123"), (None, None), ("123", "123")),
        ("a123b", None, (None, "123"), (None, None), (None, "123")),

        # FLOAT ----
        ("11,22", None, (None, None), (None, None), (None, None)),
        ("11,22", ",", (None, None), ("11,22", "11,22"), ("11,22", "11,22")),
        ("aa11,22bb", ",", (None, None), (None, "11,22"), (None, "11,22")),

        ("11.22", None, (None, None), ("11.22", "11.22"), ("11.22", "11.22")),
        ("11.22", ",", (None, None), (None, None), (None, None)),

        # MINUS ----
        ("-123", None, ("-123", "-123"), (None, None), ("-123", "-123")),
        ("---123", None, (None, "-123"), (None, None), (None, "-123")),
        ("a-123a", None, (None, "-123"), (None, None), (None, "-123")),
        ("-a---123--a", None, (None, "-123"), (None, None), (None, "-123")),
        ("he-l,lo--11.22--=-asdf", None, (None, None), (None, "-11.22"), (None, "-11.22")),
    ]
)
def test___PatNumber(source, fpoint, _EXP_int, _EXP_float, _EXP_both):
    # INT -----
    match = re.fullmatch(PatNumberSingle(fpoint).INT_EXACT, source)
    ExpectAux(match and match[1]).check_assert(_EXP_int[0])

    match = re.fullmatch(PatNumberSingle(fpoint).INT_COVERED, source)
    ExpectAux(match and match[1]).check_assert(_EXP_int[1])

    # FLOAT -----
    match = re.fullmatch(PatNumberSingle(fpoint).FLOAT_EXACT, source)
    ExpectAux(match and match[1]).check_assert(_EXP_float[0])

    match = re.fullmatch(PatNumberSingle(fpoint).FLOAT_COVERED, source)
    ExpectAux(match and match[1]).check_assert(_EXP_float[1])

    # BOTH -----
    match = re.fullmatch(PatNumberSingle(fpoint).BOTH_EXACT, source)
    ExpectAux(match and match[1]).check_assert(_EXP_both[0])

    match = re.fullmatch(PatNumberSingle(fpoint).BOTH_COVERED, source)
    ExpectAux(match and match[1]).check_assert(_EXP_both[1])


# =====================================================================================================================
