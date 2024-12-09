from typing import *
from .attr_1_aux import AttrAux


# =====================================================================================================================
class AttrAnycase:
    def __getattr__(self, item) -> Any | NoReturn:
        return AttrAux._getattr_anycase(item, self)

    def __setattr__(self, item, value) -> None | NoReturn:
        return AttrAux._setattr_anycase(item, value, self)

    # -----------------------------------------------------------------------------------------------------------------
    def __getitem__(self, item) -> Any | NoReturn:
        return AttrAux._getitem_anycase(item, self)

    def __setitem__(self, item, value) -> None | NoReturn:
        return AttrAux._setitem_anycase(item, value, self)


# =====================================================================================================================
