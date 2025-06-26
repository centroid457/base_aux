from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_values.m3_exceptions import Exx__Expected
from base_aux.aux_eq.m4_eq_valid_chain import *


# =====================================================================================================================
class Base_EqRaiseIf(Base_EqValidChain):
    """
    GOAL
    ----
    if other value validated with any variant - raise! otherwise return None

    SPECIALLY CREATED FOR
    ---------------------
    replace ClsInstPrefix Raise_If__*
    """
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_TRUE
    MSG: str = None

    def __init__(self, *args, msg: str = None, **kwargs) -> None:
        if msg is not None:
            self.MSG = msg
        super().__init__(*args, **kwargs)

    def resolve(self, other_draft: Any, *other_args, **other_kwargs) -> None | NoReturn:
        validated = super().resolve(other_draft, *other_args, **other_kwargs)
        if validated:
            if self.MSG is not None:
                msg = str(self.MSG)
            else:
                msg = str(self)
            raise Exx__Expected(msg)


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqRaiseIf_Any(Base_EqRaiseIf):
    """
    NOTE
    ----
    for Raise it is MOST USEFUL
    """
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ANY_TRUE


@final
class EqRaiseIf_All(Base_EqRaiseIf):
    """
    NOTE
    ----
    for Chain it is LESS USEFUL
    but created just to keep mirror
    """
    IRESULT_CUMULATE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE


# =====================================================================================================================
if __name__ == "__main__":
    pass

    1 == EqRaiseIf_Any(0)

    try:
        1 == EqRaiseIf_Any(1)
    except:
        assert True
    else:
        assert False


# =====================================================================================================================
