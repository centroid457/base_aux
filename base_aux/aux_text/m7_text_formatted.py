from typing import *
import re
import pytest

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
from base_aux.aux_expect.m1_expect_aux import *
from base_aux.aux_text.m6_nest_repr_clsname_str import *
from base_aux.versions.m2_version import *


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
    VALUES: AttrDump        # values set

    RAISE_TYPES: bool = False   # todo: decide to deprecate!

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, pat_format: str, *args: Any, raise_types: bool = None, **kwargs: Any) -> None:
        if raise_types is not None:
            self.RAISE_TYPES = raise_types

        self.PAT_FORMAT = pat_format

        self.init__keys()
        self.sai__values_args_kwargs(*args, **kwargs)
        self.init__types()

    # -----------------------------------------------------------------------------------------------------------------
    def init__keys(self) -> None:
        result_dict = {}
        for index, pat_group in enumerate(ReAttemptsAll(PatFormat.FIND_NAMES__IN_PAT).findall(self.PAT_FORMAT)):
            key, formatting = pat_group
            if not key:
                key = f"_{index}"
            result_dict.update({key: None})

        self.VALUES = AnnotAttrAux().annots__append(**result_dict)

    def sai__values_args_kwargs(self, *args, **kwargs) -> None | NoReturn:
        AnnotAttrAux(self.VALUES).sai__by_args_kwargs(*args, **kwargs)
        self.types__apply_on_values()

    def init__types(self) -> None:
        annots_dict = self.VALUES.__annotations__
        values_dict = AnnotAttrAux(self.VALUES).dump_dict()
        for name, type_i in annots_dict.items():
            if (type_i == Any) and (name in values_dict) and (values_dict[name] is not None):
                annots_dict[name] = type(values_dict[name])

    # -----------------------------------------------------------------------------------------------------------------
    def types__apply_on_values(self) -> None | NoReturn:
        annots_dict = self.VALUES.__annotations__
        values_dict = AnnotAttrAux(self.VALUES).dump_dict()
        for name, type_i in annots_dict.items():
            if (type_i != Any) and (name in values_dict) and (values_dict[name] is not None):
                value = values_dict[name]
                try:
                    value = type_i(value)
                except Exception as exx:
                    if self.RAISE_TYPES:
                        raise exx

                AnnotAttrAux(self.VALUES).sai__by_args_kwargs(**{name: value})

    def types__check_on_values(self) -> bool:
        """
        GOAL
        ----
        if you want to validate actual values
        """
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------
    # def __getattr__(self, item: str): # NOTE: DONT USE ANY GSAI HERE!!!
    #     return self[item]

    def __getitem__(self, item: str | int) -> Any | NoReturn:
        return IterAux(self.VALUES).value__get(item)

    # def __setattr__(self, item: str, value: Any):
    #     self[item] = value

    def __setitem__(self, item: str | int, value: Any) -> None | NoReturn:
        self.sai__values_args_kwargs(**{item: value})

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        self.types__apply_on_values()
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
                value = ""

            # apply type formatter ------
            try:
                formatter_type = formatter[-1]
                if formatter_type in ["s", ]:
                    value = str(value)
                elif formatter_type in ["d", "n"]:
                    value = int(value)
                elif formatter_type in ["f", "F"]:
                    value = float(value)
            except:
                pass

            # apply formatter -----------
            value_formatter = "{" + formatter + "}"
            try:
                value = value_formatter.format(value)
            except:
                pass

            result = re.sub(PatFormat.FIND_NAMES__IN_PAT, value, result, count=1)

            group_index += 1
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def other(self, other: str) -> Any | NoReturn:
        """
        GOAL
        ----
        reverse - parse result string back (get values)
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
        # kwargs preferred ---------------------------------
        victim = TextFormatted("hello {name}={value}", *(1, 2))
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == 1
        print(str(victim))
        assert str(victim) == "hello 1=2"

        victim.VALUES.name = "name"
        assert victim.VALUES.name == "name"
        print(str(victim))
        assert str(victim) == "hello name=2"

        # kwargs preferred ---------------------------------
        victim = TextFormatted("hello {name}={value}", "arg1", name="name", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "name"
        print(str(victim))
        assert str(victim) == "hello name=1"

        victim.VALUES.name = "name2"
        assert victim.VALUES.name == "name2"
        print(str(victim))
        assert str(victim) == "hello name2=1"

        # args ---------------------------------
        victim = TextFormatted("hello {name}={value}", "arg1", value=1)
        # assert victim.VALUES._0 == "arg1"
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

        victim.other("hello name_other=222")
        print(str(victim))
        assert victim.VALUES.name == "name_other"
        assert victim.VALUES.value == 222

        # EXX --------
        try:
            victim("hello  name_other=222")
            assert False
        except:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,_EXPECTED",
        argvalues=[
            ("hello {name}={value}", (), {}, "hello ="),
            ("hello {name}={value}", (), dict(name=1), "hello 1="),
            ("hello {name}={value}", (), dict(name=1, value=2), "hello 1=2"),
            ("hello {name}={value}", (11, 22), dict(name=1, value=2), "hello 1=2"),
            ("hello {name}={value}", (11, 22), dict(), "hello 11=22"),
            ("hello {name}={value}", (11, 22), dict(value=Version("1.2.3")), "hello 11=1.2.3"),
        ]
    )
    def test__str(self, pat_format, args, kwargs, _EXPECTED):
        func_link = lambda: str(TextFormatted(pat_format, *args, **kwargs))
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,_EXPECTED",
        argvalues=[
            ("hello{name}", (), dict(name=1), [int, 1]),
            ("hello{name}", (), dict(name="1"), [str, "1"]),
            ("hello{name}", (), dict(name=Version("1.2.3")), [Version, Version("1.2.3")]),
        ]
    )
    def test__type_apply(self, pat_format, args, kwargs, _EXPECTED):
        victim = TextFormatted(pat_format, *args, **kwargs)
        func_link = lambda: victim.VALUES.__annotations__["name"]
        ExpectAux(func_link).check_assert(_EXPECTED[0])

        func_link = lambda: getattr(victim.VALUES, "name")
        ExpectAux(func_link).check_assert(_EXPECTED[1])

        ExpectAux(lambda: victim.VALUES.name.__class__).check_assert(_EXPECTED[0])

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,new,_EXPECTED",
        argvalues=[
            ("hello{name}", (), dict(name=1), 1, [True, int, 1]),
            ("hello{name}", (), dict(name=1), "1", [True, int, 1]),
            ("hello{name}", (), dict(name=1), "text", [Exception, int, 1]),
            ("hello{name}", (), dict(name="1"), "text", [True, str, "text"]),
            ("hello{name}", (), dict(name="1"), "1", [True, str, "1"]),
            ("hello{name}", (), dict(name="1"), 1, [True, str, "1"]),
            ("hello{name}", (), dict(name=Version("1.2.3")), "1.2.3", [True, Version, Version("1.2.3")]),
        ]
    )
    def test__value_set(self, pat_format, args, new, kwargs, _EXPECTED):
        victim = TextFormatted(pat_format, *args, raise_types=True, **kwargs)

        # INCORRECT ------------------------------------
        # victim.VALUES.name = str(kwargs["name"])
        # func_link = lambda: victim.VALUES.name
        # ExpectAux(func_link).check_assert(_EXPECTED[1])
        #
        # ExpectAux(lambda: victim.VALUES.name.__class__).check_assert(_EXPECTED[0])

        # CORRECT ------------------------------------
        try:
            victim["name"] = new
            ExpectAux(True).check_assert(_EXPECTED[0])
        except:
            ExpectAux(Exception).check_assert(_EXPECTED[0])
            victim = TextFormatted(pat_format, *args, raise_types=False, **kwargs)
            victim["name"] = new    # NoRaise here!
            return
            pass

        ExpectAux(lambda: victim.VALUES.name.__class__).check_assert(_EXPECTED[1])

        func_link = lambda: victim.VALUES.name
        ExpectAux(func_link).check_assert(_EXPECTED[2])


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
