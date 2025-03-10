from typing import *

from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_text.m5_re1_rexp import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.aux_attr.m1_attr2_nest8_iter_name_value import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *
from base_aux.aux_datetime.m1_datetime import *


# =====================================================================================================================
class FormatedLine(NestInit_SourceKwArgs_Implicite, NestCa):
    """
    GOAL
    ----
    access to formated values by value names

    SPECIALLY CREATED FOR
    ---------------------
    part for Alert messages
    """
    SOURCE: str     # FORMAT PATTERN

    def __getattr__(self, key):


    def __str__(self):
        result = ""
        for name, value in self.iter_exisded_name_value():
            name: str
            if name.startswith("_"):
                result += f"[{name}]{value}"
            else:
                result += f"{value}"

    def __repr__(self):
        return str(self)


# =====================================================================================================================
