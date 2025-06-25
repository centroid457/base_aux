import pytest

from base_aux.lambdas.m1_lambda import *
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
    Lambda(func_link, match).expect__check_assert(_EXPECTED)


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
        Lambda(ReAttemptsFirst(*attempts).match, source).expect__check_assert(_EXPECTED[0])
        Lambda(ReAttemptsAll(*attempts).match, source).expect__check_assert(_EXPECTED[1])

        Lambda(ReAttemptsFirst(*attempts).fullmatch, source).expect__check_assert(_EXPECTED[2])
        Lambda(ReAttemptsAll(*attempts).fullmatch, source).expect__check_assert(_EXPECTED[3])

        Lambda(ReAttemptsFirst(*attempts).search, source).expect__check_assert(_EXPECTED[4])
        Lambda(ReAttemptsAll(*attempts).search, source).expect__check_assert(_EXPECTED[5])

        Lambda(ReAttemptsFirst(*attempts).findall, source).expect__check_assert(_EXPECTED[6])
        Lambda(ReAttemptsAll(*attempts).findall, source).expect__check_assert(_EXPECTED[7])

        Lambda(ReAttemptsFirst(*attempts).sub, source).expect__check_assert(_EXPECTED[8])
        Lambda(ReAttemptsAll(*attempts).sub, source).expect__check_assert(_EXPECTED[9])
        Lambda(ReAttemptsFirst(*attempts).delete, source).expect__check_assert(_EXPECTED[8])
        Lambda(ReAttemptsAll(*attempts).delete, source).expect__check_assert(_EXPECTED[9])

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
        Lambda(ReAttemptsFirst(*attempts).sub, source).expect__check_assert(_EXPECTED[0])
        Lambda(ReAttemptsAll(*attempts).sub, source).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
