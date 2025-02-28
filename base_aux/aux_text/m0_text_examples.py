from typing import *
from base_aux.base_statics.m4_enums import *
from base_aux.aux_values.m0_novalue import *


# =====================================================================================================================
class INI_EXAMPLES:
    # -------------------------
    NOT_MESHED__TEXT = """
    a0=00
    [S1]
    a1=11
    """
    NOT_MESHED__DICT_DIRECT = {
        "a0": "00",
        "DEFAULT": {
            "a0": "00",
        },
        "S1": {
            "a1": "11",
        },
    }
    NOT_MESHED__DICT_MERGED = {
        "a0": "00",
        "DEFAULT": {
            "a0": "00",
        },
        "S1": {
            "a0": "00",
            "a1": "11",
        },
    }

    # -------------------------
    MESHED__TEXT = """
    a0=00
    [S1]
    a0=11
    a1=11
    """
    MESHED__DICT_DIRECT = MESHED__DICT_MERGED = {
        "a0": "00",
        "DEFAULT": {
            "a0": "00",
        },
        "S1": {
            "a0": "11",
            "a1": "11",
        },
    }


# =====================================================================================================================
