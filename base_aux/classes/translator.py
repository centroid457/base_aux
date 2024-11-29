from typing import *
from base_aux.funcs.static import ValueNotExist
from base_aux.classes import *


# =====================================================================================================================
class Translator:
    """
    SPECIALLY CREATED FOR
    ---------------------
     translate breeder_stack values into russian
    """
    RETURN_SOURCE_IF_NOT_FOUND: bool = True

    SELECTOR: Callable[[Any, Any], bool] = lambda self, source, var: source == var
    RULES: dict[Any | str, Any]

    def __init__(self, rules: dict[Any, Any] | Any, selector=None, return_source_if_not_found: bool = None):
        if selector is not None:
            self.SELECTOR = selector
        if rules is not None:
            self.RULES = rules
        if return_source_if_not_found is not None:
            self.RETURN_SOURCE_IF_NOT_FOUND = return_source_if_not_found

        if not isinstance(self.RULES, dict):
            self.RULES = AttrAux.attrs__to_dict(self.RULES)

    def __call__(self, source: Any, *args, **kwargs) -> Any | type[ValueNotExist]:
        """
        GOAL
        ----
        actually make translation

        any raise - assumed as not valid/selected
        """
        for variant, result in self.RULES.items():
            try:
                if self.SELECTOR(source, variant):
                    return result
            except:
                pass

        if self.RETURN_SOURCE_IF_NOT_FOUND:
            return source
        else:
            return ValueNotExist


# =====================================================================================================================
if __name__ == "__main__":
    victim = Translator({1:11, 2:22})
    assert victim(1) == 11
    assert victim(2) == 22
    assert victim(3) == 3

    victim = Translator({1:11, 2:22}, return_source_if_not_found=False)
    assert victim(3) == ValueNotExist
    # run_over_api()


# =====================================================================================================================