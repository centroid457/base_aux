from typing import *

from base_aux.base_exceptions import Exx__ValueNotValidated

from base_aux.aux_values.m0_novalue import NoValue
from base_aux.aux_eq.m1_eq_aux import *
from base_aux.aux_eq.m2_eq_validator import *
from base_aux.aux_eq.m3_eq_validator_chains import *


# =====================================================================================================================
class ValueEqValid:
    __value: Any = NoValue
    VALUE_DEFAULT: Any = NoValue
    EQ: EqValid_Base | EqValidChain | Any | NoValue = NoValue

    def __init__(self, value: Any = NoValue, eq: EqValid_Base | EqValidChain = NoValue) -> None:
        if eq:
            self.EQ = eq

        if value is not NoValue:
            self.VALUE = value

        self.VALUE_DEFAULT = self.VALUE

    def __str__(self) -> str:
        return f"{self.VALUE}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.VALUE},eg={self.EQ})"

    def __eq__(self, other) -> bool:
        if isinstance(other, ValueEqValid):
            other = other.VALUE

        return EqAux(self.VALUE).check_doubleside__bool(other)

    @property
    def VALUE(self) -> Any:
        return self.__value

    @VALUE.setter
    def VALUE(self, value: Any) -> Optional[NoReturn]:
        if self.EQ == value or self.EQ is NoValue:    # place EQ at first place only)
            self.__value = value
        else:
            raise Exx__ValueNotValidated()

    def reset(self, value: Any | NoValue = NoValue) -> bool | NoReturn:
        """
        set new value or default
        """
        if value == NoValue:
            self.VALUE = self.VALUE_DEFAULT
        else:
            self.VALUE = value

        return True     # True - is for success only!


# =====================================================================================================================
