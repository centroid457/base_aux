from typing import *

from base_aux.path2_file.m3_filetext import *

from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_text.m0_patterns import *
from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *


# =====================================================================================================================
class DictTextFileLoader(TextFile, NestCall_Resolve):
    """
    GOAL
    ----
    same as FileAux but with TextAux methods applied inplace!
    """
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = NestInit_AnnotsAttrByKwArgsIC
    STYLE: Any = None
    KEYPATH: Iterable[str, int]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            target: type | Any = None,
            style: DictTextFormat = DictTextFormat.EXTENTION,
            keypath: Iterable[str, int] = None,     # path to direct
            *args, **kwargs
    ) -> None | NoReturn:
        super().__init__(*args, **kwargs)

        self.init_style(style)

        if target is not None:
            self.TARGET = target

        self.KEYPATH = keypath or ()

    def init_style(self, style: DictTextFormat) -> None:
        if style is not None:
            self.STYLE = DictTextFormat(style)

        if self.STYLE == DictTextFormat.EXTENTION:
            for item in DictTextFormat:
                if self.FILEPATH.name.lower().endswith(str(item.value).lower()):
                    self.STYLE = item
                    break

        if self.STYLE == None:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def resolve(self) -> NestInit_AnnotsAttrByKwArgs | Any | NoReturn:
        # get dict -------
        data = {}

        if self.STYLE == DictTextFormat.INI:
            data = self.parse__dict_ini()

        elif self.STYLE == DictTextFormat.JSON:
            data = self.parse__dict_json()

        else:
            raise Exx__Incompatible(f"{self.STYLE=}/{self.TEXT=}")

        # load keypath ---
        if self.KEYPATH:
            data = IterAux(data).value__get(self.KEYPATH)

        # load args -------
        if TypeAux(self.TARGET).check__class() and issubclass(self.TARGET, NestInit_AnnotsAttrByKwArgs):
            # used for check Annots all inited!
            result = self.TARGET(**data)
        else:
            AnnotsAux(self.TARGET).set_annots_attrs__by_args_kwargs(**data)
            result = self.TARGET

        return result


# =====================================================================================================================
