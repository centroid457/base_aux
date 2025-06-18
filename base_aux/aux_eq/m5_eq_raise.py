from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.aux_values.m3_exceptions import Exx__Expected
from base_aux.aux_eq.m4_eq_valid_chain import *


# =====================================================================================================================
class Base_EqRaise(Base_EqValidChain):
    """
    GOAL
    ----
    if other value validated with any variant - raise! otherwise return None

    SPECIALLY CREATED FOR
    ---------------------
    replace ClsInstPrefix Raise_If__*
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    MSG: str = None

    def __init__(self, *args, msg: str = None, **kwargs) -> None:
        if msg is not None:
            self.MSG = msg
        super().__init__(*args, **kwargs)

    def validate(self, other_draft: Any, *other_args, **other_kwargs) -> None | NoReturn:
        validated = super().validate(other_draft, *other_args, **other_kwargs)
        if validated:
            if self.MSG is not None:
                msg = str(self.MSG)
            else:
                msg = str(self)
            raise Exx__Expected(msg)


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqRaise_Any(Base_EqRaise):
    """
    NOTE
    ----
    for Raise it is MOST USEFUL
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE


@final
class EqRaise_All(Base_EqRaise):
    """
    NOTE
    ----
    for Chain it is LESS USEFUL
    but created just to keep mirror
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


# =====================================================================================================================
if __name__ == "__main__":
    pass

    1 == EqRaise_Any(0)

    try:
        1 == EqRaise_Any(1)
    except:
        assert True
    else:
        assert False


# =====================================================================================================================
