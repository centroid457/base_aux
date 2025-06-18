from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# =====================================================================================================================
# @final      # NOTE: dont use FINAL HERE! - used for - EqRaise_Any!
class Base_EqValidChain(EqValid_EQ):
    """
    GOAL
    ----
    use args as variants to cmp each arg with otherValue

    NOTE
    ----
    it is just a link for EqValid_EQ BUT WITH ALL_TRUE!!! to use clear exact name!
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValidChain_All(Base_EqValidChain):
    """
    NOTE
    ----
    for Chain it is MOST USEFUL
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


@final
class EqValidChain_Any(Base_EqValidChain):
    """
    NOTE
    ----
    for Chain it is LESS USEFUL
    but created just to keep mirror
    """
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
