from typing import *

from base_aux.aux_eq.m2_eq_valid2_validators import Validators
from base_aux.aux_eq.m2_eq_valid1_base import EqValid_Base
from base_aux.valid.m1_aux_valid_lg import *
from base_aux.aux_types.m0_types import *


# =====================================================================================================================
@final
class EqValid_VariantsDirect(EqValid_Base):
    VALIDATOR = Validators.VariantsDirect


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_VariantsStrLow(EqValid_Base):
    VALIDATOR = Validators.VariantsStrLow


# =====================================================================================================================
@final
class EqValid_Startswith(EqValid_Base):
    VALIDATOR = Validators.Startswith


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Endswith(EqValid_Base):
    VALIDATOR = Validators.Endswith


# =====================================================================================================================
@final
class EqValid_True(EqValid_Base):
    VALIDATOR = Validators.TRUE


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Raise(EqValid_Base):
    VALIDATOR = Validators.Raise


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_NotRaise(EqValid_Base):
    VALIDATOR = Validators.NotRaise


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_Exx(EqValid_Base):
    VALIDATOR = Validators.Exx


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_ExxRaise(EqValid_Base):
    VALIDATOR = Validators.ExxRaise


# =====================================================================================================================
@final
class EqValid_LtGt_Obj(EqValid_Base):
    VALIDATOR = Validators.LtGt_Obj


@final
class EqValid_LtGe_Obj(EqValid_Base):
    VALIDATOR = Validators.LtGe_Obj


@final
class EqValid_LeGt_Obj(EqValid_Base):
    VALIDATOR = Validators.LeGt_Obj


@final
class EqValid_LeGe_Obj(EqValid_Base):
    VALIDATOR = Validators.LeGe_Obj

# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_LtGt_SingleNumParced(EqValid_Base):
    VALIDATOR = Validators.LtGt_SingleNumParced


@final
class EqValid_LtGe_SingleNumParced(EqValid_Base):
    VALIDATOR = Validators.LtGe_SingleNumParced


@final
class EqValid_LeGt_SingleNumParced(EqValid_Base):
    VALIDATOR = Validators.LeGt_SingleNumParced


@final
class EqValid_LeGe_SingleNumParced(EqValid_Base):
    VALIDATOR = Validators.LeGe_SingleNumParced


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_SingleNumParced(EqValid_Base):
    VALIDATOR = Validators.SingleNumParced


# =====================================================================================================================
class EqValid_Regexp(EqValid_Base):
    VALIDATOR = Validators.Regexp
    BOOL_COLLECT: BoolCumulate = BoolCumulate.ALL_TRUE


# ---------------------------------------------------------------------------------------------------------------------
@final
class EqValid_RegexpAllTrue(EqValid_Regexp):
    BOOL_COLLECT: BoolCumulate = BoolCumulate.ALL_TRUE


@final
class EqValid_RegexpAnyTrue(EqValid_Regexp):
    BOOL_COLLECT: BoolCumulate = BoolCumulate.ANY_TRUE


@final
class EqValid_RegexpAllFalse(EqValid_Regexp):
    BOOL_COLLECT: BoolCumulate = BoolCumulate.ALL_FALSE


@final
class EqValid_RegexpAnyFalse(EqValid_Regexp):
    BOOL_COLLECT: BoolCumulate = BoolCumulate.ANY_FALSE


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
