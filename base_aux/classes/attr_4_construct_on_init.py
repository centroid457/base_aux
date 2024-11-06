from typing import *


# =====================================================================================================================
TYPE__CONSTRUCTOR = Type[Any] | Callable[..., Any | NoReturn]
TYPE__CONSTRUCTOR_ARGS = tuple[Any, ...]
TYPE__CONSTRUCTOR_KWARGS = dict[Any, Any]


class CallLater:
    """
    GOAL
    ----
    delay probable raising Exx on direct execution
    like creating objects on Cls attributes

    SPECIALLY CREATED FOR
    ---------------------
    Item for using with ConstructOnInit

    WHY NOT 1=simple LAMBDA?
    ------------------------
    extremely good point!
    but in case of at least ConstructOnInit you cant distinguish method or callable attribute!
    so you explicitly define attributes/objects for later constructions

    PARAMS
    ======
    :ivar CONSTRUCTOR: any class or function
    """
    CONSTRUCTOR: TYPE__CONSTRUCTOR
    ARGS: TYPE__CONSTRUCTOR_ARGS = ()
    KWARGS: TYPE__CONSTRUCTOR_KWARGS = {}

    def __init__(self, constructor: TYPE__CONSTRUCTOR, *args, **kwargs) -> None:
        self.CONSTRUCTOR = constructor
        self.ARGS = args
        self.KWARGS = kwargs

    def __call__(self) -> Any | NoReturn:
        return self.CONSTRUCTOR(*self.ARGS, **self.KWARGS)


# =====================================================================================================================
class ConstructOnInit:
    """
    GOAL
    ----
    if you need create object in classAttribute only on real inition of class
    useful in case of raise exx on init, but you want to pass instance in class attribute with inplace initiation

    REASON EXAMPLE
    --------------
    all class attributes will be calculated on import!
    class Cls:
        OK: int = int("1")
        # FAIL_ON_IMPORT: int = int("hello")    # ValueError: invalid literal for int() with base 10: 'hello'
        FAIL_ON_INIT: int = None

        def __init__(self, *args, **kwargs):
            if self.FAIL_ON_INIT is None:
                self.FAIL_ON_INIT = int("hello")    # this wount raise on import!

    Cls()   # ValueError: invalid literal for int() with base 10: 'hello'
    """

    def __init__(self, *args, **kwargs) -> None | NoReturn:
        for attr in dir(self):
            value = getattr(self, attr)
            if isinstance(value, CallLater):
                setattr(self, attr, value())

        super().__init__(*args, **kwargs)


# =====================================================================================================================
