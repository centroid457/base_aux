from typing import *
from .getattr_1_aux import GetattrAux


# =====================================================================================================================
class GetattrAnycase(GetattrAux):
    def __getattr__(self, item) -> Any | NoReturn:
        return GetattrAux._getattr_anycase(item, self)

    def __setattr__(self, item, value) -> None | NoReturn:
        return GetattrAux._setattr_anycase(item, value, self)

    def __getitem__(self, item) -> Any | NoReturn:
        return GetattrAux._getattr_anycase(item, self)


# =====================================================================================================================
