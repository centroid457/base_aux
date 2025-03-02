from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.path2_file.m3_filetext import *
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
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = AttrKit_Blank
    STYLE: DictTextFormat = DictTextFormat.AUTO
    KEYPATH: tuple[str | int, ...] = ()

    FILEPATH: pathlib.Path
    TEXT: str

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            target: type | Any = None,
            keypath: tuple[str | int, ...] = None,     # path to exact dict in dict
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
if __name__ == "__main__":
    pass


# =====================================================================================================================
