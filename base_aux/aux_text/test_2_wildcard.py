from typing import *
import pytest
import re

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_text.m2_wildcard import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # single ----
        ("", r""),
        ("*", r".*"),
        ("?", r".{0,1}"),
        (".", r"\."),

        # brackets ----
        ("[]", r"\[\]"),
        ("()", r"\(\)"),
        ("{}", r"\{\}"),

        # multy ----
        ("[*ell?]", r"\[.*ell.{0,1}\]"),
    ]
)
def test__regexp(source, _EXPECTED):
    func_link = WildCardMask(source).to_regexp
    Lambda(func_link).check_expected__assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="wmask, _EXPECTED_pat, other, _EXPECTED_other",
    argvalues=[
        # multy ----
        ("[*ell?]", r"\[.*ell.{0,1}\]", "[ell]", True),
        ("[*ell?]", r"\[.*ell.{0,1}\]", "[hello]", True),
        ("[*ell?]", r"\[.*ell.{0,1}\]", "[123hello]", True),
        ("[*ell?]", r"\[.*ell.{0,1}\]", "[123hello123]", False),
    ]
)
def test__fullmatch(wmask, _EXPECTED_pat, other, _EXPECTED_other):
    pat = WildCardMask(wmask).to_regexp()
    Lambda(pat).check_expected__assert(_EXPECTED_pat)

    assert bool(re.fullmatch(pattern=pat, string=other)) == _EXPECTED_other


# =====================================================================================================================
