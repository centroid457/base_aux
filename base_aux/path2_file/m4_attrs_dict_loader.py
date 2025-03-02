from typing import *
import pathlib
import os

from base_aux.path2_file.m3_filetext import *

from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_text.m0_patterns import *
from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *


# =====================================================================================================================
class AttrsLoader_DictTextFile(TextFile, NestCall_Resolve):
    """
    GOAL
    ----
    load attrs as parsed dict
    main usage is final key values!
    used for get settings from file into NestInit_AnnotsAttrByKwArgsIc
    """
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = Init_AnnotsAttrByKwArgs
    STYLE: DictTextFormat = DictTextFormat.AUTO
    KEYPATH: tuple[str | int] = ()

    FILEPATH: pathlib.Path
    TEXT: str

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            target: type | Any = None,
            keypath: tuple[str | int] = None,     # path to exact dict in dict
            style: DictTextFormat = None,

            **kwargs,       # init File/Text
    ) -> None | NoReturn:
        super().__init__(**kwargs)

        self.init_style(style)

        if target is not None:
            self.TARGET = target

        if keypath is not None:
            self.KEYPATH = keypath

    def init_style(self, style: DictTextFormat) -> None:
        if style is not None:
            self.STYLE = DictTextFormat(style)

        if self.STYLE == DictTextFormat.EXTENTION:
            for item in DictTextFormat:
                if self.FILEPATH.name.lower().endswith(str(item.value).lower()):
                    self.STYLE = item
                    break

        if self.STYLE is None:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> NestInit_AnnotsAttrByKwArgs | Any | NoReturn:
        # get dict -------
        data = self.parse__dict(self.STYLE)
        if data is None:
            raise Exx__Incompatible(f"{self.STYLE=}/{self.TEXT=}")

        # load keypath ---
        if self.KEYPATH:
            data = IterAux(data).value__get(*self.KEYPATH)

        # load args -------
        if TypeAux(self.TARGET).check__class() and issubclass(self.TARGET, NestInit_AnnotsAttrByKwArgs):
            # used for check Annots all inited!

            result = self.TARGET(**data)
        else:
            AnnotsAux(self.TARGET).set_annots_attrs__by_args_kwargs(**data)
            result = self.TARGET

        return result


# =====================================================================================================================
class PvLoaderIni(AttrsLoader_DictTextFile):
    """
    GOAL
    ----

    NOTE
    ----
    redefine only TARGET-kit/KEYPATH in __init
    """
    STYLE = DictTextFormat.INI
    FILEPATH = pathlib.Path.home().joinpath("pv.ini")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int]


class PvLoaderJson(AttrsLoader_DictTextFile):
    STYLE = DictTextFormat.JSON
    FILEPATH = pathlib.Path.home().joinpath("pv.json")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int]


# =====================================================================================================================
class PvLoaderEnv(NestCall_Resolve):
    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = Init_AnnotsAttrByKwArgs
    PATTS: tuple[str] = ()

    def __init__(
            self,
            target: type | Any = None,
            patts: tuple[str] = None,
            **kwargs,
    ) -> None | NoReturn:
        super().__init__(**kwargs)

        if target is not None:
            self.TARGET = target

        if patts is not None:
            self.PATTS = patts

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> NestInit_AnnotsAttrByKwArgs | Any | NoReturn:
        # get dict -------
        data = dict(os.environ)     # just a copy!

        # filter ---
        if self.PATTS:
            filterd_out = filter(lambda name: not any([re.search(pat, name) for pat in self.PATTS]), data)
            for out_i in filterd_out:
                data.pop(out_i)

        # load args -------
        if TypeAux(self.TARGET).check__class() and issubclass(self.TARGET, NestInit_AnnotsAttrByKwArgs):
            # used for check Annots all inited!

            result = self.TARGET(**data)
        else:
            AnnotsAux(self.TARGET).set_annots_attrs__by_args_kwargs(**data)
            result = self.TARGET

        return result


# ---------------------------------------------------------------------------------------------------------------------
def _explore():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
