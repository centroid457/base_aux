from base_aux.aux_eq.m2_eq_aux import *
from base_aux.aux_text.m1_text_aux import *
from base_aux.base_types.m0_static_typing import TYPING

from base_aux.aux_eq.m3_eq_other1_resolved import *


# ======================================================================================================================
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
    # ==================================================================================================================
    # 1=NO VARIANTS
    @staticmethod
    def BoolTrue(self, other_resolved: OtherResolved) -> bool:
        """
        GOAL
        ----
        True - if Other object called with no raise and no Exception in result
        """
        if other_resolved.RAISED or TypeAux(other_resolved.RESULT).check__exception():
            return False
        try:
            return bool(other_resolved.RESULT)
        except:
            return False

    @staticmethod
    def BoolFalse(self, other_resolved: OtherResolved) -> bool:
        # FIXME: what to do with exc and real false?
        return not Validators.BoolTrue(self, other_resolved)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Raised(self, other_resolved: OtherResolved) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return other_resolved.RAISED

    @staticmethod
    def NotRaised(self, other_resolved: OtherResolved) -> bool:
        """
        GOAL
        ----
        True - if Other object called with raised
        if other is exact final Exception without raising - it would return False!
        """
        return not other_resolved.RAISED

    @staticmethod
    def Exc(self, other_resolved: OtherResolved) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception()
        if raised - return False!!
        """
        return not other_resolved.RAISED and TypeAux(other_resolved.RESULT).check__exception()

    @staticmethod
    def ExcRaised(self, other_resolved: OtherResolved) -> bool:
        """
        GOAL
        ----
        True - if Other object is exact Exception or Exception() or Raised
        """
        return other_resolved.RAISED or TypeAux(other_resolved.RESULT).check__exception()

    # ==================================================================================================================
    @staticmethod
    def IsinstanceSameinstance(self, other_resolved: OtherResolved, variant: type[Any] | Any) -> bool | NoReturn:
        """
        GOAL
        ----
        isinstance or SameInstance!!!
        """
        try:
            issubclass(variant, object)
        except:
            variant = variant.__class__

        return isinstance(other_resolved.RESULT, variant)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Contain(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        """
        GOAL
        ----
        check each variant with other by IN operator
        mainly using for check substrs (variants) in BaseStr

        SPECIALLY CREATED FOR
        ---------------------
        AttrsAux.dump_dict/AttrsDump to skip exact attrs with Parts in names
        """
        return variant in other_resolved.RESULT

    @staticmethod
    def ContainStrIc(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return str(variant).lower() in str(other_resolved.RESULT).lower()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Startswith(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        other_final = str(other_resolved.RESULT)
        variant = str(variant)
        return other_final.startswith(variant)

    @staticmethod
    def StartswithIc(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        other_final = str(other_resolved.RESULT).lower()
        variant = str(variant).lower()
        return other_final.startswith(variant)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Endswith(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        other_final = str(other_resolved.RESULT)
        variant = str(variant)
        return other_final.endswith(variant)

    @staticmethod
    def EndswithIc(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        other_final = str(other_resolved.RESULT).lower()
        variant = str(variant).lower()
        return other_final.endswith(variant)

    # ==================================================================================================================
    @staticmethod
    def CMP_EQ(self, other_resolved: OtherResolved, variant: Any, parse__number_single: bool | None = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_resolved.RESULT).parse__number_single()
        else:
            other_final = other_resolved.RESULT
        print(f"CMP_EQ={other_resolved.RESULT=}/{other_final=}/{variant=}")
        return variant == other_final

    @staticmethod
    def CMP_EQ__StrIc(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return str(variant).lower() == str(other_resolved.RESULT).lower()

    @staticmethod
    def CMP_EQ__NumParsedSingle(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return Validators.CMP_EQ(self, other_resolved, variant, parse__number_single=True)

    # ==================================================================================================================
    @staticmethod
    def CMP_L_T(self, other_resolved: OtherResolved, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_resolved.RESULT).parse__number_single()
        else:
            other_final = other_resolved.RESULT
        return variant > other_final    # NOTE: KEEP variant ALWAYS AT FIRST PLACE!!! to use its DANDER-methods!

    @staticmethod
    def CMP_L_E(self, other_resolved: OtherResolved, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_resolved.RESULT).parse__number_single()
        else:
            other_final = other_resolved.RESULT
        return variant >= other_final

    @staticmethod
    def CMP_G_T(self, other_resolved: OtherResolved, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_resolved.RESULT).parse__number_single()
        else:
            other_final = other_resolved.RESULT
        return variant < other_final

    @staticmethod
    def CMP_G_E(self, other_resolved: OtherResolved, variant: Any, parse__number_single: bool = None) -> bool | NoReturn:
        if parse__number_single:
            other_final = TextAux(other_resolved.RESULT).parse__number_single()
        else:
            other_final = other_resolved.RESULT
        return variant <= other_final

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def CMP_GL(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            edges_mode: str,
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        """
        NOTE
        ----
        used all variants of cmp (l/g* + *t/e) just to make a one clear logical func!
        intended using only one or two appropriate combination!
        """
        # schema
        if edges_mode[0].lower() == "t":
            edge_mode__greater = Validators.CMP_G_T
        else:
            edge_mode__greater = Validators.CMP_G_E

        if edges_mode[1].lower() == "t":
            edge_mode__lower = Validators.CMP_L_T
        else:
            edge_mode__lower = Validators.CMP_L_E

        for validator, variant in [
            (edge_mode__greater, variant[0]),
            (edge_mode__lower, variant[1]),
        ]:
            if variant is not None:
                if not validator(self, other_resolved, variant, parse__number_single=parse__number_single):
                    return False
        return True

    @staticmethod
    def CMP_GL_EE(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        return Validators.CMP_GL(
            self,
            other_resolved=other_resolved,
            variant=variant,
            edges_mode="ee",
            parse__number_single=parse__number_single,
        )

    @staticmethod
    def CMP_GL_TT(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        return Validators.CMP_GL(
            self,
            other_resolved=other_resolved,
            variant=variant,
            edges_mode="tt",
            parse__number_single=parse__number_single,
        )

    @staticmethod
    def CMP_GL_TE(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        return Validators.CMP_GL(
            self,
            other_resolved=other_resolved,
            variant=variant,
            edges_mode="te",
            parse__number_single=parse__number_single,
        )

    @staticmethod
    def CMP_GL_ET(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            parse__number_single: bool = None,
    ) -> bool | NoReturn:
        return Validators.CMP_GL(
            self,
            other_resolved=other_resolved,
            variant=variant,
            edges_mode="et",
            parse__number_single=parse__number_single,
        )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def CMP_LT_NumParsedSingle(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return Validators.CMP_L_T(self, other_resolved, variant, parse__number_single=True)

    @staticmethod
    def CMP_LE_NumParsedSingle(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return Validators.CMP_L_E(self, other_resolved, variant, parse__number_single=True)

    @staticmethod
    def CMP_GT_NumParsedSingle(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return Validators.CMP_G_T(self, other_resolved, variant, parse__number_single=True)

    @staticmethod
    def CMP_GE_NumParsedSingle(self, other_resolved: OtherResolved, variant: Any) -> bool | NoReturn:
        return Validators.CMP_G_E(self, other_resolved, variant, parse__number_single=True)

    @staticmethod
    def CMP_GL_NumParsedSingle(
            self,
            other_resolved: OtherResolved,
            variant: tuple[Any | None, Any | None],
            edges_mode: str,
    ) -> bool | NoReturn:
        return Validators.CMP_GL(self, other_resolved, variant, edges_mode, parse__number_single=True)

    # ==================================================================================================================
    @staticmethod
    def NumParsedSingle_Success(self, other_resolved: OtherResolved) -> bool:
        other_final = TextAux(other_resolved.RESULT).parse__number_single()
        return other_final is not None

    @staticmethod
    def NumParsedSingle_TypeInt(self, other_resolved: OtherResolved) -> bool:
        other_final = TextAux(other_resolved.RESULT).parse__number_single()
        return isinstance(other_final, int)

    @staticmethod
    def NumParsedSingle_TypeFloat(self, other_resolved: OtherResolved) -> bool:
        other_final = TextAux(other_resolved.RESULT).parse__number_single()
        return isinstance(other_final, float)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def Regexp(
            self,
            other_resolved: OtherResolved,
            pattern: str,
            ignorecase: bool = True,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        # NOTE: just a link!
        #   you can use directly match_link in Base_EqValid!!!!??? - no you need use it at least over LAMBDA!
        result = match_link(pattern=str(pattern), string=str(other_resolved.RESULT), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)
        return result is not None

    @staticmethod
    def RegexpFM(
            self,
            other_resolved: OtherResolved,
            pattern: str,
            ignorecase: bool = True,
    ) -> bool | NoReturn:
        return Validators.Regexp(
            self,
            other_resolved=other_resolved,
            pattern=pattern,
            ignorecase=ignorecase,
            match_link=re.fullmatch,
        )

    @staticmethod
    def RegexpSearch(
            self,
            other_resolved: OtherResolved,
            pattern: str,
            ignorecase: bool = True,
    ) -> bool | NoReturn:
        return Validators.Regexp(
            self,
            other_resolved=other_resolved,
            pattern=pattern,
            ignorecase=ignorecase,
            match_link=re.search,
        )

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def AttrsByKwargs(
            self,
            other_resolved: OtherResolved,
            **kwargs: TYPING.KWARGS_FINAL
    ) -> bool | NoReturn:
        for key, value in kwargs.items():
            value_expected = Lambda(value).resolve__style(EnumAdj_CallResolveStyle.EXC)
            value_other = AttrAux_Existed(other_resolved.RESULT).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    @staticmethod
    def AttrsByObj(
            self,
            other_resolved: OtherResolved,
            source: Any,
            attr_level: EnumAdj_AttrScope = EnumAdj_AttrScope.NOT_PRIVATE,
    ) -> bool | NoReturn:
        for key in AttrAux_Existed(source).iter__names_filter(attr_level):
            value_expected = AttrAux_Existed(source).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            value_other = AttrAux_Existed(other_resolved.RESULT).gai_ic__callable_resolve(key, EnumAdj_CallResolveStyle.EXC)
            if not EqAux(value_expected).check_doubleside__bool(value_other):
                return False

        # FINISH -----
        return True

    @staticmethod
    def AttrsByObj_NotPrivate(self, other_resolved: OtherResolved, source: Any) -> bool | NoReturn:
        return Validators.AttrsByObj(self, other_resolved=other_resolved, source=source, attr_level=EnumAdj_AttrScope.NOT_PRIVATE)

    @staticmethod
    def AttrsByObj_NotHidden(self, other_resolved: OtherResolved, source: Any) -> bool | NoReturn:
        return Validators.AttrsByObj(self, other_resolved=other_resolved, source=source, attr_level=EnumAdj_AttrScope.NOT_HIDDEN)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def AnnotsAllExists(self, other_resolved: OtherResolved) -> bool | NoReturn:
        return AttrAux_AnnotsAll(other_resolved.RESULT).annots__check_all_defined()

    # ==================================================================================================================
    @staticmethod
    def DictFull(self, other_resolved: OtherResolved, dictfull: dict[Any, Any | Base_EqValid]) -> bool | NoReturn:
        # use direct cmp!!!
        if not isinstance(other_resolved.RESULT, dict):
            return False

        return dictfull == other_resolved.RESULT

    @staticmethod
    def DictPart(self, other_resolved: OtherResolved, dictpart: dict[Any, Any | Base_EqValid]) -> bool | NoReturn:
        """
        GOAL
        validate only part of other
        """
        if not isinstance(other_resolved.RESULT, dict):
            return False

        for key, value in dictpart.items():
            if value != other_resolved.RESULT[key]:   # KEEP VALUE FIRTS!!!   # could raise
                return False                # on any fail return false

        return True

    # ------------------------------------------------------------------------------------------------------------------
    # @staticmethod
    # def JsonFull(self, other_resolved: OtherResolved, dictfull: dict[Any, Any | Base_EqValid]) -> bool | NoReturn:
    #     pass


# ======================================================================================================================
