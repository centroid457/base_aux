from typing import *
from .getattr_1_aux import GetattrAux


# =====================================================================================================================
class GetattrAnycase(GetattrAux):
    def __getattr__(self, item) -> Any | NoReturn:
        return GetattrAux._attr_anycase__get_value(item, self)

    def __getitem__(self, item) -> Any | NoReturn:
        return GetattrAux._attr_anycase__get_value(item, self)


# =====================================================================================================================
