from base_aux.valid.m1_aux_valid_lg import *
from base_aux.aux_cmp_eq.m2_eq_aux import *


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
    """
    # -----------------------------------------------------------------------------------------------------------------
    def Isinstance(self, other_final: Any, *variants: type[Any]) -> bool | NoReturn:
        for variant in variants:
            if isinstance(other_final, variant):
                return True
        return False

    # -----------------------------------------------------------------------------------------------------------------
    def Variants(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        """
        GOAL
        ----
        cmp Other with each variants by IN operator
        """
        return other_final in variants

    def VariantsStrIc(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variants = (str(var).lower() for var in variants)

        return other_final in variants

    # -----------------------------------------------------------------------------------------------------------------
    def Contains(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        """
        GOAL
        ----
        cmp each variant with other by IN operator
        mainly using for check substrs (variants) in BaseStr

        SPECIALLY CREATED FOR
        ---------------------
        AttrsAux.dump_dict/AttrsDump to skip exact attrs with Parts in names
        """
        for variant in variants:
            if variant in other_final:
                return True
        return False

    def ContainsStrIc(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variants = [str(var).lower() for var in variants]

        for variant in variants:
            if variant in other_final:
                return True
        return False

    # -----------------------------------------------------------------------------------------------------------------
    def Startswith(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variants = (str(var) for var in variants)

        for var in variants:
            if other_final.startswith(var):
                return True

        return False

    def StartswithIc(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variants = (str(var).lower() for var in variants)

        for var in variants:
            if other_final.startswith(var):
                return True

        return False

    # -----------------------------------------------------------------------------------------------------------------
    def Endswith(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variants = (str(var) for var in variants)

        for var in variants:
            if other_final.endswith(var):
                return True

        return False

    def EndswithIc(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variants = (str(var).lower() for var in variants)

        for var in variants:
            if other_final.endswith(var):
                return True

        return False

    # -----------------------------------------------------------------------------------------------------------------
    def BoolTrue(self, other_final: TYPE__VALID_BOOL__DRAFT, *v_args, **v_kwargs) -> bool:
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

    def Raise(self, other_final: Any, *variants: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return self.OTHER_RAISED

    def NotRaise(self, other_final, *v_args, **v_kwargs) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return not self.OTHER_RAISED

    def Exx(self, other_final, *v_args, **v_kwargs) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception()
        if raised - return False!!
        """
        return not self.OTHER_RAISED and TypeAux(other_final).check__exception()

    def ExxRaise(self, other_final, *v_args, **v_kwargs) -> bool:
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
            *regexps: str,
            ignorecase: bool = True,
            bool_collect: Enum_BoolCumulate = None,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        bool_collect = bool_collect or self.BOOL_COLLECT

        for pattern in regexps:
            result_i = match_link(pattern=str(pattern), string=str(other_final), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)

            # CUMULATE --------
            if bool_collect == Enum_BoolCumulate.ALL_TRUE:
                if not result_i:
                    return False
            elif bool_collect == Enum_BoolCumulate.ANY_TRUE:
                if result_i:
                    return True
            elif bool_collect == Enum_BoolCumulate.ALL_FALSE:
                if result_i:
                    return False
            elif bool_collect == Enum_BoolCumulate.ANY_FALSE:
                if not result_i:
                    return True

        # FINAL ------------
        if bool_collect in [Enum_BoolCumulate.ALL_TRUE, Enum_BoolCumulate.ALL_FALSE]:
            return True
        else:
            return False

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
