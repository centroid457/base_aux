from typing import *
from .attr_1_aux import AttrAux


# =====================================================================================================================
class AttrAnycase:
    def __getattr__(self, item) -> Any | NoReturn:
        return AttrAux.anycase__getattr(item, self)

    def __setattr__(self, item, value) -> None | NoReturn:
        return AttrAux.anycase__setattr(item, value, self)

    # -----------------------------------------------------------------------------------------------------------------
    def __getitem__(self, item) -> Any | NoReturn:
        return AttrAux.anycase__getitem(item, self)

    def __setitem__(self, item, value) -> None | NoReturn:
        return AttrAux.anycase__setitem(item, value, self)


# =====================================================================================================================
