from typing import *
from base_aux.funcs.static import ValueNotExist


# =====================================================================================================================
class Translator:
    RETURN_SOURCE_IF_NOT_FOUND: bool = True

    VALIDATOR: Callable[[Any, Any], bool] = lambda self, source, var: source == var
    RULES: dict[Any, Any]

    def __init__(self, rules, validator=None, return_source_if_not_found: bool = None):
        if validator is not None:
            self.VALIDATOR = validator
        if rules is not None:
            self.RULES = rules
        if return_source_if_not_found is not None:
            self.RETURN_SOURCE_IF_NOT_FOUND = return_source_if_not_found

    def __call__(self, source: Any, *args, **kwargs) -> Any | type[ValueNotExist]:
        for variant, result in self.RULES.items():
            if self.VALIDATOR(source, variant):
                return result

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
