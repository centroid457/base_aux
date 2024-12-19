from typing import *
from .attr_1_aux import AttrAux


# =====================================================================================================================
class AttrAnycase:
    def __getattr__(self, item) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(item)

    def __setattr__(self, item, value) -> None | NoReturn:
        return AttrAux(self).anycase__setattr(item, value)

    # -----------------------------------------------------------------------------------------------------------------
    def __getitem__(self, item) -> Any | NoReturn:
        return AttrAux(self).anycase__getitem(item)

    def __setitem__(self, item, value) -> None | NoReturn:
        return AttrAux(self).anycase__setitem(item, value)


# =====================================================================================================================
