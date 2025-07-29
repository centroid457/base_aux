from typing import *

from base_aux.aux_iter.m1_iter_aux import IterAux
from base_aux.base_values.m2_value_special import *
from base_aux.base_lambdas.m1_lambda import *


# =====================================================================================================================
class DictIcKeys(dict):
    """
    GOAL
    ----
    just a Caseinsense dict
    """
    # __getattr__ = dict.get
    # __setattr__ = dict.__setitem__
    # __delattr__ = dict.__delitem__
    # __iter__ = dict.__iter__
    # __copy__ = dict.copy

    # __repr__ = dict.__repr__  # и так работает!
    # __str__ = dict.__str__    # и так работает!
    # __len__ = dict.__len__    # и так работает!

    # -----------------------------------------------------------------------------------------------------------------
    # GENERIC CLASSES LIKE DICT MUST APPLIED LAST IN MRO!!!
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     _LOCK_KEYS = self.__LOCK_KEYS
    #     super().__init__(*args, **kwargs)
    #     self.__LOCK_KEYS = _LOCK_KEYS

    # -----------------------------------------------------------------------------------------------------------------
    def key__get_original(self, key: str | Any) -> str | NoValue | Any:
        keys_list = list(self)
        result = IterAux(keys_list).item__get_original(key)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def get(self, item: str | Any) -> Any | None:    # | NoReturn:
        """
        always get value or None!
        if you need check real contain key - check contain)))) [assert key in self] or [getitem_original]
        """
        key_original = self.key__get_original(item)
        if key_original is NoValue:
            return None
            # key_original = item
            # msg = f"{item=}"
            # raise KeyError(msg)

        return super().get(key_original)

    # def set(self, item: Any, value: Any) -> None:

    def pop(self, item: str | Any) -> Any:
        item_original = self.key__get_original(item)
        if item_original is NoValue:
            item_original = item

        return super().pop(item_original)

    def update(self, *args, **kwargs) -> None | NoReturn:
        if args:
            params = args[0]
        else:
            params = kwargs
        for item, value in params.items():
            key_original = self.key__get_original(item)
            if key_original is NoValue:
                key_original = item

            super().update({key_original: value})

    def __contains__(self, item: Any) -> bool:
        return self.key__get_original(item) is not NoValue

    # -----------------------------------------------------------------------------------------------------------------
    # ITEM is universal!
    def __getitem__(self, item: Any) -> Any | NoReturn:
        # if item not in self:        # decide use original behaviour or Raise!?
        #     msg = f"{item=}"
        #     raise KeyError(msg)
        return self.get(item)

    def __setitem__(self, item: Any, value: Any) -> None:
        self.update({item: value})

    def __delitem__(self, item: Any) -> None:
        self.pop(item)

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: dict | Any) -> bool:
        if not isinstance(other, dict):
            return False

        if len(self) != len(other):
            return False

        for key, value in other.items():
            if key not in self or self[key] != value:
                return False

        return True


# =====================================================================================================================
# @final
class DictIc_LockedKeys(DictIcKeys):
    """
    GOAL
    ----
    create INLINE/OnTheFly (ByOneLine) keys set on init object!
    so you dont need create one more/extra object!
    like in
        class MyLockedKeys:
            ATTR1: str = "ATTR1"
            ATTR2: int = 2
            def update(**kwargs):
                pass

        class Final:
            PARAMS = MyLockedKeys()
            def __init__(**kwargs):
                self.PARAMS.update(**kwargs)

    use instead
        class Final:
            PARAMS = DictIc_LockedKeys(ATTR1="ATTR1, ATTR2=2)
            def __init__(**kwargs):
                self.PARAMS.update(**kwargs)

    make dict similar to named tuple
    when you setup keys only on init!

    SPECIALLY CREATED FOR
    ---------------------
    indics and other PARAMS useful objects
    """
    def __setitem__(self, item: Any, value: Any) -> None:
        if item not in self:
            msg = f"[{self.__class__.__name__}]{item=}/{value=}"
            raise Exx__WrongUsage(msg)

        self.update({item: value})

    def update(self, *args, **kwargs) -> None | NoReturn:
        if args:
            params = args[0]
        else:
            params = kwargs
        for item, value in params.items():
            key_original = self.key__get_original(item)
            if key_original is NoValue:
                msg = f"[{self.__class__.__name__}]{item=}/{value=}"
                raise Exx__WrongUsage(msg)

            super().update({key_original: value})


# =====================================================================================================================
# class _DictIcKeys(dict):
#     """
#     DEEP_SEEk +some ref - is not
#     """
#     def __init__(self, arg, **kwargs):
#         super().__init__(arg, **kwargs)
#         self._convert_keys()
#
#     def __setitem__(self, key: Any, value):
#         super().__setitem__(key.lower() if isinstance(key, str) else key, value)
#
#     def __getitem__(self, key: Any):
#         return super().__getitem__(key.lower() if isinstance(key, str) else key)
#
#     def __contains__(self, key: Any):
#         return super().__contains__(key.lower() if isinstance(key, str) else key)
#
#     def get(self, key: Any, default=None):
#         return super().get(key.lower() if isinstance(key, str) else key, default)
#
#     def pop(self, key: Any, default=None):
#         return super().pop(key.lower() if isinstance(key, str) else key, default)
#
#     def update(self, other=None, **kwargs):
#         if other is not None:
#             if hasattr(other, 'items'):
#                 for key, value in other.items():
#                     self[key] = value
#             else:
#                 for key, value in other:
#                     self[key] = value
#         for key, value in kwargs.items():
#             self[key] = value
#
#     def _convert_keys(self):
#         for key in list(self.keys()):
#             if isinstance(key, str):
#                 value = super().pop(key)
#                 self[key] = value


# =====================================================================================================================
