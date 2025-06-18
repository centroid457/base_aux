from typing import *
import time

from base_aux.base_nest_dunders.m1_init0_args_kwargs import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_values.m3_exceptions import Exx__Expected
from base_aux.aux_eq.m4_eq_valid_chain import *


# =====================================================================================================================
class Base_RaiseIf(NestInit_Args_Implicit):
    ARGS: Any | Callable[..., Any] = ()
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE

    def resolve(self) -> None | NoReturn:
        for arg_source in self.ARGS:
            arg_result = CallableAux(arg_source).resolve_bool()

            if self.IRESULT_CUMULATE == Enum_BoolCumulate.ANY_TRUE:
                if arg_result:
                    msg = f"{arg_source=}/{arg_result=}"
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
            raise Exx__Expected()


# ---------------------------------------------------------------------------------------------------------------------
class RaiseIf_Any(Base_RaiseIf):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE


class RaiseIf_All(Base_RaiseIf):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


# =====================================================================================================================
