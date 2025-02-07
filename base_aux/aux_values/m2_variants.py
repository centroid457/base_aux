from typing import *

from base_aux.aux_values.m0_novalue import NoValue
from base_aux.base_exceptions.m1_exceptions import *
from base_aux.aux_eq.m1_eq_aux import EqAux


# =====================================================================================================================
TYPE__VARIANT = Union[str, Any]
TYPE__VARIANTS = list[TYPE__VARIANT] | NoValue


# =====================================================================================================================
# FOXME: DEPRECATE for new Eq style

class ValueVariants:
    """
    used to keep separated VALUE and measure unit

    SAME AS - ValueEqValid_Variants
    -------------------------------
    here is only validating and keep passed value
    in ValueVariants - final value used from exact Variants!

    GOAL
    ----
    1. get first associated value
    2. validate item by variants
    """
    # NOTE: NOTS DEPRECATE!!!
    # TODO: combine with ValueUnit - just add ACCEPTABLE(*VARIANTS) and rename UNIT just as SUFFIX!

    # SETTINGS -----------------------
    IGNORECASE: bool = True
    VARIANTS: TYPE__VARIANTS = NoValue
    VALUE_DEFAULT: Any = NoValue

    # DATA ---------------------------
    __value: Any = NoValue

    def __init__(self, value: Union[str, Any] = NoValue, variants: TYPE__VARIANTS = NoValue, ignorecase: bool = None):
        """
        """
        if ignorecase is not None:
            self.IGNORECASE = ignorecase

        self._variants_apply(variants)

        if value != NoValue:
            self.VALUE = value
            self.VALUE_DEFAULT = self.VALUE

        self._variants_apply(variants)  # need secondary!!!

    def _variants_apply(self, variants: set[Union[str, Any]] | NoValue = NoValue) -> None:
        if variants is not NoValue:
            self.VARIANTS = variants

        if self.VARIANTS is NoValue:
            if self.VALUE is not NoValue:
                self.VARIANTS = [self.VALUE, ]
            # else:
            #     self.VARIANTS = set()

    def __str__(self) -> str:
        return f"{self.VALUE}"

    def __repr__(self) -> str:
        """
        used as help
        """
        return f"{self.VALUE}{self.VARIANTS}"

    def __eq__(self, other):
        if isinstance(other, ValueVariants):
            if other.VALUE == NoValue:
                return self.VALUE in other
            else:
                other = other.VALUE

        if self.VALUE == NoValue:
            return self.value_validate(other)

        # todo: decide is it correct using comparing by str()??? by now i think it is good enough! but maybe add it as parameter
        if self.IGNORECASE:
            return (self.VALUE == other) or (str(self.VALUE).lower() == str(other).lower())
        else:
            return (self.VALUE == other) or (str(self.VALUE) == str(other))

    def __len__(self):
        return len(self.VARIANTS or [])

    def __iter__(self):
        yield from self.VARIANTS

    def __contains__(self, item) -> bool:
        """
        used to check compatibility
        """
        return self.value_validate(item)

    def __getitem__(self, item: int) -> Any:
        return self.VARIANTS[item]

    @property
    def VALUE(self) -> Any:
        return self.__value

    @VALUE.setter
    def VALUE(self, value: Any) -> Optional[NoReturn]:
        variant = self.value_get_variant(value)
        if variant != NoValue:
            self.__value = variant
        else:
            raise Exx__ValueNotValidated()

    def value_get_variant(self, value: Any) -> TYPE__VARIANT | NoValue:
        for variant in self.VARIANTS:
            if EqAux(variant).check_doubleside__bool(value):
                return variant

            if self.IGNORECASE:
                result = str(variant).lower() == str(value).lower()
            else:
                result = str(variant) == str(value)
            if result:
                return variant

        return NoValue

    def value_validate(self, value: Any) -> Any | None:
        return self.value_get_variant(value) != NoValue

    def reset(self) -> None:
        """
        set VALUE into default only if default is exists!
        """
        if self.VALUE_DEFAULT != NoValue:
            self.VALUE = self.VALUE_DEFAULT


# =====================================================================================================================
