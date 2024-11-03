from typing import *
from base_aux.funcs import ValueNotExist


# =====================================================================================================================
class AttrAux:
    """
    NOTICE
    ------
    if there are several same attrs in different cases - you should resolve it by yourself!
    """
    # NAME ------------------------------------------------------------------------------------------------------------
    @classmethod
    def _attr_anycase__find(cls, item: str | Any, obj: Any = ValueNotExist) -> str | None:
        """
        get attr name in original register
        """
        if not isinstance(item, str):
            return

        item = item.strip()
        if obj == ValueNotExist:
            obj = cls   # seems it is not good idea!!!

        for name in dir(obj):
            if name.lower() == str(item).lower():
                return name

        return

    # GET -------------------------------------------------------------------------------------------------------------
    @classmethod
    def _getattr_anycase(cls, item: str, obj: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!
        """
        name_original = cls._attr_anycase__find(item, obj)
        if name_original is None:
            raise AttributeError(item)

        return getattr(obj, name_original)

    # SET -------------------------------------------------------------------------------------------------------------
    @classmethod
    def _setattr_anycase(cls, item: str, value:Any, obj: Any) -> Any | Callable | NoReturn:
        """
        get attr value by name in any register
        no execution! return pure value as represented in object!

        NoReturn - in case of not accepted names when setattr
        """
        name_original = cls._attr_anycase__find(item, obj)
        if name_original is None:
            if not isinstance(item, str):
                raise AttributeError(item)

            item = item.strip()
            if item in ["", ]:
                raise AttributeError(item)
            name_original = item

        # NOTE: you still have no exx with setattr(obj, "    HELLO", value) and ""
        return setattr(obj, name_original, value)


# =====================================================================================================================
