from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.base_statics.m4_enums import *


# =====================================================================================================================
@final
class DictAux(NestInit_Source):
    """
    NOTE
    ----
    decide where to work - source or copy????
    """
    SOURCE: dict[Any, Any] = dict

    # -----------------------------------------------------------------------------------------------------------------
    def clear_values(self, form: FormIntExt = FormIntExt.EXTERNAL) -> dict[Any, None]:
        keys = list(self.SOURCE)
        new_dict = dict.fromkeys(keys)
        if form == FormIntExt.EXTERNAL:
            return new_dict

        if form == FormIntExt.INTERNAL:
            self.SOURCE.clear()
            self.SOURCE.update(new_dict)
            return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def keys_del(self, *keys: Any) -> None:
        for key in keys:
            try:
                self.SOURCE.pop(key)
            except:
                pass

    def keys_rename__by_func(self, func: Callable[[Any], Any], form: FormIntExt = FormIntExt.EXTERNAL) -> dict[Any, Any]:
        """
        GOAL
        ----
        useful to rename keys by func like str.LOWER/upper
        raise on func - delete key from origin! applied like filter
        """
        result = {}
        if form == FormIntExt.EXTERNAL:
            result = {}
        elif form == FormIntExt.INTERNAL:
            result = self.SOURCE

        # -----------------------
        for key in list(self.SOURCE):
            value = self.SOURCE.get(key)
            DictAux(result).keys_del(key)
            try:
                key_new = func(key)
                result.update({key_new: value})
            except:
                pass

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def collapse_key(self, key: Any) -> dict[Any, Any]:
        """
        GOAL
        ----
        specially created for 2level-dicts (when values could be a dict)
        so it would replace values (if they are dicts and have special_key)

        CONSTRAINTS
        -----------
        it means that you have similar dicts with same exact keys
            {
                0: 0,
                1: {1:1, 2:2, 3:3},
                2: {1:11, 2:22, 3:33},
                3: {1:111, 2:222, 3:333},
                4: 4,
            }
        and want to get special slice like result

        SPECIALLY CREATED FOR
        ---------------------
        testplans get results for special dut from all results


        main idia to use values like dicts as variety and we can select now exact composition! remain other values without variants

        EXAMPLES
        --------
        dicts like
            {
                1: {1:1, 2:2, 3:3},
                2: {1:1, 2:None},
                3: {1:1},
                4: 4,
            }
        for key=2 return
            {
                1: 2,
                2: None,
                3: None,
                4: 4,
            }

        """
        result = {}
        for root_key, root_value in self.SOURCE.items():
            if isinstance(root_value, dict) and key in root_value:
                root_value = root_value.get(key)

            result[root_key] = root_value

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def prepare_serialisation(self) -> dict:
        result = {}
        # TODO: FINISH

        return result


# =====================================================================================================================
