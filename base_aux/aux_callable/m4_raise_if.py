from typing import *
import time

from base_aux.base_nest_dunders.m1_init0_args_kwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_values.m3_exceptions import Exx__Expected
from base_aux.base_nest_dunders.m3_calls import *


# =====================================================================================================================
class Base_RaiseIf(NestInit_Args_Implicit, NestCall_Resolve):
    ARGS: Any | Callable[..., Any] = ()
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE

    RESOLVE_ON_INIT: bool = None

    def __init__(self, *args, resolve_on_init: bool = None, **kwargs) -> None | NoReturn:
        super().__init__(*args, **kwargs)

        if resolve_on_init is not None:
            self.RESOLVE_ON_INIT = bool(resolve_on_init)

        if self.RESOLVE_ON_INIT:
            self.resolve()

    def resolve(self) -> None | NoReturn:
        results_all = []
        for arg_source in self.ARGS:
            arg_result = CallableAux(arg_source).resolve_bool()
            results_all.append(arg_result)

            if self.IRESULT_CUMULATE == Enum_BoolCumulate.ANY_TRUE:
                if arg_result:
                    msg = f"{arg_source=}/{arg_result=}//{results_all=}"
                    raise Exx__Expected(msg)

            elif self.IRESULT_CUMULATE == Enum_BoolCumulate.ALL_TRUE:
                if arg_result:
                    continue
                else:
                    return

        # FINAL ---------
        if self.IRESULT_CUMULATE == Enum_BoolCumulate.ANY_TRUE:
            return
        else:
            raise Exx__Expected(f"{results_all=}")


# ---------------------------------------------------------------------------------------------------------------------
class RaiseIf_Any(Base_RaiseIf):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE


class RaiseIf_All(Base_RaiseIf):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


# =====================================================================================================================
