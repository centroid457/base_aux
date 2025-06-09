from typing import *
from base_aux.aux_iter.m1_iter_aux import IterAux
from base_aux.aux_values.m1_value_special import *


# =====================================================================================================================
class DictIcKeys(dict):
    """
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
    def pop(self, item: Any) -> None:
        item_original = IterAux(self).item__get_original(item)
        if item_original is NoValue:
            item_original = item

        super().pop(item_original)

    def get(self, item: Any) -> Any:    # | NoReturn:
        """
        always get value or None!
        if you need check real contain key - check contain)))) [assert key in self] or [getitem_original]
        """
        key_original = IterAux(self).item__get_original(item)
        if key_original is NoValue:
            return None
            # key_original = item
            # msg = f"{item=}"
            # raise KeyError(msg)

        return super().get(key_original)

    # def set(self, item: Any, value: Any) -> None:

    def update(self, m, /, **kwargs) -> None:
        for item, value in m.items():
            key_original = IterAux(self).item__get_original(item)
            if key_original is NoValue:
                key_original = item

            super().update({key_original: value})

    def __contains__(self, item: Any) -> bool:
        if IterAux(self).item__get_original(item) is not NoValue:
            return True

    # -----------------------------------------------------------------------------------------------------------------
    # ITEM is universal!
    def __getitem__(self, item: Any) -> Any | NoReturn:
        return self.get(item)

    def __setitem__(self, item: Any, value: Any) -> None | NoReturn:
        self.update({item: value})

    def __delitem__(self, item: Any) -> None:
        self.pop(item)


# =====================================================================================================================
