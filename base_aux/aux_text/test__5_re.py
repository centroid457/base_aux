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
            # GROUPS-NO --------
            ("aaa111bbb222", [r"\d+", ], [
                None, [],
                None, [],
                "111", ["111", ],
                ["111", "222"], ["111", "222", ],
                "aaabbb", "aaabbb",
            ]),
            ("aaa111bbb222", [r"\d+", r"\d+"], [        # same rexp
                None, [],
                None, [],
                "111", ["111", "111"],
                ["111", "222"], ["111", "222", "111", "222"],
                "aaabbb", "aaabbb",
            ]),
            ("aaa111bbb222", [r"\d+", r"\D+"], [
                "aaa", ["aaa", ],
                None, [],
                "111", ["111", "aaa"],
                ["111", "222"], ["111", "222", "aaa", "bbb"],
                "aaabbb", "",
            ]),

            # groups-ONE --------
            ("aaa111bbb222", [r"b(\d+)", ], [
                None, [],
                None, [],
                "222", ["222", ],
                ["222"], ["222", ],
                "aaa111bb", "aaa111bb",
            ]),
            # groups-several --------
            ("aaa111bbb222", [r"(\d+)\D+(\d+)", ], [
                None, [],
                None, [],
                ("111", "222"), [("111", "222"), ],
                [("111", "222")], [("111", "222"), ],
                "aaa", "aaa",
            ]),

            # groups-several --------
            ("aaa111bbb222", [RExp(r"(\D+)(\d+)", sub=r"\2\1"), ], [
                ("aaa", "111"), [("aaa", "111"), ],
                None, [],
                ("aaa", "111"), [("aaa", "111"), ],
                [("aaa", "111"), ("bbb", "222")], [("aaa", "111"), ("bbb", "222"), ],
                "111aaa222bbb", "111aaa222bbb",
            ]),
        ]
    )
    def test__match(self, source, attempts, _EXPECTED):
        ExpectAux(ReAttemptsFirst(*attempts).match, source).check_assert(_EXPECTED[0])
        ExpectAux(ReAttemptsAll(*attempts).match, source).check_assert(_EXPECTED[1])

        ExpectAux(ReAttemptsFirst(*attempts).fullmatch, source).check_assert(_EXPECTED[2])
        ExpectAux(ReAttemptsAll(*attempts).fullmatch, source).check_assert(_EXPECTED[3])

        ExpectAux(ReAttemptsFirst(*attempts).search, source).check_assert(_EXPECTED[4])
        ExpectAux(ReAttemptsAll(*attempts).search, source).check_assert(_EXPECTED[5])

        ExpectAux(ReAttemptsFirst(*attempts).findall, source).check_assert(_EXPECTED[6])
        ExpectAux(ReAttemptsAll(*attempts).findall, source).check_assert(_EXPECTED[7])

        ExpectAux(ReAttemptsFirst(*attempts).sub, source).check_assert(_EXPECTED[8])
        ExpectAux(ReAttemptsAll(*attempts).sub, source).check_assert(_EXPECTED[9])
        ExpectAux(ReAttemptsFirst(*attempts).delete, source).check_assert(_EXPECTED[8])
        ExpectAux(ReAttemptsAll(*attempts).delete, source).check_assert(_EXPECTED[9])

    @pytest.mark.parametrize(
        argnames="source, attempts, _EXPECTED",
        argvalues=[
            ("aaa111bbb222", [RExp(r"(\D+)(\d+)", sub=r"\2\1"), ], [
                "111aaa222bbb", "111aaa222bbb",
            ]),
            ("aaa111bbb222", [RExp(r"(\D+)(\d+)", sub=r"\2\1", scount=1), ], [
                "111aaabbb222", "111aaabbb222",
            ]),

            ("aaa111bbb222", [RExp(r"(\D+)(\d+)", sub=r"\2\1"), RExp(r"(\D+)(\d+)", sub=r"\2\1")], [
                "111aaa222bbb", "111222aaabbb",
            ]),
        ]
    )
    def test__sub(self, source, attempts, _EXPECTED):
        ExpectAux(ReAttemptsFirst(*attempts).sub, source).check_assert(_EXPECTED[0])
        ExpectAux(ReAttemptsAll(*attempts).sub, source).check_assert(_EXPECTED[1])


# =====================================================================================================================
