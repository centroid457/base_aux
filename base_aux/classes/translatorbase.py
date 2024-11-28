from typing import *
from base_aux.funcs.static import ValueNotExist


# =====================================================================================================================
class TranslatorBase:
    """
    SPECIALLY CREATED FOR
    ---------------------
    as base to translate breeder_stack into russian
    """
    SELECTOR_ATTR: str = None
    RETURN_SOURCE_IF_NOT_FOUND: bool = True

    SELECTOR: Callable[[Any, Any], bool] = lambda self, source, var: source == var
    RULES: dict[Any, Any]

    def __init__(self, rules, selector=None, return_source_if_not_found: bool = None, selector_attr: str = None):
        if selector is not None:
            self.SELECTOR = selector
        if rules is not None:
            self.RULES = rules
        if return_source_if_not_found is not None:
            self.RETURN_SOURCE_IF_NOT_FOUND = return_source_if_not_found
        if selector_attr is not None:
            self.SELECTOR_ATTR = selector_attr

    def __call__(self, source: Any, *args, **kwargs) -> Any | type[ValueNotExist]:
        """
        any raise - assumed as not valid
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
class TranslatorDirect(TranslatorBase):
    """
    just a clear derivative
    """
    pass


class TranslatorByAttr(TranslatorBase):
    """
    SPECIALLY CREATED FOR
    ---------------------
    exact translate breeder_stack into russian
    """

    SELECTOR = lambda self, source, var: getattr(source, self.SELECTOR_ATTR) == var


# =====================================================================================================================
if __name__ == "__main__":
    victim = TranslatorBase({1:11, 2:22})
    assert victim(1) == 11
    assert victim(2) == 22
    assert victim(3) == 3

    victim = TranslatorBase({1:11, 2:22}, return_source_if_not_found=False)
    assert victim(3) == ValueNotExist
    # run_over_api()


# =====================================================================================================================
