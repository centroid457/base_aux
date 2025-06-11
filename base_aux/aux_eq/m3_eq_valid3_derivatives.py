from base_aux.aux_eq.m3_eq_valid2_validators import *
from base_aux.aux_eq.m3_eq_valid1_base import *
from base_aux.aux_values.m2_types import *
from base_aux.aux_values.m5_enums import *


# =====================================================================================================================
@final
class EqValid_Isinstance(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.Isinstance


# =====================================================================================================================
@final
class EqValid_Variant(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.Variant


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_VariantStrIc(Base_EqValid):
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ANY_TRUE
    VALIDATOR = Validators.VariantStrIc


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
@final
class EqValid_LtGt_Obj(Base_EqValid):
    VALIDATOR = Validators.LtGt_Obj


@final
class EqValid_LtGe_Obj(Base_EqValid):
    VALIDATOR = Validators.LtGe_Obj


@final
class EqValid_LeGt_Obj(Base_EqValid):
    VALIDATOR = Validators.LeGt_Obj


@final
class EqValid_LeGe_Obj(Base_EqValid):
    VALIDATOR = Validators.LeGe_Obj

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_LtGt_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.LtGt_NumParsedSingle


@final
class EqValid_LtGe_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.LtGe_NumParsedSingle


@final
class EqValid_LeGt_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.LeGt_NumParsedSingle


@final
class EqValid_LeGe_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.LeGe_NumParsedSingle


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_NumParsedSingle(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle


@final
class EqValid_NumParsedSingle_TypeInt(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle_TypeInt


@final
class EqValid_NumParsedSingle_TypeFloat(Base_EqValid):
    VALIDATOR = Validators.NumParsedSingle_TypeFloat


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
