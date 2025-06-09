from base_aux.base_nest_dunders.m1_init0_args_kwargs import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_values.m3_exceptions import *
from base_aux.aux_values.m4_primitives import *


# =====================================================================================================================
@final
class EqArgs(NestInit_Args_Implicit, NestCall_Resolve, NestBool_Resolve):
    """
    GOAL
    ----
    return True if all Args equal (with first arg)
    """
    def resolve(self) -> bool | NoReturn:
        # only one chans for Raise - not enough count --------------
        if len(self.ARGS) < 2:
            msg = f"need at least 2 args {self.ARGS=}"
            raise Exx__WrongUsage(msg)

        arg_0 = self.ARGS[0]

        # any raise on comparisons - return False! --------------
        for arg_next in self.ARGS[1:]:
            try:
                if arg_0 != arg_next:
                    return False
            except:
                return False

        return True

    def __eq__(self, other: Any | bool) -> bool | NoReturn:
        if other:   # True
            result = bool(self.resolve())
        else:      # False
            result = bool(self.resolve())

        return result


# =====================================================================================================================
