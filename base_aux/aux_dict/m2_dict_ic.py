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

    def update(self, m, /, **kwargs) -> None:
        for item, value in m.items():
            key_original = self.key__get_original(item)
            if key_original is NoValue:
                key_original = item

            super().update({key_original: value})

    def __contains__(self, item: Any) -> bool:
        return self.key__get_original(item) is not NoValue

    # -----------------------------------------------------------------------------------------------------------------
    # ITEM is universal!
    def __getitem__(self, item: Any) -> Any | NoReturn:
        if item not in self:
            msg = f"{item=}"
            raise KeyError(msg)
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
