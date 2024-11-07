from typing import *

from base_aux.classes.static import TYPE__LAMBDA_CONSTRUCTOR, TYPE__LAMBDA_ARGS, TYPE__LAMBDA_KWARGS
from base_aux.classes.valid_0_aux import ValidAux


# =====================================================================================================================
class Lambda:
    """
    # FIXME: it seems ValidAux have same functions!!! need to combine in one object???
        in this case its perfect separating args without special Ensure_tuple! NO!!!

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

    # OVERWRITE! ------------------------------------------------------------------------------------------------------
    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        return self.CONSTRUCTOR(*args, **kwargs)

    def __eq__(self, other) -> bool | NoReturn:
        return ValidAux.compare_doublesided__bool(other, self())

    # UNIVERSAL =======================================================================================================
    def __init__(self, constructor: TYPE__LAMBDA_CONSTRUCTOR, *args, **kwargs) -> None:
        self.CONSTRUCTOR = constructor
        self.ARGS = args
        self.KWARGS = kwargs

    # -----------------------------------------------------------------------------------------------------------------
    def __bool__(self) -> bool | NoReturn:
        return bool(self(*self.ARGS, **self.KWARGS))

    # -----------------------------------------------------------------------------------------------------------------
    def get_result_or_raise(self, *args, **kwargs) -> bool | NoReturn:
        """
        just a direct result
        """
        return self(*args, **kwargs)

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

    # -----------------------------------------------------------------------------------------------------------------
    def check_raise(self, *args, **kwargs) -> bool:
        """
        SPECIALLY CREATED FOR
        ---------------------
        check Privates in pytest for skipping

        USE LambdaTrySuccess instead!
        """
        try:
            self(*args, **kwargs)
            return False
        except Exception as exx:
            return True

    def check_no_raise(self, *args, **kwargs) -> bool:
        return not self.check_raise(*args, **kwargs)


# =====================================================================================================================
class LambdaBool(Lambda):
    """
    GOAL
    ----
    same as Lambda, in case of get result in bool variant
    +add reverse

    SPECIALLY CREATED FOR
    ---------------------
    classes.Valid.skip_link with Reverse variant

    why Reversing is so important?
    --------------------------------
    because you cant keep callable link and reversing it by simply NOT
        skip_link__direct = bool        # correct
        skip_link__direct = LambdaBool(bool)  # correct
        skip_link__reversal = not bool  # incorrect
        skip_link__reversal = LambdaBool(bool, attr).get_reverse  # correct

    but here we can use lambda
        skip_link__reversal = lambda attr: not bool(attr)  # correct but not so convenient ???

    PARAMS
    ======
    :ivar BOOL_REVERSE: just for LambdaBoolReversed, no need to init
    """

    BOOL_REVERSE: bool = False

    def __call__(self, *args, **kwargs) -> bool | NoReturn:
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        result = bool(self.CONSTRUCTOR(*args, **kwargs))
        if self.BOOL_REVERSE:
            result = not result
        return result

    def get_reverse(self, *args, **kwargs) -> bool | NoReturn:
        """
        if raise - raise

        try not to use in LambdaBoolReversed
        """
        return not self(*args, **kwargs)

    def get_bool_only(self, *args, **kwargs) -> bool:
        """
        if raise - return False, else get result
        """
        try:
            return self(*args, **kwargs)
        except Exception as exx:
            return False

    def get_bool_only__reverse(self, *args, **kwargs) -> bool:
        return not self.get_bool_only(*args, **kwargs)


# -----------------------------------------------------------------------------------------------------------------
class LambdaBoolReversed(LambdaBool):
    """
    just a reversed LambdaBool
    """
    BOOL_REVERSE: bool = True


# =====================================================================================================================
class LambdaTrySuccess(LambdaBool):
    """
    just an ability to check if object is not raised on call

    best practice
    -------------
    if LambdaTrySuccess(func):
        return func()

    @pytest.mark.skipif(LambdaTryFail(func), ...)
    """
    def __call__(self, *args, **kwargs) -> bool:
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        try:
            self.CONSTRUCTOR(*args, **kwargs)
            return not self.BOOL_REVERSE
        except:
            return bool(self.BOOL_REVERSE)


class LambdaTryFail(LambdaTrySuccess):
    BOOL_REVERSE: bool = True


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
