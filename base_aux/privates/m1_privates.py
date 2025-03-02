from typing import *
import os
import pathlib
import re

from base_aux.aux_attr.m2_annot1_aux import AnnotsAux
from base_aux.aux_types.m1_type_aux import TypeAux

from base_aux.base_inits.m3_nest_init_annots_attrs_by_kwargs import NestInit_AnnotsAttrByKwArgs
from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.base_resolver.m1_resolver import NestCall_Resolve
from base_aux.base_statics.m4_enums import DictTextFormat
from base_aux.path2_file.m4_attrs_dict_loader import AttrsLoader_DictTextFile


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
    KEYPATH: tuple[str | int, ...]


# =====================================================================================================================
class PvLoaderJson(AttrsLoader_DictTextFile):
    STYLE = DictTextFormat.JSON
    FILEPATH = pathlib.Path.home().joinpath("pv.json")

    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any
    KEYPATH: tuple[str | int, ...]


# =====================================================================================================================
class PvLoaderEnv(NestCall_Resolve):
    # INIT -------
    TARGET: type[NestInit_AnnotsAttrByKwArgs] | Any = AttrKit_Blank
    PATTS: tuple[str, ...] = ()

    def __init__(
            self,
            target: type | Any = None,
            patts: tuple[str, ...] = None,
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
            filtered_out = filter(lambda name: not any([re.search(pat, name, flags=re.IGNORECASE) for pat in self.PATTS]), list(data))
            for out_i in filtered_out:
                data.pop(out_i)

        # load args -------
        if TypeAux(self.TARGET).check__class() and issubclass(self.TARGET, NestInit_AnnotsAttrByKwArgs):
            # used for check Annots all inited!

            result = self.TARGET(**data)
        else:
            AnnotsAux(self.TARGET).set_annots_attrs__by_args_kwargs(**data)
            result = self.TARGET

        return result


# =====================================================================================================================
def _explore():
    pass


# =====================================================================================================================
if __name__ == "__main__":
    _explore()


# =====================================================================================================================
