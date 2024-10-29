from typing import *
from funcs_aux import ValueNotExist


# =====================================================================================================================
class GetattrAux:
    """
    NOTICE
    ------
    if there are several same attrs in different cases - you should resolve it by yourself!
    """
    @classmethod
    def _attr_anycase__get_name(cls, item: str | Any, obj: Any = ValueNotExist) -> str | None:
        """
        get attr name in original register
        """
        if obj == ValueNotExist:
            obj = cls   # seems it is not good idea!!!

        for name in dir(obj):
            if name.lower() == str(item).lower():
                return name

    @classmethod
    def _attr_anycase__get_value(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = cls._attr_anycase__get_name(item, obj)
        if name_original is None:
            raise AttributeError(item)

        return getattr(obj, name_original)


# =====================================================================================================================
