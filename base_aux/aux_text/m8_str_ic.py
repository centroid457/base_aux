from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_text.m5_re2_attemps import *
from base_aux.aux_attr.m4_kits import *
from base_aux.versions.m2_version import *


# =====================================================================================================================
class Enum__TextCaseStyle(Enum):
    ORIGINAL: int = 0
    LOWER: int = 1
    UPPER: int = 2


# =====================================================================================================================
class StrIc(NestInit_Source):
    """
    GOAL
    ----
    cmp any object with IC meaning,
    i used this behaviour many times and finally decide to make an object

    SPECIALLY CREATED FOR
    ---------------------
    first creation for EnumEqValid to use for keys
    """
    SOURCE: str | Any | Callable[[], str | Any] = None
    STYLE_REINIT: Enum__TextCaseStyle = Enum__TextCaseStyle.ORIGINAL   # REMAKE original source - todo: decide to deprecate?

    def init_post(self) -> None:
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
        self.SOURCE = Lambda(self.SOURCE).resolve__exx()
        self.SOURCE = str(self.SOURCE)

        # restyle ------
        if self.STYLE_REINIT == Enum__TextCaseStyle.UPPER:
            self.SOURCE = self.SOURCE.upper()

        elif self.STYLE_REINIT == Enum__TextCaseStyle.LOWER:
            self.SOURCE = self.SOURCE.lower()

    def __str__(self) -> str:
        return str(self.SOURCE)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __eq__(self, other: Any) -> bool:
        return str(other).lower() == self.SOURCE.lower()

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

    def __hash__(self):
        return hash(self.SOURCE.lower())


# =====================================================================================================================
class StrIcUpper(StrIc):
    STYLE_REINIT = Enum__TextCaseStyle.UPPER


# ---------------------------------------------------------------------------------------------------------------------
class StrIcLower(StrIc):
    STYLE_REINIT = Enum__TextCaseStyle.LOWER


# =====================================================================================================================
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
def test__1_eq(source_draft, other_draft, _EXPECTED):
    Lambda(StrIc(source_draft) == other_draft).expect__check_assert(_EXPECTED)
    Lambda(StrIcUpper(source_draft) == other_draft).expect__check_assert(_EXPECTED)
    Lambda(StrIcLower(source_draft) == other_draft).expect__check_assert(_EXPECTED)


@pytest.mark.parametrize(
    argnames="source_draft, _EXPECTED",
    argvalues=[
        (1, ["1", "1", "1"]),
        ("AaA", ["AaA", "AAA", "aaa"]),
        (Lambda("AaA"), ["AaA", "AAA", "aaa"]),
        (Lambda(1), ["1", "1", "1"]),
    ]
)
def test__2_str(source_draft, _EXPECTED):
    Lambda(lambda: str(StrIc(source_draft))).expect__check_assert(_EXPECTED[0])
    Lambda(lambda: str(StrIcUpper(source_draft))).expect__check_assert(_EXPECTED[1])
    Lambda(lambda: str(StrIcLower(source_draft))).expect__check_assert(_EXPECTED[2])


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
def test__2_ga(source_draft, item, _EXPECTED):
    Lambda(lambda: StrIc(source_draft)[item]).expect__check_assert(_EXPECTED)
    Lambda(lambda: StrIcUpper(source_draft)[item]).expect__check_assert(_EXPECTED)
    Lambda(lambda: StrIcLower(source_draft)[item]).expect__check_assert(_EXPECTED)


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
