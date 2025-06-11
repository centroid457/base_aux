from base_aux.valid.m1_aux_valid_lg import *
from base_aux.aux_eq.m2_eq_aux import *


# =====================================================================================================================
class Validators:
    """
    GOAL
    ----
    collect all validators (funcs) in one place
    applicable in Base_EqValid only (by common way), but you can try using it separated!

    SPECIALLY CREATED FOR
    ---------------------
    Base_EqValid

    RULES
    -----
    1/ NoReturn - available for all returns as common!!! but sometimes it cant be reached (like TRUE/RAISE)
    2/ other_final - always at first place! other params goes nest (usually uncovered)
    """
    # -----------------------------------------------------------------------------------------------------------------
    def Isinstance(self, other_final: Any, variant: type[Any]) -> bool | NoReturn:
        return isinstance(other_final, variant)

    # -----------------------------------------------------------------------------------------------------------------
    def Variant(self, other_final: Any, variant: Any) -> bool | NoReturn:
        """
        GOAL
        ----
        cmp Other with each variants by IN operator
        """
        return other_final == variant

    def VariantStrIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return str(other_final).lower() == str(variant).lower()

    # -----------------------------------------------------------------------------------------------------------------
    def Contain(self, other_final: Any, variant: Any) -> bool | NoReturn:
        """
        GOAL
        ----
        check each variant with other by IN operator
        mainly using for check substrs (variants) in BaseStr

        SPECIALLY CREATED FOR
        ---------------------
        AttrsAux.dump_dict/AttrsDump to skip exact attrs with Parts in names
        """
        return variant in other_final

    def ContainStrIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return str(variant).lower() in str(other_final).lower()

    # -----------------------------------------------------------------------------------------------------------------
    def Startswith(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variant = str(variant)
        return other_final.startswith(variant)

    def StartswithIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variant = str(variant).lower()
        return other_final.startswith(variant)

    # -----------------------------------------------------------------------------------------------------------------
    def Endswith(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variant = str(variant)
        return other_final.endswith(variant)

    def EndswithIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variant = str(variant).lower()
        return other_final.endswith(variant)

    # -----------------------------------------------------------------------------------------------------------------
    def BoolTrue(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with no raise and no Exception in result
        """
        if self.OTHER_RAISED or TypeAux(other_final).check__exception():
            return False
        try:
            return bool(other_final)
        except:
            return False

    # TODO: add FALSE????? what to do with exx and real false?

    def Raise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return self.OTHER_RAISED

    def NotRaise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return not self.OTHER_RAISED

    def Exx(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception()
        if raised - return False!!
        """
        return not self.OTHER_RAISED and TypeAux(other_final).check__exception()

    def ExxRaise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception() or Raised
        """
        return self.OTHER_RAISED or TypeAux(other_final).check__exception()

    # -----------------------------------------------------------------------------------------------------------------
    def LtGt_Obj(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_Obj(other_final).ltgt(low, high)

    def LtGe_Obj(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_Obj(other_final).ltge(low, high)

    def LeGt_Obj(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_Obj(other_final).legt(low, high)

    def LeGe_Obj(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_Obj(other_final).lege(low, high)

    # -----------------------------------------------------------------------------------------------------------------
    def LtGt_NumParsedSingle(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_NumParsedSingle(other_final).ltgt(low, high)

    def LtGe_NumParsedSingle(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_NumParsedSingle(other_final).ltge(low, high)

    def LeGt_NumParsedSingle(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_NumParsedSingle(other_final).legt(low, high)

    def LeGe_NumParsedSingle(self, other_final, low: Any | None = None, high: Any | None = None) -> bool | NoReturn:
        return ValidAux_NumParsedSingle(other_final).lege(low, high)

    # -----------------------------------------------------------------------------------------------------------------
    def NumParsedSingle(self, other_final, expect: Any | None | bool | Enum_NumType = True) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(expect)

    def NumParsedSingle_TypeInt(self, other_final) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(int)

    def NumParsedSingle_TypeFloat(self, other_final) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(float)

    # -----------------------------------------------------------------------------------------------------------------
    def Regexp(
            self,
            other_final,
            pattern: str,
            ignorecase: bool = True,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        # NOTE: just a link!
        #   you can use directly match_link in Base_EqValid!!!!
        result = match_link(pattern=str(pattern), string=str(other_final), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)
        return result is not None

    # -----------------------------------------------------------------------------------------------------------------
    def AttrsByKwargs(
            self,
            other_final,
            # callable_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
            **kwargs: TYPING.KWARGS_FINAL
    ) -> bool | NoReturn:
        for key, value in kwargs.items():
            value_expected = CallableAux(value).resolve(Enum_CallResolve.EXX)
            value_other = AttrAux(other_final).gai_ic__callable_resolve(key, Enum_CallResolve.EXX)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    def AttrsByObj(
            self,
            other_final,
            # callable_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
            source: Any,
            # attr_level: Enum_AttrScope = Enum_AttrScope.NOT_PRIVATE,
    ) -> bool | NoReturn:
        for key in AttrAux(source).iter__names_filter(self.ATTR_LEVEL):
            value_expected = AttrAux(source).gai_ic__callable_resolve(key, Enum_CallResolve.EXX)
            value_other = AttrAux(other_final).gai_ic__callable_resolve(key, Enum_CallResolve.EXX)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    # NOTE: INAPPROPRIATE!!!!
    # def AttrsByObjNotPrivate(
    #         self,
    #         other_final,
    #         # callable_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
    #         source: Any,
    # ) -> bool | NoReturn:
    #     return self._AttrsByObj(other_final=other_final, source=source, attr_level=Enum_AttrScope.NOT_PRIVATE)
    # def AttrsByObjNotHidden(
    #         self,
    #         other_final,
    #         # callable_resolve: Enum_CallResolve = Enum_CallResolve.EXX,
    #         source: Any,
    # ) -> bool | NoReturn:
    #     return self._AttrsByObj(other_final=other_final, source=source, attr_level=Enum_AttrScope.NOT_HIDDEN)

    # -----------------------------------------------------------------------------------------------------------------
    def AnnotsAllExists(
            self,
            other_final,
            **kwargs: TYPING.KWARGS_FINAL
    ) -> bool | NoReturn:
        return AnnotsAllAux(other_final).annots__check_all_defined()


# =====================================================================================================================
