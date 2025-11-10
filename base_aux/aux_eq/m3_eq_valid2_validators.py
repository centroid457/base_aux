from base_aux.aux_eq.m2_eq_aux import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_types.m0_static_typing import TYPING


# =====================================================================================================================
class Validators:
    """
    CAREFULL
    --------
    using one validators inside others - is not so simple!

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
    3/ in cmp result KEEP variant ALWAYS AT FIRST PLACE!!! to use its DANDER-methods first! like in CMP_LT

    """
    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def IsinstanceSameinstance(self, other_final: Any, variant: type[Any] | Any) -> bool | NoReturn:
        """
        GOAL
        ----
        isinstance or SameInstance!!!
        """
        try:
            issubclass(variant, object)
        except:
            variant = variant.__class__

        return isinstance(other_final, variant)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
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

    @staticmethod
    def ContainStrIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return str(variant).lower() in str(other_final).lower()

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Startswith(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variant = str(variant)
        return other_final.startswith(variant)

    @staticmethod
    def StartswithIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variant = str(variant).lower()
        return other_final.startswith(variant)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Endswith(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final)
        variant = str(variant)
        return other_final.endswith(variant)

    @staticmethod
    def EndswithIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variant = str(variant).lower()
        return other_final.endswith(variant)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
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

    # TODO: add FALSE????? what to do with exc and real false?

    @staticmethod
    def Raise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return self.OTHER_RAISED

    @staticmethod
    def NotRaise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return not self.OTHER_RAISED

    @staticmethod
    def Exc(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception()
        if raised - return False!!
        """
        return not self.OTHER_RAISED and TypeAux(other_final).check__exception()

    @staticmethod
    def ExcRaise(self, other_final: Any) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception() or Raised
        """
        return self.OTHER_RAISED or TypeAux(other_final).check__exception()

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def CMP_EQ(self, other_final: Any, variant: Any) -> bool | NoReturn:
        print(f"CMP_EQ={other_final=}/{variant=}")
        return variant == other_final

    @staticmethod
    def CMP_EQ__StrIc(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return str(variant).lower() == str(other_final).lower()

    @staticmethod
    def CMP_EQ__NumParsedSingle(self, other_final: Any, variant: Any) -> bool | NoReturn:
        other_final = TextAux(other_final).parse__number_single()
        print(f"CMP_EQ__NumParsedSingle={other_final=}/{variant=}")
        return Validators.CMP_EQ(self, other_final, variant)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def CMP_LT(self, other_final: Any, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_final).parse__number_single()
        return variant > other_final    # NOTE: KEEP variant ALWAYS AT FIRST PLACE!!! to use its DANDER-methods!

    @staticmethod
    def CMP_LE(self, other_final: Any, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_final).parse__number_single()
        return variant >= other_final

    @staticmethod
    def CMP_GT(self, other_final: Any, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_final).parse__number_single()
        return variant < other_final

    @staticmethod
    def CMP_GE(self, other_final: Any, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_final).parse__number_single()
        return variant <= other_final

    @staticmethod
    def CMP_LGTE(
            self,
            other_final: Any,
            lt: Any | None = None,
            le: Any | None = None,
            gt: Any | None = None,
            ge: Any | None = None,
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        """
        NOTE
        ----
        used all variants of cmp (l/g* + *t/e) just to make a one clear logical func!
        intended using only one or two appropriate combination!
        """
        if parse__number_single:
            other_final = TextAux(other_final).parse__number_single()

        for validator, variant in [
            (Validators.CMP_LT, lt),
            (Validators.CMP_LE, le),
            (Validators.CMP_GT, gt),
            (Validators.CMP_GE, ge),
        ]:
            if variant is not None:
                if not validator(self, other_final, variant):
                    return False
        return True

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def CMP_LT_NumParsedSingle(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return Validators.CMP_LT(self, other_final, variant, parse__number_single=True)

    @staticmethod
    def CMP_LE_NumParsedSingle(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return Validators.CMP_LE(self, other_final, variant, parse__number_single=True)

    @staticmethod
    def CMP_GT_NumParsedSingle(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return Validators.CMP_GT(self, other_final, variant, parse__number_single=True)

    @staticmethod
    def CMP_GE_NumParsedSingle(self, other_final: Any, variant: Any) -> bool | NoReturn:
        return Validators.CMP_GE(self, other_final, variant, parse__number_single=True)

    @staticmethod
    def CMP_LGTE_NumParsedSingle(
            self,
            other_final: Any,
            lt: Any | None = None,
            le: Any | None = None,
            gt: Any | None = None,
            ge: Any | None = None,
    ) -> bool | NoReturn:
        return Validators.CMP_LGTE(self, other_final, lt=lt, le=le, gt=gt, ge=ge, parse__number_single=True)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def NumParsedSingle_Success(self, other_final) -> bool:
        other_final = TextAux(other_final).parse__number_single()
        return other_final is not None

    @staticmethod
    def NumParsedSingle_TypeInt(self, other_final) -> bool:
        other_final = TextAux(other_final).parse__number_single()
        return isinstance(other_final, int)

    @staticmethod
    def NumParsedSingle_TypeFloat(self, other_final) -> bool:
        other_final = TextAux(other_final).parse__number_single()
        return isinstance(other_final, float)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Regexp(
            self,
            other_final,
            pattern: str,
            ignorecase: bool = True,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        # NOTE: just a link!
        #   you can use directly match_link in Base_EqValid!!!!??? - no you need use it at least over LAMBDA!
        result = match_link(pattern=str(pattern), string=str(other_final), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)
        return result is not None

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def AttrsByKwargs(
            self,
            other_final,
            # callable_resolve: EnumAdj_CallResolveStyle = EnumAdj_CallResolveStyle.EXC,
            **kwargs: TYPING.KWARGS_FINAL
    ) -> bool | NoReturn:
        for key, value in kwargs.items():
            value_expected = Lambda(value).resolve__style(EnumAdj_CallResolveStyle.EXC)
            value_other = AttrAux_Existed(other_final).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    @staticmethod
    def AttrsByObj(
            self,
            other_final,
            # callable_resolve: EnumAdj_CallResolveStyle = EnumAdj_CallResolveStyle.EXC,
            source: Any,
            # attr_level: EnumAdj_AttrScope = EnumAdj_AttrScope.NOT_PRIVATE,
    ) -> bool | NoReturn:
        for key in AttrAux_Existed(source).iter__names_filter(self.ATTR_LEVEL):
            value_expected = AttrAux_Existed(source).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            value_other = AttrAux_Existed(other_final).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    # NOTE: INAPPROPRIATE!!!!
    # def AttrsByObjNotPrivate(
    #         self,
    #         other_final,
    #         # callable_resolve: EnumAdj_CallResolveStyle = EnumAdj_CallResolveStyle.EXC,
    #         source: Any,
    # ) -> bool | NoReturn:
    #     return self._AttrsByObj(other_final=other_final, source=source, attr_level=EnumAdj_AttrScope.NOT_PRIVATE)
    # def AttrsByObjNotHidden(
    #         self,
    #         other_final,
    #         # callable_resolve: EnumAdj_CallResolveStyle = EnumAdj_CallResolveStyle.EXC,
    #         source: Any,
    # ) -> bool | NoReturn:
    #     return self._AttrsByObj(other_final=other_final, source=source, attr_level=EnumAdj_AttrScope.NOT_HIDDEN)

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def AnnotsAllExists(
            self,
            other_final,
    ) -> bool | NoReturn:
        return AttrAux_AnnotsAll(other_final).annots__check_all_defined()


# =====================================================================================================================
