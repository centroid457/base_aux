from typing import *
from .novalue import NoValue


# =====================================================================================================================
TYPE__LAMBDA_CONSTRUCTOR = Union[Any, type[Any], Callable[..., Any | NoReturn]]
TYPE__LAMBDA_ARGS = tuple[Any, ...]
TYPE__LAMBDA_KWARGS = dict[str, Any]


# =====================================================================================================================
class InitArgsKwargs:
    """
    GOAL
    ----
    idea to keep args and kwargs in appropriate form/one object without application (constructor or func).
    so we can uncovering in later.
    usage in test parametrisation.

    SPECIALLY CREATED FOR
    ---------------------
    ATC tests with using special param prefix="*"

    BEST PRACTICE
    -------------
    for item, expect in [
        (InitArgsKwargs("get name"), "ATC"),
        (InitArgsKwargs("test gnd", _timeout=5), "PASS"),
    ]:
        assert serialDevice.send(*item.ARGS, **item.KWARGS) == expect

    WHY NOT - 1=add direct __iter for args and smth like __dict for kwargs
    ----------------------------------------------------------------------
    and use then (*victim, **victim)
    NO - there are no __dict like dander method!
    but we can use InitArgsKwargs(dict)!? - yes but it add all other methods!
        class Cls(dict):
            ARGS: tuple[Any, ...]
            KWARGS: dict[str, Any]

            def __init__(self, *args, **kwargs) -> None:
                super().__init__(**kwargs)
                self.ARGS = args
                self.KWARGS = kwargs

            def __iter__(self) -> Iterator[Any]:
                yield from self.ARGS

    so as result the best decision is (*item.ARGS, **item.KWARGS)
    and we could use this class as simple base for Lambda for example!
    """
    ARGS: TYPE__LAMBDA_ARGS = ()
    KWARGS: TYPE__LAMBDA_KWARGS = {}

    def __init__(self, *args, **kwargs) -> None:
        self.ARGS = args
        self.KWARGS = kwargs

    def __bool__(self) -> bool:
        if self.ARGS or self.KWARGS:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
class Args(InitArgsKwargs):
    """
    just a derivative to clearly show only Args is important
    """
    def __bool__(self) -> bool:
        if self.ARGS:
            return True
        else:
            return False

    # def __iter__(self):
    #     yield from self.ARGS
    # NOTE: dont use any danders! its too complicated! be simple and get access to self.ARGS!


class Kwargs(InitArgsKwargs):
    """
    just a derivative to clearly show only KwArgs is important
    """
    # TODO: decide apply dict nesting or not! by now it seems more clear
    def __bool__(self) -> bool:
        if self.KWARGS:
            return True
        else:
            return False

    # def __iter__(self):
    #     yield from self.KWARGS


# =====================================================================================================================
# SEE SAME BUT DIFFERS: TYPE__LAMBDA_ARGS *
TYPE__VALID_ARGS = Union[NoValue, Any, tuple, "TYPE__EXPLICIT", InitArgsKwargs, Args]   # dont use None! use clear Args()/NoValue
TYPE__VALID_KWARGS = Union[NoValue, dict[str, Any], InitArgsKwargs, Kwargs]             # dont use None! use clear Kwargs()/NoValue


# =====================================================================================================================
