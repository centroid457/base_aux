from typing import *
import os
import re

from base_aux.aux_attr.m1_annot_attr1_aux import AttrAux_AnnotsAll
from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import NestInit_AnnotsAttrByKwArgs
from base_aux.base_nest_dunders.m3_calls import NestCall_Resolve


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
            AttrAux_AnnotsAll(self.TARGET).sai__by_args_kwargs(**data)
            result = self.TARGET

        return result


# =====================================================================================================================
