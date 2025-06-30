from base_aux.base_enums.m1_enum0_nest_eq import *


# =====================================================================================================================
class EnumValue_Os(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os - deprecated - use KwargsEqExpect_OS
    """
    LINUX = "linux"
    WINDOWS = "windows"


# =====================================================================================================================
class EnumValue_MachineArch(NestEq_EnumAdj):
    """
    SPECIALLY CREATED FOR
    ---------------------
    ReqCheckStr_Os - deprecated - use KwargsEqExpect_OS
    """
    PC = "amd64"        # standard PC
    WSL = "x86_64"      # wsl standard
    ARM = "aarch64"     # raspberry=ARM!


# =====================================================================================================================
