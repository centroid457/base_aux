from typing import *

from base_aux.aux_text.m5_re2_attemps import *
from base_aux.aux_attr.m4_kits import *
from base_aux.base_lambdas.m1_lambda import *
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
class TextFormatted(
    NestCall_Other,
    # NestRepr__ClsName_SelfStr     # use manual
):
    """
    GOAL
    ----
    access to formated values by value names

    SPECIALLY CREATED FOR
    ---------------------
    part for Alert messages

    NOTE
    ----
    1/ formatters is not tested and could not working!
    """
    PAT_FORMAT: str = ""    # FORMAT PATTERN
    VALUES: AttrDumped        # values set

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

        self.VALUES = AttrAux_AnnotsAll().annots__append(**result_dict)

    def sai__values_args_kwargs(self, *args, **kwargs) -> None | NoReturn:
        AttrAux_AnnotsAll(self.VALUES).sai__by_args_kwargs(*args, **kwargs)
        self.types__apply_on_values()

    def init__types(self) -> None:
        annots_dict = self.VALUES.__annotations__
        values_dict = AttrAux_AnnotsAll(self.VALUES).dump_dict()
        for name, type_i in annots_dict.items():
            if (type_i == Any) and (name in values_dict) and (values_dict[name] is not None):
                annots_dict[name] = type(values_dict[name])

    # -----------------------------------------------------------------------------------------------------------------
    def types__apply_on_values(self) -> None | NoReturn:
        annots_dict = self.VALUES.__annotations__
        values_dict = AttrAux_AnnotsAll(self.VALUES).dump_dict()
        for name, type_i in annots_dict.items():
            if (type_i != Any) and (name in values_dict) and (values_dict[name] is not None):
                value = values_dict[name]
                try:
                    value = type_i(value)
                except Exception as exx:
                    if self.RAISE_TYPES:
                        raise exx

                AttrAux_AnnotsAll(self.VALUES).sai__by_args_kwargs(**{name: value})

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
        values = AttrAux_AnnotsAll(self.VALUES).dump_dict()
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

    def __repr__(self):
        values = AttrAux_AnnotsAll(self.VALUES).dump_dict()
        result = f"{self.__class__.__name__}({self})"
        result += f"kwargs={values}"
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
            # values = [value.strip() for value in values]  # DONT DO STRIP!!!
            self.sai__values_args_kwargs(*values)
        else:
            raise Exx__Incompatible(f"{other=}, {self.PAT_FORMAT=}")

        print(self)


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
