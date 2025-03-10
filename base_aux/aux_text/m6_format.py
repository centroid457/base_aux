from typing import *
import re

from base_aux.base_inits.m1_nest_init_source import *
from base_aux.aux_callable.m2_nest_calls import *
from base_aux.aux_text.m5_re1_rexp import *
from base_aux.aux_text.m5_re2_attemps import *
from base_aux.aux_iter.m1_iter_aux import *
from base_aux.aux_attr.m1_attr2_nest8_iter_name_value import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *
from base_aux.aux_datetime.m1_datetime import *
from base_aux.aux_attr.m4_dump import AttrDump
from base_aux.aux_attr.m4_kits import *


# =====================================================================================================================
class PatFormat:
    FIND_GROUPS: str = r"\{([a-zA-Z]*)([^{}]*)\}"   # (key, format)


class FormatedLine(NestCall_Other):
    """
    GOAL
    ----
    access to formated values by value names

    SPECIALLY CREATED FOR
    ---------------------
    part for Alert messages
    """
    PAT_FORMAT: str = ""    # FORMAT PATTERN
    PAT_RE: str = r""       # RE PATTERN
    VALUES: AttrDump        # values set

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, pat_format: str, *args: Any, **kwargs: Any) -> None:
        self.PAT_FORMAT = pat_format

        self.init__keys()
        # self.sai_args_kwargs(*args, **kwargs)

    def init__keys(self):
        result_dict = {}
        for index, pat_group in enumerate(ReAttemptsAll(PatFormat.FIND_GROUPS).findall(self.PAT_FORMAT)):
            key, formatting = pat_group
            if not key:
                key = f"_{index}"
            result_dict.update({key: None})

        self.VALUES = AnnotAttrAux.annots__make_object(**result_dict)

    # -----------------------------------------------------------------------------------------------------------------
    def init__values_args_kwargs(self, *args, **kwargs) -> bool:
        for index, value in enumerate(args):
            self[index] = value

        for key, value in kwargs.items():
            self[key] = value

        return True




    # def __getattr__(self, item: str): # NOTE: DONT USE ANY GSAI HERE!!!
    #     return self[item]
    #
    # def __getitem__(self, item: str | int):
    #     if isinstance(item, str):
    #         for key in self.VALUES:
    #             if key.lower() == item.lower():
    #                 return self.VALUES[key]
    #     elif isinstance(item, int):
    #         key = list(self.VALUES)[item]
    #         return self.VALUES[key]
    #
    #     raise AttributeError(item)
    #
    # def __setattr__(self, item: str, value: Any):
    #     self[item] = value
    #
    # def __setitem__(self, item: str | int, value: Any):
    #     if isinstance(item, str):
    #         for key in self.VALUES:
    #             if key.lower() == item.lower():
    #                 self.VALUES[key] = value
    #                 return
    #     elif isinstance(item, int):
    #         key = list(self.VALUES)[item]
    #         self.VALUES[key] = value
    #         return
    #
    #     raise AttributeError(item)

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.PAT_FORMAT.format(self.VALUES)

    def __repr__(self):
        return str(self)


# =====================================================================================================================
if __name__ == "__main__":
    victim = FormatedLine("{}", 1)
    assert victim.VALUES._0 == 1


# =====================================================================================================================
