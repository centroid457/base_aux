from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_enums.m2_enum1_adj import *


# =====================================================================================================================
class StrIc(NestInit_Source):
    """
    NOTE
    ----
    DO NOT USE in simple dict as keys! - use exact DictIcKeys instead!

    GOAL
    ----
    cmp any object with IC meaning,
    i used this behaviour many times and finally decide to make an object

    SPECIALLY CREATED FOR
    ---------------------
    first creation for EnumEqValid to use for keys - but it is incorrect (not enough)!
    """
    SOURCE: str | Any | Callable[[], str | Any] = None
    RESTYLE: EnumAdj__TextCaseStyle = EnumAdj__TextCaseStyle.ORIGINAL   # REMAKE original source - todo: decide to deprecate?

    def _init_post(self) -> None:
        self.source_update()

    def source_update(self) -> None:
        """
        GOAL
        ----
        update/change source by expected style!

        WHY
        ---
        if you already have result on inition? - because smtms you can change source by adding some new data
        and after that you may be want toFix actual value
        """
        # resolve -----
        self.SOURCE = Lambda(self.SOURCE).resolve__exc()
        self.SOURCE = str(self.SOURCE)

        # restyle ------
        if self.RESTYLE == EnumAdj__TextCaseStyle.UPPER:
            self.SOURCE = self.SOURCE.upper()

        elif self.RESTYLE == EnumAdj__TextCaseStyle.LOWER:
            self.SOURCE = self.SOURCE.lower()

    def __str__(self) -> str:
        return str(self.SOURCE)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __eq__(self, other: Any) -> bool:
        return str(other).lower() == self.SOURCE.lower()

    def __hash__(self) -> int:
        return hash(self.SOURCE.lower())

    def __contains__(self, other: Any) -> bool:
        return str(other).lower() in self.SOURCE.lower()

    def __getitem__(self, item: int) -> Self | NoReturn:
        result = self.SOURCE.lower()[item]
        return self.__class__(result)

    def __len__(self) -> int:
        return len(str(self.SOURCE))

    def __iter__(self) -> Iterable[Self]:
        for item in self.SOURCE:
            yield self.__class__(item)


# =====================================================================================================================
class StrIcUpper(StrIc):
    RESTYLE = EnumAdj__TextCaseStyle.UPPER


# ---------------------------------------------------------------------------------------------------------------------
class StrIcLower(StrIc):
    RESTYLE = EnumAdj__TextCaseStyle.LOWER


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source_draft, _EXPECTED",
    argvalues=[
        (1, ["1", "1", "1"]),
        ("AaA", ["AaA", "AAA", "aaa"]),
        (Lambda("AaA"), ["AaA", "AAA", "aaa"]),
        (Lambda(1), ["1", "1", "1"]),
    ]
)
def test__1_str(source_draft, _EXPECTED):
    Lambda(lambda: str(StrIc(source_draft))).expect__check_assert(_EXPECTED[0])
    Lambda(lambda: str(StrIcUpper(source_draft))).expect__check_assert(_EXPECTED[1])
    Lambda(lambda: str(StrIcLower(source_draft))).expect__check_assert(_EXPECTED[2])


@pytest.mark.parametrize(
    argnames="source_draft, other_draft, _EXPECTED",
    argvalues=[
        (1, 1, True),
        (Lambda(1), 1, True),
        ("AaA", "aAa", True),
        (Lambda("AaA"), "aAa", True),
        (Lambda("AaA"), StrIc("aAa"), True),
    ]
)
def test__2_eq(source_draft, other_draft, _EXPECTED):
    Lambda(StrIc(source_draft) == other_draft).expect__check_assert(_EXPECTED)
    Lambda(StrIcUpper(source_draft) == other_draft).expect__check_assert(_EXPECTED)
    Lambda(StrIcLower(source_draft) == other_draft).expect__check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source_draft, item, _EXPECTED",
    argvalues=[
        (1, 0, "1"),
        (1, 1, Exception),
        ("AaA", "aAa", Exception),
        (Lambda("AaA"), "aAa", Exception),
        (Lambda(1), 0, "1"),
        (Lambda(123), 0, "1"),
        (Lambda(123), 1, "2"),
        (Lambda("ABC"), 1, "b"),
    ]
)
def test__3_ga(source_draft, item, _EXPECTED):
    Lambda(lambda: StrIc(source_draft)[item]).expect__check_assert(_EXPECTED)
    Lambda(lambda: StrIcUpper(source_draft)[item]).expect__check_assert(_EXPECTED)
    Lambda(lambda: StrIcLower(source_draft)[item]).expect__check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source_draft, other, _EXPECTED",
    argvalues=[
        (1, 0, False),
        (1, 1, True),
        ("AaA", "aAa", True),
        ("AaA", "Aa", True),
        (Lambda("AaA"), "Aa", True),
        (Lambda(1), 0, False),
        (Lambda(123), 0, False),
        (Lambda(123), 1, True),
    ]
)
def test__4_other_in(source_draft, other, _EXPECTED):
    Lambda(other in StrIc(source_draft)).expect__check_assert(_EXPECTED)
    Lambda(other in StrIcUpper(source_draft)).expect__check_assert(_EXPECTED)
    Lambda(other in StrIcLower(source_draft)).expect__check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source_draft, items, _EXPECTED",
    argvalues=[
        (1, [0, 10], False),
        (1, [0, 1], True),
        ("AaA", ["aAa", "aA"], True),
        ("AaA", ["Aa", ], False),
        (Lambda("AaA"), ["Aa", ], False),
        (Lambda(1), [0, 10,],  False),
        (Lambda(123), [0, 10,], False),
        (Lambda(123), [0, 123,], True),
    ]
)
def test__5_in_other(source_draft, items, _EXPECTED):
    Lambda(StrIc(source_draft) in items).expect__check_assert(_EXPECTED)
    Lambda(StrIcUpper(source_draft) in items).expect__check_assert(_EXPECTED)
    Lambda(StrIcLower(source_draft) in items).expect__check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source_1, source_2, _EXPECTED",
    argvalues=[
        (1, 0, 2),
        (1, 1, 1),
        ("AaA", "aAa", 1),
        ("AaA", "Aa", 2),
        (Lambda("AaA"), "Aa", 2),
        (Lambda(1), 0, 2),
        (Lambda(123), 0, 2),
    ]
)
def test__6_set(source_1, source_2, _EXPECTED):
    Lambda(len({StrIc(source_1), StrIcUpper(source_2)})).expect__check_assert(_EXPECTED)
    Lambda(len({StrIc(source_1), StrIcLower(source_2)})).expect__check_assert(_EXPECTED)
    Lambda(len({StrIcUpper(source_1), StrIcLower(source_2)})).expect__check_assert(_EXPECTED)


def test__10_gi_from_dict():
    assert {1: 1, StrIc("AAA"): 1, "2": 2}["aaa"] == 1
    try:
        assert {1: 1, StrIc("AAA"): 1, "2": 2}["AAA"] == 1
    except:
        print(f"THIS WILL newer work with gi! try use not a simple dict but DictIcKeys")
        return
    assert False


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
