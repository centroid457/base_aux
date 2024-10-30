from typing import *


# =====================================================================================================================
class ValueNotExist:
    """
    DEPRECATE???
    ---------
    use direct ArgsEmpty???

    GOAL
    ----
    it is different from Default!
    there is no value!
    used when we need to change logic with not passed value!

    SPECIALLY CREATED FOR
    ---------------------
    Valid as universal validation object under cmp other objects!

    USAGE
    -----
    class Cls:
        def __init__(self, value: Any | Type[ValueNotExist] | ValueNotExist = ValueNotExist):
            self.value = value

        def __eq__(self, other):
            if self.value is ValueNotExist:
                return other is True
                # or
                return self.__class__(other).run()
            else:
                return other == self.value

        def run(self):
            return bool(self.value)

    SAME AS
    -------
    args.ArgsEmpty but single and really not defined
    """
    pass


# =====================================================================================================================
TYPE__VALUE_NOT_PASSED = Type[ValueNotExist] | ValueNotExist

TYPE__ARGS = Union[tuple, Any, None, "TYPE__ARGS_EMPTY", "TYPE__EXPLICIT"]
TYPE__KWARGS = Optional[dict[str, Any]]

TYPE__EXCEPTION = Union[Exception, Type[Exception]]
TYPE__SOURCE_LINK = Union[Any, TYPE__EXCEPTION, Callable[[...], Any | NoReturn], TYPE__VALUE_NOT_PASSED]


# =====================================================================================================================
