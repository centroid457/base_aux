from base_aux.base_statics.m4_enums import *
from base_aux.valid.m1_aux_valid_lg import *
from base_aux.aux_types.m1_type_aux import *


# =====================================================================================================================
class Validators:
    """
    GOAL
    ----
    collect all validators (funcs) in one place
    applicable in EqValid_Base only (by common way), but you can try using it separated!

    SPECIALLY CREATED FOR
    ---------------------
    EqValid_Base

    RULES
    -----
    1/ NoReturn - available for all returns as common!!! but sometimes it cant be reached (like TRUE/RAISE)
    """
    def VariantsDirect(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        if other_final in variants:
            return True
        else:
            return False

    def VariantsStrLow(self, other_final: Any, *variants: Any) -> bool | NoReturn:
        other_final = str(other_final).lower()
        variants = (str(var).lower() for var in variants)

        if other_final in variants:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def Startswith(self, other_final: Any, *variants: Any, ignorecase: bool = None) -> bool | NoReturn:
        if ignorecase:
            other_final = str(other_final).lower()
            variants = (str(var).lower() for var in variants)
        else:
            other_final = str(other_final)
            variants = (str(_) for _ in variants)

        for var in variants:
            if other_final.startswith(var):
                return True

        return False

    def Endswith(self, other_final: Any, *variants: Any, ignorecase: bool = None) -> bool | NoReturn:
        if ignorecase:
            other_final = str(other_final).lower()
            variants = (str(var).lower() for var in variants)
        else:
            other_final = str(other_final)
            variants = (str(_) for _ in variants)

        for var in variants:
            if other_final.endswith(var):
                return True

        return False

    # -----------------------------------------------------------------------------------------------------------------
    def TRUE(self, other_final: TYPE__VALID_BOOL__DRAFT, *v_args, **v_kwargs) -> bool:
        """
        GOAL
        ----
        True - if Other object called with no raise and no Exception in result
        """
        result = False
        if self.OTHER_RAISED or TypeAux(other_final).check__exception():
            return False

        return bool(other_final)

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
    def NumParsedSingle(self, other_final, expect: Any | None | bool | NumType = True) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(expect)

    def NumParsedSingle_Int(self, other_final) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(int)

    def NumParsedSingle_Float(self, other_final) -> bool:
        return ValidAux_NumParsedSingle(other_final).eq(float)

    # -----------------------------------------------------------------------------------------------------------------
    def Regexp(
            self,
            other_final,
            *regexps: str,
            ignorecase: bool = True,
            bool_collect: BoolCumulate = None,
            match_link: Callable = re.fullmatch,
    ) -> bool | NoReturn:
        bool_collect = bool_collect or self.BOOL_COLLECT

        for pattern in regexps:
            result_i = match_link(pattern=str(pattern), string=str(other_final), flags=re.RegexFlag.IGNORECASE if ignorecase else 0)

            # CUMULATE --------
            if bool_collect == BoolCumulate.ALL_TRUE:
                if not result_i:
                    return False
            elif bool_collect == BoolCumulate.ANY_TRUE:
                if result_i:
                    return True
            elif bool_collect == BoolCumulate.ALL_FALSE:
                if result_i:
                    return False
            elif bool_collect == BoolCumulate.ANY_FALSE:
                if not result_i:
                    return True

        # FINAL ------------
        if bool_collect in [BoolCumulate.ALL_TRUE, BoolCumulate.ALL_FALSE]:
            return True
        else:
            return False


# =====================================================================================================================
