from typing import *


# =====================================================================================================================
@final
class AttrsInitByKwArgs:
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
    def __init__(self, *args, _RAISE__: bool = None, **kwargs) -> None | NoReturn:
        self.__init_args(*args)
        self.__init_kwargs(**kwargs, _RAISE_=_RAISE__)

    def __init_kwargs(self, _RAISE__: bool = None, **kwargs) -> None | NoReturn:
        for name, value in kwargs.items():
            try:
                setattr(self, name, value)
            except Exception as exx:
                if _RAISE__:
                    raise exx

    def __init_args(self, *args) -> None | NoReturn:
        kwargs = dict.fromkeys(args)
        self.__init_kwargs(**kwargs)


# =====================================================================================================================
