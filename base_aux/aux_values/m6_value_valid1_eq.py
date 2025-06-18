from base_aux.aux_eq.m4_eq_valid_chain import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_types.m1_type_aux import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


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
    EQ: Base_EqValid | type[Base_EqValid] | type[NoValue] = NoValue

    def __init__(
            self,
            value: Any = NoValue,
            eq: Base_EqValid | type[Base_EqValid] | type[NoValue] = NoValue,
            eq_args: TYPING.ARGS_DRAFT = ARGS_FINAL__BLANK,          # NOTE: dont try to use INDIRECT style passing */**!!! but why???
            eq_kwargs: TYPING.KWARGS_DRAFT = KWARGS_FINAL__BLANK,
    ) -> None | NoReturn:
        if eq is not NoValue:
            self.EQ = eq

        if TypeAux(self.EQ).check__class() and issubclass(self.EQ, Base_EqValid):
            self.EQ = self.EQ(*eq_args, **eq_kwargs)

        if value is not NoValue:
            self.VALUE = value

        if self.VALUE_DEFAULT is NoValue:
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
    def VALUE(self, value: Any) -> None | NoReturn:
        if self.EQ == value or self.EQ is NoValue:    # place EQ at first place only)
            self.__value = value
            if self.VALUE_DEFAULT is NoValue:
                self.VALUE_DEFAULT = value
        else:
            raise Exx__ValueNotValidated()

    def value_update(self, value: Any | NoValue = NoValue) -> bool | NoReturn:
        """
        set new value or default
        """
        if value == NoValue:
            self.VALUE = self.VALUE_DEFAULT
        else:
            self.VALUE = value

        return True     # True - is for success only!


# =====================================================================================================================
class Base_ValueEqValid(ValueEqValid):
    """
    GOAL
    ----
    base class to make a classes with specific validation

    SAME AS - ValueEqValid but
    --------------------------
    all args/kwargs passed into EQ

    NOTE
    ----
    exact EQ! - no need to pass EQ object! already kept in class
    """
    EQ: type[Base_EqValid]

    def __init__(
            self,
            value: Any,
            *eq_args: TYPING.ARGS_DRAFT,
            **eq_kwargs: TYPING.KWARGS_DRAFT,
    ) -> None:
        super().__init__(value=value, eq=NoValue, eq_args=eq_args, eq_kwargs=eq_kwargs)


# ---------------------------------------------------------------------------------------------------------------------
@final
class ValueEqValid_Variants(Base_ValueEqValid):
    """
    SAME AS - ValueVariants but
    ---------------------------
    here is only validating and keep passed value
    in ValueVariants - final value used from exact Variants!
    """
    EQ = EqValid_EQ


@final
class ValueEqValid_VariantsStrIc(Base_ValueEqValid):
    EQ = EqValid_EQ_StrIc


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

    assert ValueEqValid_VariantsStrIc(1, *(1, 2))
    assert ValueEqValid_VariantsStrIc("val", *("VAL", 2))


# =====================================================================================================================
