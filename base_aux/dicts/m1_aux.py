from typing import *

from base_aux.base_source import InitSource
from base_aux.lambdas import Lambda


# =====================================================================================================================
class DictAux(InitSource):  # use name *s to not mess with typing.Dict
    """
    NOTE
    ----
    decide where to work - source or copy????
    """

    SOURCE: dict[Any, Any] = Lambda(dict)

    # -----------------------------------------------------------------------------------------------------------------
    def clear_values(self) -> dict[Any, None]:
        return dict.fromkeys(self.SOURCE)

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
