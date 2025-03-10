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
from base_aux.aux_text.m6_nest_repr_clsname_str import *


# =====================================================================================================================
class PatFormat:
    FIND_GROUPS: str = r"\{([_a-zA-Z][_a-zA-Z01-9]*)?([^{}]*)\}"   # (key, formatter)


class FormatedLine(NestCall_Other, NestRepr__ClsName_SelfStr):
    """
    GOAL
    ----
    access to formated values by value names

    SPECIALLY CREATED FOR
    ---------------------
    part for Alert messages
    """
    PAT_FORMAT: str = ""    # FORMAT PATTERN
    # PAT_RE: str = r""       # RE PATTERN
    VALUES: AttrDump        # values set

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, pat_format: str, *args: Any, **kwargs: Any) -> None:
        self.PAT_FORMAT = pat_format

        self.init__keys()
        self.init__values_args_kwargs(*args, **kwargs)

    def init__keys(self):
        result_dict = {}
        for index, pat_group in enumerate(ReAttemptsAll(PatFormat.FIND_GROUPS).findall(self.PAT_FORMAT)):
            key, formatting = pat_group
            if not key:
                key = f"_{index}"
            result_dict.update({key: None})

        self.VALUES = AnnotAttrAux().annots__append(**result_dict)

    # -----------------------------------------------------------------------------------------------------------------
    def init__values_args_kwargs(self, *args, **kwargs) -> bool:
        return AnnotAttrAux(self.VALUES).sai__by_args_kwargs(*args, **kwargs)

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
    def __str__(self) -> str:
        result = str(self.PAT_FORMAT)
        values = AnnotAttrAux(self.VALUES).dump_dict()
        group_index = 0
        while True:
            match = re.search(PatFormat.FIND_GROUPS, result)
            if not match:
                break

            name, formatter = match.groups()
            name = name or f"_{group_index}"
            name_orig = IterAux(values).item__get_original(name)
            value = values[name_orig]
            if value is None:
                value=""
            value_formatter = "{" + formatter + "}"
            value_formatted = value_formatter.format(value)

            result = re.sub(PatFormat.FIND_GROUPS, value_formatted, result, count=1)

            group_index += 1
        return result


# =====================================================================================================================
if __name__ == "__main__":
    victim = FormatedLine("{}", 1)
    assert victim.VALUES._0 == 1

    print("{}".format(1))
    print(str(victim))
    assert str(victim) == "1"


    victim = FormatedLine("hello {name}={value}", 1, name="name", value="value")
    # assert victim.VALUES._1 == 1
    assert victim.VALUES.name == "name"
    print(str(victim))
    assert str(victim) == "hello name=value"

    victim.VALUES.name = "name2"
    assert victim.VALUES.name == "name2"
    print(str(victim))
    assert str(victim) == "hello name2=value"


# =====================================================================================================================
