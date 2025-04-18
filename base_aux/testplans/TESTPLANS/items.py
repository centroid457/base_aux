from typing import *

from base_aux.testplans.tp_item import Base_TpItem
from base_aux.base_nest_dunders.m5_iter_annots_values import NestIter_AnnotValues

from .DEVICES import atc, ptb, breeders
from .Example import (
    tc1_direct,
    tc2_reverse,
    tc3_atc,
)


# =====================================================================================================================
class Tp_Example(Base_TpItem):
    NAME = "Tp_Example"
    DEV_BREEDER = breeders.DevicesBreeder__AtcPtbDummy
    TCS_CLS = {
        tc1_direct.TestCase: True,
        tc2_reverse.TestCase: True,
    }


# =====================================================================================================================
class Tp_Psu800(Base_TpItem):
    NAME = "Tp_Example2"
    DEV_BREEDER = breeders.DevicesBreeder__Psu800
    TCS_CLS = {
        tc2_reverse.TestCase: True,
        tc1_direct.TestCase: True,
        tc3_atc.TestCase: True,
    }


# =====================================================================================================================
class TpItems(NestIter_AnnotValues):
    TP_EXAMPLE: type[Base_TpItem] = Tp_Example
    TP_PSU800: type[Base_TpItem] = Tp_Psu800


# =====================================================================================================================
