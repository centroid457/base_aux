from typing import *

from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *


# =====================================================================================================================
class NestInit_AttrsByKwArgs:
    """
    GOAL
    ----
    create object with aux_attr as dict model / template

    SAME AS
    -------
    AttrAux.load_by_dict but more simple!

    SPECIALLY CREATED FOR
    ---------------------
    best way seems in test issues for base_aux.args

    NOTE
    ----
    used only acceptable items! no raise!
    """
    def __init__(self, *args, **kwargs) -> None | NoReturn:
        self.__init_args(*args)
        self.__init_kwargs(**kwargs)

    def __init_kwargs(self, **kwargs) -> None | NoReturn:
        for name, value in kwargs.items():
            try:
                setattr(self, name, value)
            except:
                pass

    def __init_args(self, *args) -> None | NoReturn:
        kwargs = dict.fromkeys(args)
        self.__init_kwargs(**kwargs)


# =====================================================================================================================
class NestInit_AttrsByKwArgsIc(NestInit_AttrsByKwArgs, NestGSAI_AttrAnycase):
    pass


# =====================================================================================================================
