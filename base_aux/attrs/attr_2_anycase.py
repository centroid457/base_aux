from typing import *
from .attr_1_aux import AttrAux


# =====================================================================================================================
class AttrAnycase:
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)

    def __setattr__(self, name, value) -> None | NoReturn:
        return AttrAux(self).anycase__setattr(name, value)

    # -----------------------------------------------------------------------------------------------------------------
    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getitem(name)

    def __setitem__(self, name, value) -> None | NoReturn:
        return AttrAux(self).anycase__setitem(name, value)


# =====================================================================================================================
