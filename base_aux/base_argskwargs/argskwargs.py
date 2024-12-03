from typing import Any, Callable, NoReturn, Union
from .novalue import NoValue


# =====================================================================================================================
TYPE__LAMBDA_CONSTRUCTOR = Any | type[Any] | Callable[..., Any | NoReturn]
TYPE__LAMBDA_ARGS = tuple[Any, ...]
TYPE__LAMBDA_KWARGS = dict[str, Any]


# =====================================================================================================================
class ArgsKwargs:
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
class Args(ArgsKwargs):
    """
    just a derivative to clearly show only Args is important
    """
    def __bool__(self) -> bool:
        if self.ARGS:
            return True
        else:
            return False


class Kwargs(ArgsKwargs):
    """
    just a derivative to clearly show only KwArgs is important
    """
    def __bool__(self) -> bool:
        if self.KWARGS:
            return True
        else:
            return False


# =====================================================================================================================
# class _ArgsEmpty(Default):
#     """
#     # FIXME: DEPRECATED!!! dont use it!! and del later
#     THIS IS JUST A PARTIAL CASE FOR ARGS Default
#
#     DEPRECATE ???
#     ---------
#     USE DIRECTLY THE CONSTANT VALUE ()!!!
#     its clear and
#
#     GOAL
#     ----
#     explicit pass
#     resolve not passed parameters in case of None VALUE!
#
#     special object used as VALUE to show that parameter was not passed!
#     dont pass it directly! keep it only as default parameter in class and in methods instead of None Value!
#     it used only in special cases! not always even in one method!!!
#
#     SAME AS
#     -------
#     value_explicit.NoValue but just blank collection
#     """
#     def __init__(self):
#         super().__init__(source=())
#
#     # # NOTE: this is not nesessory!!! and even need not to use for sure!
#     # @classmethod
#     # def __str__(cls):
#     #     return "()"
#     #
#     # @classmethod
#     # def __repr__(cls):
#     #     return str(cls)
#     #
#     # @classmethod
#     # def __len__(cls):
#     #     return 0
#     #
#     # @classmethod
#     # def __bool__(cls):
#     #     return False
#     #
#     # @classmethod
#     # def __iter__(cls):
#     #     yield from ()
#

# =====================================================================================================================
# SEE SAME BUT DIFFERS: TYPE__LAMBDA_ARGS *
TYPE__VALID_ARGS = Union[NoValue, Any, tuple, "TYPE__EXPLICIT", ArgsKwargs, Args]   # dont use None! use clear Args()/NoValue
TYPE__VALID_KWARGS = Union[NoValue, dict[str, Any], ArgsKwargs, Kwargs]             # dont use None! use clear Kwargs()/NoValue


# =====================================================================================================================
