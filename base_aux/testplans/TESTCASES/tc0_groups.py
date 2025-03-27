from typing import *

from base_aux.base_statics.m4_enums import NestEq_Enum
from base_aux.testplans.tc import Enum_TcGroup_Base


# =====================================================================================================================
class Enum_TcGroup(NestEq_Enum):
    G1 = "g1"
    G2 = "g2"
    G3 = "g3"
    G4 = "g4"


# =====================================================================================================================
if __name__ == "__main__":
    print(Enum_TcGroup_Base.NONE == Enum_TcGroup.G1)


# =====================================================================================================================
