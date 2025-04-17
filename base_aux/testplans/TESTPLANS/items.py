from typing import *

from base_aux.testplans.tp_item import Base_TpItem
from base_aux.base_nest_dunders.m5_iter_annots_values import NestIter_AnnotValues
from . import item1__example


# =====================================================================================================================
class TpItems(NestIter_AnnotValues):
    TP_EXAMPLE: type[Base_TpItem] = item1__example.Tp_Example


# =====================================================================================================================
