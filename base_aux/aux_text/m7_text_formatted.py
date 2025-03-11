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
    FIND_NAMES__IN_PAT: str = r"\{([_a-zA-Z]\w*)?([^{}]*)\}"   # (key, key_formatter)  dont use indexes!

    @classmethod
    @property
    def SPLIT_STATIC__IN_PAT(cls) -> str:
        result = r"(?:" + re.sub(r"\((.*?)\)", r"(?:\1)", cls.FIND_NAMES__IN_PAT) + r")"
        return result


# =====================================================================================================================
class TextFormatted(NestCall_Other, NestRepr__ClsName_SelfStr):
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
        self.sai__values_args_kwargs(*args, **kwargs)

    def init__keys(self):
        result_dict = {}
        for index, pat_group in enumerate(ReAttemptsAll(PatFormat.FIND_NAMES__IN_PAT).findall(self.PAT_FORMAT)):
            key, formatting = pat_group
            if not key:
                key = f"_{index}"
            result_dict.update({key: None})

        self.VALUES = AnnotAttrAux().annots__append(**result_dict)

    # -----------------------------------------------------------------------------------------------------------------
    def sai__values_args_kwargs(self, *args, **kwargs) -> bool:
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
            match = re.search(PatFormat.FIND_NAMES__IN_PAT, result)
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

            result = re.sub(PatFormat.FIND_NAMES__IN_PAT, value_formatted, result, count=1)

            group_index += 1
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def other(self, other: str) -> Any | NoReturn:
        """
        GOAL
        ----
        parse result string back (get values)
        """
        static_data = re.split(PatFormat.SPLIT_STATIC__IN_PAT, self.PAT_FORMAT)
        pat_values_fullmatch = r""
        for static_i in static_data:
            if pat_values_fullmatch:
                pat_values_fullmatch += r"(.*)"

            pat_values_fullmatch += re.escape(static_i)

        values_match = re.fullmatch(pat_values_fullmatch, other)
        if values_match:
            values = values_match.groups()
            self.sai__values_args_kwargs(*values)
        else:
            raise Exx__Incompatible(f"{other=}, {self.PAT_FORMAT=}")


# =====================================================================================================================
class Test_Formatted:
    def test__pat_groups(self):
        assert PatFormat.SPLIT_STATIC__IN_PAT == r"(?:\{(?:[_a-zA-Z]\w*)?(?:[^{}]*)\})"

    def test__simple(self):
        victim = TextFormatted("{}", 1)
        assert victim.VALUES._0 == 1

        print("{}".format(1))
        print(str(victim))
        assert str(victim) == "1"

    def test__kwargs(self):
        victim = TextFormatted("hello {name}={value}", "arg1", name="name", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "name"
        print(str(victim))
        assert str(victim) == "hello name=1"

        victim.VALUES.name = "name2"
        assert victim.VALUES.name == "name2"
        print(str(victim))
        assert str(victim) == "hello name2=1"

        # ---------------------------------
        victim = TextFormatted("hello {name}={value}", "arg1", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "arg1"
        print(str(victim))
        assert str(victim) == "hello arg1=1"

    def test__other(self):
        # OK --------
        victim = TextFormatted("hello {name}={value}", "arg1", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "arg1"
        print(str(victim))
        assert str(victim) == "hello arg1=1"

        victim("hello name_other=222")
        assert victim.VALUES.name == "name_other"
        assert victim.VALUES.value == "222"

        # EXX --------
        try:
            victim("hello  name_other=222")
            assert False
        except:
            pass


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
