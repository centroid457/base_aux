import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m5_re2_attemps import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, pat, _EXPECTED",
    argvalues=[
        ("abc123", r"hello", Exception),
        ("abc123", r"\d+", "123"),
        ("abc123", r"\d(\d)\d", "2"),
        ("abc123", r"\d(\d)(\d)", ("2", "3")),
    ]
)
def test__result_get_from_match(source, pat, _EXPECTED):
    match = re.search(pat, source)
    func_link = Base_ReAttempts._result__get_from_match
    ExpectAux(func_link, match).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__re:
    @pytest.mark.parametrize(
        argnames="source, attempts, _EXPECTED",
        argvalues=[
            ("abc123", (r"\d+", r"\D+"), "abc"),
        ]
    )
    def test__match(self, source, attempts, _EXPECTED):
        func_link = ReAttemptsFirst(*attempts).match
        ExpectAux(func_link, source).check_assert(_EXPECTED)


# =====================================================================================================================
