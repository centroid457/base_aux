from base_aux.aux_eq.m3_eq_other2_validators import *
from base_aux.aux_eq.m4_eq_valid1_base import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_enums.m2_enum1_adj import *
from base_aux.base_nest_dunders.m3_calls import *


# ======================================================================================================================
class ModifierTry(NestCall_Resolve):
    """
    GOAL
    collect modifiers in separated object
    """
    modifiers_try: TYPING.MODIFIERS_TRY__FINAL
    _modifier_direct_results: list[Any | Exception]    # for debugging!

    def __init__(self, *args):
        self._modifier_direct_results = []

        self.modifiers_try = []
        for item in args:
            if not callable(item):
                msg = f"Incorrect type usage {item=}/{args=}"
                raise Exception(msg)
            self.modifiers_try.append(item)

    def resolve(self, source: Any, *args, **kwargs) -> Any:
        """
        RULE
        try all items!
        pass any value further in chain if no Exception

        if exception accuses - modifier ignored!
        """
        result = source
        for item in self.modifiers_try:
            try:
                result = item(result, *args, **kwargs)
                self._modifier_direct_results.append(result)
            except Exception as exc:
                self._modifier_direct_results.append(exc)
        return result


# ======================================================================================================================
