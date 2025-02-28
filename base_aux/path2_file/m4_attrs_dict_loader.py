from typing import *

from base_aux.path2_file.m3_filetext import *

from base_aux.base_statics.m4_enums import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_text.m0_patterns import *
from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.base_resolver.m1_resolver import *
from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import *


# =====================================================================================================================
class AttrsDictTextFileLoader(TextFile, NestCall_Resolve):
    """
    GOAL
    ----
    load attrs as parsed dict
    main usage is final key values!
    used for get settings from file into NestInit_AnnotsAttrByKwArgsIc
    """
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = NestInit_AnnotsAttrByKwArgs
    STYLE: Any = DictTextFormat.AUTO
    KEYPATH: Iterable[str | int]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            target: type | Any = None,
            keypath: Iterable[str | int] = None,     # path to exact dict
            style: DictTextFormat = None,
            **kwargs,
    ) -> None | NoReturn:
        super().__init__(**kwargs)

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
