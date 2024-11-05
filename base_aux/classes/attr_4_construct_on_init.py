from typing import *
from base_aux.funcs import ValueNotExist


# =====================================================================================================================
class ConstructOnInit_Item:
    """
    Item for using with ConstructOnInit
    """
    CLS: Type[Any]
    ARGS: tuple[Any, ...] = ()
    KWARGS: dict[Any, Any] = {}

    def __init__(self, cls: Type[Any], *args, **kwargs) -> None:
        self.CLS = cls
        self.ARGS = args
        self.KWARGS = kwargs

    def __call__(self) -> Any | NoReturn:
        return self.CLS(*self.ARGS, **self.KWARGS)


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
            if isinstance(value, ConstructOnInit_Item):
                setattr(self, attr, value())

        super().__init__(*args, **kwargs)


# =====================================================================================================================
