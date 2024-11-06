from typing import *


# =====================================================================================================================
TYPE__LAMBDA_CONSTRUCTOR = Type[Any] | Callable[..., Any | NoReturn]
TYPE__LAMBDA_ARGS = tuple[Any, ...]
TYPE__LAMBDA_KWARGS = dict[Any, Any]


class Lambda:
    """
    GOAL
    ----
    1. delay probable raising Exx on direct execution (use with AttrLambdaCall)
    like creating objects on Cls attributes
        class Cls:
            ATTR = PrivateValues(123)   # Lambda(PrivateValues, 123)

    2. (not serious) replace simple lambda!
    by using lambda you should define args/kwargs any time! and im sick of it!
        func = lambda *args, **kwargs: sum(*args) + sum(**kwargs.values())  # its not a simple lambda!
        func = lambda *args: sum(*args)  # its simple lambda
        result = func(1, 2)
    replace to
        func = Lambda(sum)
        result = func(1, 2)

        func = Lambda(sum, 1, 2)
        result = func()
    its те a good idea to replace lambda fully!
    cause you cant replace following examples
        func_link = lambda source: str(self.Victim(source))
        func_link = lambda source1, source2: self.Victim(source1) == source2


    SPECIALLY CREATED FOR
    ---------------------
    Item for using with AttrLambdaCall

    WHY NOT 1=simple LAMBDA?
    ------------------------
    extremely good point!
    but
    1. in case of at least AttrLambdaCall you cant distinguish method or callable attribute!
    so you explicitly define attributes/objects for later constructions
    and in some point it can be more clear REPLACE LAMBDA by this solvation!!!

    2.

    PARAMS
    ======
    :ivar CONSTRUCTOR: any class or function
    """
    CONSTRUCTOR: TYPE__LAMBDA_CONSTRUCTOR
    ARGS: TYPE__LAMBDA_ARGS = ()
    KWARGS: TYPE__LAMBDA_KWARGS = {}

    def __init__(self, constructor: TYPE__LAMBDA_CONSTRUCTOR, *args, **kwargs) -> None:
        self.CONSTRUCTOR = constructor
        self.ARGS = args
        self.KWARGS = kwargs

    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        return self.CONSTRUCTOR(*args, **kwargs)

    def check_raise(self, *args, **kwargs) -> bool:
        """
        SPECIALLY CREATED FOR
        ---------------------
        check Privates in pytest for skipping
        """
        return not self.check_no_raise(*args, **kwargs)

    def check_no_raise(self, *args, **kwargs) -> bool:
        try:
            self(*args, **kwargs)
            return True
        except Exception as exx:
            return False

    def get_result_or_exx(self, *args, **kwargs) -> bool | Exception:
        """
        SPECIALLY CREATED FOR
        ---------------------
        just in case
        """
        try:
            return self(*args, **kwargs)
        except Exception as exx:
            return exx


# =====================================================================================================================
class AttrLambdaCall:
    """
    find and call all Lambda attrs On class inition
    GOAL
    ----
    if you need create object in classAttribute only on real inition of class
    useful in case of raising exx on init, but you want to pass instance in class attribute with inplace initiation

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
            if isinstance(value, Lambda):
                setattr(self, attr, value())

        super().__init__(*args, **kwargs)


# =====================================================================================================================
