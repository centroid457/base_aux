from typing import *
from .m0_novalue import NoValue


# =====================================================================================================================
TYPE__LAMBDA_CONSTRUCTOR = Union[Any, type[Any], Callable[..., Any | NoReturn]]

TYPE__ARGS_FINAL = tuple[Any, ...]
TYPE__KWARGS_FINAL = dict[str, Any]


# =====================================================================================================================
class ArgsKwargs:       # fixme: decide to separate+FINAL!!! so used only for direct KwArgs
    """
    NOTE
    ----
    1/ DONT NEST! (expect Args/Kwargs)
    2/ DONT USE!

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
        (ArgsKwargs("get name"), "ATC"),
        (ArgsKwargs("test gnd", _timeout=5), "PASS"),
    ]:
        assert serialDevice.send(*item.ARGS, **item.KWARGS) == expect

    WHY NOT - 1=add direct __iter for args and smth like __dict for kwargs
    ----------------------------------------------------------------------
    and use then (*victim, **victim)
    NO - there are no __dict like dander method!
    but we can use ArgsKwargs(dict)!? - yes but it add all other methods!
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
    ARGS: TYPE__ARGS_FINAL = ()
    KWARGS: TYPE__KWARGS_FINAL = {}

    def __init__(self, *args, **kwargs) -> None:
        self.ARGS = args
        self.KWARGS = kwargs

    def __bool__(self) -> bool:
        if self.ARGS or self.KWARGS:
            return True
        else:
            return False


# ---------------------------------------------------------------------------------------------------------------------
@final
class Args(ArgsKwargs):
    """
    just a derivative to clearly show only Args is important
    """
    def __bool__(self) -> bool:
        if self.ARGS:
            return True
        else:
            return False

    def __iter__(self):
        yield from self.ARGS

    def __call__(self):
        return self.ARGS


@final
class Kwargs(ArgsKwargs):
    """
    just a derivative to clearly show only KwArgs is important
    """
    def __bool__(self) -> bool:
        if self.KWARGS:
            return True
        else:
            return False

    def __iter__(self):
        yield from self.KWARGS

    def __call__(self):
        return self.KWARGS


# =====================================================================================================================
TYPE__ARGS_DRAFT = Union[Any, TYPE__ARGS_FINAL, ArgsKwargs]           # you can use direct single value
TYPE__KWARGS_DRAFT = Union[None, TYPE__KWARGS_FINAL, ArgsKwargs]  # if passed NONE - no data!


# =====================================================================================================================
