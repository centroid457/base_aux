from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_dict.m3_dict_ga1_simple import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_eq.m1_eq_args import *


# =====================================================================================================================
class DictDiff(NestCall_Resolve):
    """
    GOAL
    ----
    get diffs from several states,
    dicts assumed like AttrDumped objects - so keys are STR.

    SPECIALLY CREATED FOR
    ---------------------
    cmp two objects by attr values
    """
    DICTS: tuple[TYPING.DICT_STR_ANY, ...]

    def __init__(self, *dicts: TYPING.DICT_STR_ANY):
        self.DICTS = dicts

    def resolve(self) -> dict[str, tuple[Any, ...]] | NoReturn:
        keys: list[str] = [key for DICT in self.DICTS for key in DICT]
        keys = sorted(keys)

        result = {}
        for key in keys:
            # values collect -------
            values = []
            for DICT in self.DICTS:
                try:
                    value = DICT[key]
                except Exception as exx:
                    value = exx

                values.append(value)

            # values check -------
            if EqArgs(*values):




# =====================================================================================================================
