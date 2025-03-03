from typing import *
import pytest
import re

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m2_wildcard import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # single ----
        ("", ""),
        ("*", ".*"),
        ("?", ".{0,1}"),
        (".", "\."),

        # brackets ----
        ("[]", "\[\]"),
        ("()", "\(\)"),
        ("{}", "\{\}"),

        # multy ----
        ("[*ell?]", "\[.*ell.{0,1}\]"),
    ]
)
def test__regexp(source, _EXPECTED):
    func_link = WildCardMask(source).to_regexp
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="wmask, _EXPECTED_pat, other, _EXPECTED_other",
    argvalues=[
        # multy ----
        ("[*ell?]", "\[.*ell.{0,1}\]", "[ell]", True),
        ("[*ell?]", "\[.*ell.{0,1}\]", "[hello]", True),
        ("[*ell?]", "\[.*ell.{0,1}\]", "[123hello]", True),
        ("[*ell?]", "\[.*ell.{0,1}\]", "[123hello123]", False),
    ]
)
def test__fullmatch(wmask, _EXPECTED_pat, other, _EXPECTED_other):
    pat = WildCardMask(wmask).to_regexp()
    ExpectAux(pat).check_assert(_EXPECTED_pat)

    assert bool(re.fullmatch(pattern=pat, string=other)) == _EXPECTED_other


# =====================================================================================================================
