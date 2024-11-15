from typing import *
from typing import Union, Any, Type, Callable, NoReturn


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
        def __init__(self, value: Any | type[ValueNotExist] | ValueNotExist = ValueNotExist):
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

    def __bool__(self):
        return False


# =====================================================================================================================
TYPE__VALUE_NOT_PASSED = type[ValueNotExist] | ValueNotExist

# ---------------------------------------------------------------------------------------------------------------------
# SEE SAME BUT DIFFERS: TYPE__LAMBDA_ARGS *
TYPE__VALID_ARGS = Union[tuple, Any, None, "TYPE__ARGS_EMPTY", "TYPE__EXPLICIT"]
TYPE__VALID_KWARGS = Optional[dict[str, Any]]

TYPE__VALID_EXCEPTION = Union[Exception, type[Exception]]
TYPE__VALID_callable_item = Callable[[...], Any | NoReturn]
TYPE__VALID_SOURCE = Union[
    Any,                                # as main idea! as already final generic
    Callable[[...], Any | NoReturn],    # as main idea! to get final generic
    # TYPE__VALID_EXCEPTION,              # fixme: hide? think no? we can pass in theory Exx! but why? for tests? why? we need it only in result! if need in tests Place it as Any!
    TYPE__VALUE_NOT_PASSED
]
TYPE__VALID_RESULT = Union[
    Any,
    TYPE__VALID_EXCEPTION,  # as main idea! instead of raise
]
# BOOL --------------------------------
TYPE__VALID_SOURCE_BOOL = Union[
    Any,                                # fixme: hide? does it need? for results like []/{}/()/0/"" think KEEP! it mean you must know that its expecting boolComparing in further logic!
    bool,                               # as main idea! as already final generic
    Callable[[...], bool | Any | NoReturn],   # as main idea! to get final generic
    # TYPE__VALID_EXCEPTION,
    TYPE__VALUE_NOT_PASSED
]
TYPE__VALID_RESULT_BOOL = Union[
    # this is when you need get only bool! raise - as False!
    bool,  # as main idea! instead of raise/exx
]
# FIXME: TODO: solve idea of BOOL!!! cant understand about Exx in here!
TYPE__VALID_RESULT_BOOL__EXX = Union[
    bool,
    TYPE__VALID_EXCEPTION,
]

# ---------------------------------------------------------------------------------------------------------------------
TYPE__VALID_VALIDATOR = Union[
    Any,    # generic final instance as expecting value - direct comparison OR comparison instance like Valid!
    # Type,   # Class as validator like Valid? fixme
    TYPE__VALID_EXCEPTION,  # direct comparison
    Callable[[Any, ...], bool | NoReturn]     # func with first param for validating source
]


# =====================================================================================================================
TYPES_ELEMENTARY_SINGLE: tuple[type, ...] = (
    type(None), bool,
    str, bytes,
    int, float,
)
TYPES_ELEMENTARY_COLLECTION: tuple[type, ...] = (
    tuple, list,
    set, dict,
)
TYPES_ELEMENTARY: tuple[type, ...] = (*TYPES_ELEMENTARY_SINGLE, *TYPES_ELEMENTARY_COLLECTION, )
TYPE__ELEMENTARY = Union[*TYPES_ELEMENTARY]


# =====================================================================================================================
