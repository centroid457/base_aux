from base_aux.base_values.m5_enum0_nest_eq import *


# =====================================================================================================================
class EnumValue_Os(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os
    """
    LINUX = "linux"
    WINDOWS = "windows"


# =====================================================================================================================
class EnumValue_MachineArch(NestEq_Enum):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os
    """
    PC = "amd64"        # standard PC
    WSL = "x86_64"      # wsl standard
    ARM = "aarch64"     # raspberry=ARM!


# =====================================================================================================================
