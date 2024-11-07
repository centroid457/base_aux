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

# ---------------------------------------------------------------------------------------------------------------------
# SEE SAME BUT DIFFERS: TYPE__LAMBDA_ARGS *
TYPE__VALID_ARGS = Union[tuple, Any, None, "TYPE__ARGS_EMPTY", "TYPE__EXPLICIT"]
TYPE__VALID_KWARGS = Optional[dict[str, Any]]

TYPE__VALID_EXCEPTION = Union[Exception, Type[Exception]]
TYPE__VALID_SOURCE = Union[
    Callable[[...], Any | NoReturn],    # as main idea! to get final generic
    Any,                                # as main idea! as already final generic
    TYPE__VALID_EXCEPTION,              # fixme: hide? think no!
    TYPE__VALUE_NOT_PASSED
]

TYPE__VALID_RESULT = Union[
    TYPE__VALID_EXCEPTION,  # as main idea! instead of raise
    Any,
]


# =====================================================================================================================
