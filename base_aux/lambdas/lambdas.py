from typing import *
import time

from base_aux.base_argskwargs.argskwargs import *
from base_aux.base_enums.enums import When2
from base_aux.base_objects import TypeChecker

from base_aux.valid.valid_0_aux import ValidAux


# =====================================================================================================================
class Lambda(ArgsKwargs):
    """
    IDEA
    ----
    no calling on init!

    GOAL
    ----
    1. (MAIN) delay probable raising on direct func execution (used with AttrLambdaCall)
    like creating base_objects on Cls attributes
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
    so you explicitly define attributes/base_objects for later constructions
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
        if callable(self.CONSTRUCTOR):  # callable accept all variants! TypeChecker.check__callable_func_meth_inst_cls!
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

        SPECIFIC LOGIC
        --------------
        if callable - call and return result.
        else - return source.

        GOAL
        ----
        get common expected for any python code result - simple calculate or raise!
        because of get_result_or_exx is not enough!

        CREATED SPECIALLY FOR
        ---------------------
        GetattrPrefixInst
        """
        return self(*args, **kwargs)

    def get_result_or_exx(self, *args, **kwargs) -> bool | Exception:
        """
        GOAL
        ----
        same as get_result_or_raise but
        attempt to simplify result by not using try-sentence.
        so if get raise in get_result_or_raise - return Exx object

        USEFUL IDEA
        -----------
        1. in gui when its enough to get str() on result and see the result

        SPECIALLY CREATED FOR
        ---------------------
        just in case

        """
        try:
            return self(*args, **kwargs)
        except Exception as exx:
            return exx

    def get_result_bool(self, *args, **kwargs) -> bool:
        """
        GOAL
        ----
        same as get_result_or_exx but
        apply bool func on result

        ability to get bool result with meanings:
            - methods/funcs must be called
                assert get_bool(LAMBDA_TRUE) is True
                assert get_bool(LAMBDA_NONE) is False

            - Exceptions assumed as False
                assert get_bool(Exception) is False
                assert get_bool(Exception("FAIL")) is False
                assert get_bool(LAMBDA_EXX) is False

            - for other values get classic bool()
                assert get_bool(None) is False
                assert get_bool([]) is False
                assert get_bool([None, ]) is True

                assert get_bool(LAMBDA_LIST) is False
                assert get_bool(LAMBDA_LIST, [1, ]) is True

            - if on bool() exception raised - return False!
                assert get_bool(ClsBoolRaise()) is False

        CREATED SPECIALLY FOR
        ---------------------
        funcs.Valid.skip_link or else value/func assumed as bool result
        """
        try:
            result = Lambda(self.CONSTRUCTOR).get_result_or_raise(*args, **kwargs)
            if TypeChecker.check__exception(result):
                return False
            return bool(result)
        except:
            return False

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
