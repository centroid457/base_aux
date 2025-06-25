from base_aux.aux_eq.m3_eq_valid2_validators import *
from base_aux.aux_eq.m3_eq_valid1_base import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_values.m5_enums import *


# =====================================================================================================================
@final
class EqValid_IsinstanceSameinstance(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.IsinstanceSameinstance


# =====================================================================================================================
@final
class EqValid_Contain(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.Contain


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_ContainStrIc(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.ContainStrIc


# =====================================================================================================================
@final
class EqValid_Startswith(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.Startswith


@final
class EqValid_StartswithIc(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.StartswithIc


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Endswith(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.Endswith


@final
class EqValid_EndswithIc(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.EndswithIc


# =====================================================================================================================
@final
class EqValid_BoolTrue(Base_EqValid):
    VALIDATOR = Validators.BoolTrue


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Raise(Base_EqValid):
    VALIDATOR = Validators.Raise


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_NotRaise(Base_EqValid):
    VALIDATOR = Validators.NotRaise


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Exx(Base_EqValid):
    VALIDATOR = Validators.Exx


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_ExxRaise(Base_EqValid):
    VALIDATOR = Validators.ExxRaise


# =====================================================================================================================
# @final    # DONT USE FINAL!!! need next in - CHAIN!!!
class EqValid_EQ(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.CMP_EQ

@final
class EqValid_EQ_StrIc(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.CMP_EQ__StrIc


# @final    # DONT USE FINAL!!! need next in - EqValid_NumParsedSingle_EQ!!!
class EqValid_EQ_NumParsedSingle(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.CMP_EQ__NumParsedSingle


# =====================================================================================================================
@final
class EqValid_LT(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_LT

@final
class EqValid_LE(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_LE

@final
class EqValid_GT(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_GT

@final
class EqValid_GE(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_GE

# --------------------------------
@final
class EqValid_LGTE(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_LGTE

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_LT_NumParsedSingle(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_LT_NumParsedSingle

@final
class EqValid_LE_NumParsedSingle(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_LE_NumParsedSingle

@final
class EqValid_GT_NumParsedSingle(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_GT_NumParsedSingle

@final
class EqValid_GE_NumParsedSingle(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE
    VALIDATOR = Validators.CMP_GE_NumParsedSingle

# --------------------------------
@final
class EqValid_LGTE_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.CMP_LGTE_NumParsedSingle

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_NumParsedSingle_Sucess(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle_Sucess


@final
class EqValid_NumParsedSingle_TypeInt(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle_TypeInt


@final
class EqValid_NumParsedSingle_TypeFloat(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle_TypeFloat

@final
class EqValid_NumParsedSingle_EQ(EqValid_EQ_NumParsedSingle):
    """
    just a link to keep name schema!
    """
    pass


# =====================================================================================================================
class EqValid_Regexp(Base_EqValid):
    """
    NOTE
    ----
    for one regexp - simply use this EqValid_Regexp
    for several patterns - use other classes for clarification!
    """
    VALIDATOR = Validators.Regexp
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_RegexpAllTrue(EqValid_Regexp):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE


@final
class EqValid_RegexpAnyTrue(EqValid_Regexp):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE


@final
class EqValid_RegexpAllFalse(EqValid_Regexp):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_FALSE


@final
class EqValid_RegexpAnyFalse(EqValid_Regexp):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_FALSE


# =====================================================================================================================
@final
class EqValid_AttrsByKwargs(Base_EqValid):
    VALIDATOR = Validators.AttrsByKwargs


# ---------------------------------------------------------------------------------------------------------------------
# @final
# class EqValid_AttrsByObj(Base_EqValid):
#     VALIDATOR = Validators.AttrsByObj
#     ATTR_LEVEL: Enum_AttrScope = Enum_AttrScope.NOT_PRIVATE


@final
class EqValid_AttrsByObjNotPrivate(Base_EqValid):
    VALIDATOR = Validators.AttrsByObj
    ATTR_LEVEL: Enum_AttrScope = Enum_AttrScope.NOT_PRIVATE


@final
class EqValid_AttrsByObjNotHidden(Base_EqValid):
    VALIDATOR = Validators.AttrsByObj
    ATTR_LEVEL: Enum_AttrScope = Enum_AttrScope.NOT_HIDDEN


def _explore():
    class Cls:
        o = 1
        _h = 1
        __p = 1

    source = Cls()
    other = Cls()
    ev = EqValid_AttrsByObjNotPrivate(source)
    print(f"{ev=}")
    print(f"{ev == other}")


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_AnnotsAllExists(Base_EqValid):
    VALIDATOR = Validators.AnnotsAllExists


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
