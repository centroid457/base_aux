from base_aux.base_nest_dunders.m1_init1_args_kwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_values.m3_exceptions import Exc__ExpectedAnother
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
class Base_ArgsBoolIf(NestInit_Args_Implicit, NestCall_Resolve):
    """
    GOAL
    ----
    check args (callables acceptable)
    and raise if True
    """
    ARGS: Any | Callable[..., Any] = ()
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_TRUE

    RAISE_INSTEAD_TRUE: bool = None  # RAISE_INSTEAD_TRUE
    RAISE_ON_INIT: bool = None

    def __init__(self, *args, _iresult_cumulate: EnumAdj_BoolCumulate = None, _raise_instead_true: bool = None, raise_on_init: bool = None, **kwargs) -> None | NoReturn:
        super().__init__(*args, **kwargs)

        if _iresult_cumulate is not None:
            self.IRESULT_CUMULATE = _iresult_cumulate

        if _raise_instead_true is not None:
            self.RAISE_INSTEAD_TRUE = bool(_raise_instead_true)

        if raise_on_init is not None:
            self.RAISE_ON_INIT = bool(raise_on_init)

        if self.RAISE_ON_INIT and self.RAISE_INSTEAD_TRUE:
            self.resolve()

    def resolve(self) -> bool | NoReturn:
        results_all = []
        for arg_source in self.ARGS:
            arg_result = Lambda(arg_source).resolve__bool()
            results_all.append(arg_result)

            if self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ALL_TRUE:
                if arg_result:
                    continue
                else:
                    return False

            elif self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ALL_FALSE:
                if not arg_result:
                    continue
                else:
                    return False

            elif self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ANY_TRUE:
                if arg_result:
                    if self.RAISE_INSTEAD_TRUE:
                        msg = f"{arg_source=}/{arg_result=}//{results_all=}"
                        raise Exc__ExpectedAnother(msg)
                    else:
                        return True

            elif self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ANY_FALSE:
                if not arg_result:
                    if self.RAISE_INSTEAD_TRUE:
                        msg = f"{arg_source=}/{arg_result=}//{results_all=}"
                        raise Exc__ExpectedAnother(msg)
                    else:
                        return True

        # FINAL ---------
        if self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ANY_TRUE or self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ANY_FALSE:
            return False
        else:   # self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ALL_TRUE or self.IRESULT_CUMULATE == EnumAdj_BoolCumulate.ALL_FALSE
            if self.RAISE_INSTEAD_TRUE:
                msg = f"{results_all=}"
                raise Exc__ExpectedAnother(msg)
            else:
                return True


# =====================================================================================================================
class ArgsBoolIf_AllTrue(Base_ArgsBoolIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE


class ArgsBoolIf_AnyTrue(Base_ArgsBoolIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_TRUE


class ArgsBoolIf_AllFalse(Base_ArgsBoolIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_FALSE


class ArgsBoolIf_AnyFalse(Base_ArgsBoolIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_FALSE


# =====================================================================================================================
class Base_ArgsRaiseIf(Base_ArgsBoolIf):
    RAISE_INSTEAD_TRUE: bool = True


# ---------------------------------------------------------------------------------------------------------------------
class ArgsRaiseIf_AllTrue(Base_ArgsRaiseIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE


class ArgsRaiseIf_AnyTrue(Base_ArgsRaiseIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_TRUE


class ArgsRaiseIf_AllFalse(Base_ArgsRaiseIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_FALSE


class ArgsRaiseIf_AnyFalse(Base_ArgsRaiseIf):
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_FALSE


# ---------------------------------------------------------------------------------------------------------------------
class ArgsRaiseIfOnInit_AllTrue(ArgsRaiseIf_AllTrue):
    RAISE_ON_INIT: bool = True


class ArgsRaiseIfOnInit_AnyTrue(ArgsRaiseIf_AnyTrue):
    RAISE_ON_INIT: bool = True


class ArgsRaiseIfOnInit_AllFalse(ArgsRaiseIf_AllFalse):
    RAISE_ON_INIT: bool = True


class ArgsRaiseIfOnInit_AnyFalse(ArgsRaiseIf_AnyFalse):
    RAISE_ON_INIT: bool = True


# =====================================================================================================================
