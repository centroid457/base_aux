from typing import *
import time

from base_aux.classes.static import TYPE__LAMBDA_CONSTRUCTOR, TYPE__LAMBDA_ARGS, TYPE__LAMBDA_KWARGS
from base_aux.enums.enums import When2
from base_aux.valid.valid_0_aux import ValidAux
from base_aux.objects import TypeChecker


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


# =====================================================================================================================
class Lambda(ArgsKwargs):
    """
    # FIXME: it seems ValidAux have same functions!!! need to combine in one object??? - NO!!!
        in this case its perfect separating args without special Ensure_tuple!

    IDEA
    ----
    no calling on init!

    GOAL
    ----
    1. (MAIN) delay probable raising on direct func execution (used with AttrLambdaCall)
    like creating objects on Cls attributes
        class Cls:
            ATTR = PrivateValues(123)   # -> Lambda(PrivateValues, 123)

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

    # OVERWRITE! ------------------------------------------------------------------------------------------------------
    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        return self.construct(*args, **kwargs)

    def __eq__(self, other) -> bool | NoReturn:
        return ValidAux.eq_doublesided__bool(other, self())

    # UNIVERSAL =======================================================================================================
    def __init__(self, constructor: TYPE__LAMBDA_CONSTRUCTOR, *args, **kwargs) -> None:
        self.CONSTRUCTOR = constructor
        super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def construct(self, *args, **kwargs) -> Any | NoReturn:
        """
        unsafe (raise acceptable) get value
        """
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        if callable(self.CONSTRUCTOR) or TypeChecker.check__class(self.CONSTRUCTOR):
            return self.CONSTRUCTOR(*args, **kwargs)
        else:
            return self.CONSTRUCTOR

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
        result = bool(self.construct(*args, **kwargs))
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


class LambdaBoolReversed(LambdaBool):
    """
    just a reversed LambdaBool
    """
    BOOL_REVERSE: bool = True


# =====================================================================================================================
class LambdaTrySuccess(LambdaBool):
    """
    just an ability to check if object is not raised on call

    BEST PRACTICE
    -------------
    1. direct/quick/shortest checks without big trySentence
        if LambdaTrySuccess(func):
            return func()

    2. pytestSkipIf
        @pytest.mark.skipif(LambdaTryFail(func), ...)

    3. pytest assertions

        class Victim(DictDotsAnnotRequired):
            lowercase: str

        assert LambdaTryFail(Victim)
        assert not LambdaTrySuccess(Victim)
        assert LambdaTrySuccess(Victim, lowercase="lowercase")
    """
    def __call__(self, *args, **kwargs) -> bool:
        try:
            self.construct(*args, **kwargs)
            return not self.BOOL_REVERSE
        except:
            return bool(self.BOOL_REVERSE)


class LambdaTryFail(LambdaTrySuccess):
    BOOL_REVERSE: bool = True


# =====================================================================================================================
class LambdaSleep(Lambda):
    """
    just delay construction
    """
    WHEN: When2 = When2.BEFORE
    SEC: float = 1

    def __init__(self, sec: float = None, *args, **kwargs) -> None:
        if sec is not None:
            self.SEC = sec
        super().__init__(*args, **kwargs)

    def __call__(self, sec: float = None, *args, **kwargs) -> Any | NoReturn:
        if sec is None:
            sec = self.SEC

        if self.WHEN == When2.BEFORE:
            time.sleep(sec)
        result = self.construct(*args, **kwargs)
        if self.WHEN == When2.AFTER:
            time.sleep(sec)
        return result


# ---------------------------------------------------------------------------------------------------------------------
class LambdaSleepAfter(LambdaSleep):
    """
    CREATED SPECIALLY FOR
    ---------------------
    UART/ATC tests for RST command
    """
    WHEN: When2 = When2.AFTER


# =====================================================================================================================
