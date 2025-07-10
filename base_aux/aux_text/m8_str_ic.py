from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_text.m5_re2_attemps import *
from base_aux.aux_attr.m4_kits import *
from base_aux.base_lambdas.m1_lambda import *
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
    SOURCE: str = None
    STYLE_REINIT: Enum__TextCaseStyle = Enum__TextCaseStyle.ORIGINAL   # REMAKE original source - todo: decide to deprecate?

    def init_post(self) -> None | NoReturn:
        self.source_update()

    def source_update(self):
        """
        GOAL
        ----
        update/change source by expected style!

        WHY
        ---
        if you already have result on inition? - because smtms you can change source by adding some new data
        and after that you may be want toFix actual value
        """
        self.SOURCE = str(self.SOURCE)

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
if __name__ == "__main__":
    pass


# =====================================================================================================================
