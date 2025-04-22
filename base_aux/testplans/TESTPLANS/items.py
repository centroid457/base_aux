from typing import *

from base_aux.testplans.tp_item import Base_TpItem
from base_aux.base_nest_dunders.m5_iter_annots_values import NestIter_AnnotValues

from .DEVICES import atc, ptb, breeders
from .Example import (
    tc1_direct,
    tc2_reverse,
    tc3_atc,
)
from .psu800 import (
    tc1_none_1_exist_psu,
    tc1_none_2_test_gnd,
    tc1_none_3_off,
    tc1_none_4_on,

    tc2_ext_1_test_pmbus,
    tc2_ext_2_off,
    tc2_ext_3_on,

    tc3_hv_1_off,
    tc3_hv_2_on,

    tc4_hv_1_test_SC12S,
    tc4_hv_2_test_SC12M,
    tc4_hv_3_test_LD12S,
    tc4_hv_4_test_LOAD,

    tc8_hv1_150_off,
    tc8_hv2_160_on,
    tc8_hv3_250_on,
    tc8_hv4_260_off,
)


# =====================================================================================================================
class Tp_Example(Base_TpItem):
    NAME = "пример с пустыми устройствами"
    DEV_BREEDER = breeders.DevicesBreeder__AtcPtbDummy
    TCS_CLS = {
        tc1_direct.TestCase: True,
        tc2_reverse.TestCase: True,
    }


# =====================================================================================================================
class Tp_Example2(Base_TpItem):
    NAME = "пример с реальными устройствами"
    DEV_BREEDER = breeders.DevicesBreeder__Psu800
    TCS_CLS = {
        tc1_direct.TestCase: True,
        tc2_reverse.TestCase: True,
        tc3_atc.TestCase: True,
    }


# =====================================================================================================================
class Tp_Psu800(Base_TpItem):
    NAME = "ОТК БП800"
    DEV_BREEDER = breeders.DevicesBreeder__Psu800
    TCS_CLS = {
        tc1_none_1_exist_psu.TestCase: True,
        tc1_none_2_test_gnd.TestCase: True,
        tc1_none_3_off.TestCase: True,
        tc1_none_4_on.TestCase: True,

        tc2_ext_1_test_pmbus.TestCase: True,
        tc2_ext_2_off.TestCase: True,
        tc2_ext_3_on.TestCase: True,

        tc3_hv_1_off.TestCase: True,
        tc3_hv_2_on.TestCase: True,

        tc4_hv_1_test_SC12S.TestCase: True,
        tc4_hv_2_test_SC12M.TestCase: True,
        tc4_hv_3_test_LD12S.TestCase: True,
        tc4_hv_4_test_LOAD.TestCase: True,

        tc8_hv1_150_off.TestCase: True,
        tc8_hv2_160_on.TestCase: True,
        tc8_hv3_250_on.TestCase: True,
        tc8_hv4_260_off.TestCase: True,
    }


# =====================================================================================================================
class TpItems(NestIter_AnnotValues):
    TP_EXAMPLE: type[Base_TpItem] = Tp_Example
    TP_EXAMPLE2: type[Base_TpItem] = Tp_Example2
    TP_PSU800: type[Base_TpItem] = Tp_Psu800


# =====================================================================================================================
