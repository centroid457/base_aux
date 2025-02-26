from base_aux.base_statics.m2_exceptions import Exx__ValueNotValidated

from base_aux.aux_cmp_eq.m2_eq_aux import *
from base_aux.aux_cmp_eq.m4_eq_valid_chain import *
from base_aux.base_resolver.m1_resolver import *


# =====================================================================================================================
class ValueEqValid(NestCall_Resolve):
    """
    GOAL
    ----
    class to use validation by Eq objects for new values

    NOTE
    ----
    universal - need to pass EQ object!
    """
    __value: Any = NoValue
    VALUE_DEFAULT: Any = NoValue
    EQ: EqValid_Base | type[EqValid_Base] | EqValidChain | type[NoValue] = NoValue

    def __init__(
            self,
            value: Any = NoValue,
            eq: EqValid_Base | type[EqValid_Base] | EqValidChain | type[NoValue] = NoValue,
            eq_args: TYPING.ARGS_DRAFT = ARGS_FINAL__BLANK,          # NOTE: dont try to use INDIRECT style passing */**
            eq_kwargs: TYPING.KWARGS_DRAFT = KWARGS_FINAL__BLANK,
    ) -> None | NoReturn:
        if eq is not NoValue:
            self.EQ = eq

        if TypeAux(self.EQ).check__class() and issubclass(self.EQ, EqValid_Base):
            self.EQ = self.EQ(*eq_args, **eq_kwargs)

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

    def resolve(self) -> Any:
        return self.VALUE

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
class ValueEqValid_Exact(ValueEqValid):
    """
    GOAL
    ----
    base class to make a classes with specific validation

    SAME AS - ValueEqValid but
    --------------------------
    all args/kwargs passed into EQ

    NOTE
    ----
    exact EQ! - no need to pass EQ object! already in class
    """
    EQ: type[EqValid_Base]

    def __init__(
            self,
            value: Any,
            *eq_args: TYPING.ARGS_DRAFT,
            **eq_kwargs: TYPING.KWARGS_DRAFT,
    ) -> None:
        super().__init__(value=value, eq=NoValue, eq_args=eq_args, eq_kwargs=eq_kwargs)


# ---------------------------------------------------------------------------------------------------------------------
@final
class ValueEqValid_Variants(ValueEqValid_Exact):
    """
    SAME AS - ValueVariants but
    ---------------------------
    here is only validating and keep passed value
    in ValueVariants - final value used from exact Variants!
    """
    EQ = EqValid_VariantsDirect


@final
class ValueEqValid_VariantsStrLow(ValueEqValid_Exact):
    EQ = EqValid_VariantsStrLow


# =====================================================================================================================
if __name__ == "__main__":
    assert ValueEqValid_Variants(1, *(1, 2))
    try:
        assert ValueEqValid_Variants(1, *(10, 2))
        assert False
    except:
        assert True

    try:
        assert ValueEqValid_Variants("val", *("VAL", 2))
        assert False
    except:
        assert True

    assert ValueEqValid_VariantsStrLow(1, *(1, 2))
    assert ValueEqValid_VariantsStrLow("val", *("VAL", 2))


# =====================================================================================================================
