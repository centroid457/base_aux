from . import *
from typing import *
from object_info import ObjectInfo
import re

from .valid_1_base import Valid

# =====================================================================================================================
class Exx__ValueNotInVariants(Exception):
    pass


class Exx__VariantsIncompatible(Exception):     # TODO: seems need to deprecate it! it is not important!
    pass


# =====================================================================================================================
TYPE__VARIANT = Union[str, Any]
TYPE__VARIANTS = Iterable[TYPE__VARIANT] | ValueNotExist


# =====================================================================================================================
class ValueVariants:
    """
    used to keep separated VALUE and measure unit

    GOAL
    ----
    1. get first associated value
    2. validate item by variants
    """
    # TODO: combine with ValueUnit - just add ACCEPTABLE(*VARIANTS) and rename UNIT just as SUFFIX!

    # SETTINGS -----------------------
    CASE_INSENSITIVE: bool = True
    VARIANTS: TYPE__VARIANTS = ValueNotExist
    VALUE_DEFAULT: Any = ValueNotExist

    # DATA ---------------------------
    __value: Any = ValueNotExist

    def __init__(self, value: Union[str, Any] = ValueNotExist, variants: TYPE__VARIANTS = ValueNotExist, case_insensitive: bool = None):
        """
        """
        if case_insensitive is not None:
            self.CASE_INSENSITIVE = case_insensitive

        self._variants_apply(variants)

        if value != ValueNotExist:
            self.VALUE = value
            self.VALUE_DEFAULT = self.VALUE

        self._variants_apply(variants)  # need secondary!!!

    def _variants_apply(self, variants: set[Union[str, Any]] | ValueNotExist = ValueNotExist) -> None:
        if variants is not ValueNotExist:
            self.VARIANTS = variants

        if self.VARIANTS is ValueNotExist:
            if self.VALUE is not ValueNotExist:
                self.VARIANTS = {self.VALUE, }
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
            if other.VALUE == ValueNotExist:
                return self.VALUE in other
            else:
                other = other.VALUE

        if self.VALUE == ValueNotExist:
            return self.value_validate(other)

        # todo: decide is it correct using comparing by str()??? by now i think it is good enough! but maybe add it as parameter
        if self.CASE_INSENSITIVE:
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

    @property
    def VALUE(self) -> Any:
        return self.__value

    @VALUE.setter
    def VALUE(self, value: Any) -> Optional[NoReturn]:
        variant = self.value_get_variant(value)
        if variant != ValueNotExist:
            self.__value = variant
        else:
            raise Exx__ValueNotInVariants()

    def value_get_variant(self, value: Any) -> TYPE__VARIANT | ValueNotExist:
        for variant in self.VARIANTS:
            if Valid.compare_doublesided__bool(variant, value):
                return variant

            if self.CASE_INSENSITIVE:
                result = str(variant).lower() == str(value).lower()
            else:
                result = str(variant) == str(value)
            if result:
                return variant

        return ValueNotExist

    def value_validate(self, value: Any) -> Any | None:
        return self.value_get_variant(value) != ValueNotExist

    def reset(self) -> None:
        """
        set VALUE into default only if default is exists!
        """
        if self.VALUE_DEFAULT != ValueNotExist:
            self.VALUE = self.VALUE_DEFAULT


# =====================================================================================================================
