from typing import *
import time

# from base_aux.aux_argskwargs.m1_argskwargs import TYPE__LAMBDA_CONSTRUCTOR
from base_aux.base_statics.m4_enums import *
# from base_aux.aux_types import TypeAux   # CIRCULAR IMPORT
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import NestInit_SourceKwArgs_Implicite

from base_aux.aux_cmp_eq.m2_eq_aux import *


# =====================================================================================================================
class Lambda(NestInit_SourceKwArgs_Implicite):
    """
    IDEA
    ----
    no calling on init!

    GOAL
    ----
    1. (MAIN) delay probable raising on direct func execution (used with NestInit_AttrsLambdaResolve)
    like creating aux_types on Cls attributes
        class Cls:
            ATTR = PrivateValues(123)   # -> Lambda(PrivateValues, 123) - IT IS OLD!!!! but could be used as example!

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
    Item for using with NestInit_AttrsLambdaResolve

    WHY NOT 1=simple LAMBDA?
    ------------------------
    extremely good point!
    but
    1. in case of at least NestInit_AttrsLambdaResolve you cant distinguish method or callable attribute!
    so you explicitly define attributes/aux_types for later constructions
    and in some point it can be more clear REPLACE LAMBDA by this solvation!!!

    2.

    PARAMS
    ======
    :ivar SOURCE: any class or function
    """
    SOURCE: Union[Callable, Any]

    # UNIVERSAL =======================================================================================================
    def construct(self, *args, **kwargs) -> Any | NoReturn:
        """
        unsafe (raise acceptable) get value
        """
        args = args or self.ARGS
        kwargs = kwargs or self.KWARGS
        if callable(self.SOURCE):  # callable accept all variants! TypeAux.check__callable_func_meth_inst_cls!
            return self.SOURCE(*args, **kwargs)
        else:
            return self.SOURCE

    # -----------------------------------------------------------------------------------------------------------------
    def __bool__(self) -> bool | NoReturn:
        return bool(self(*self.ARGS, **self.KWARGS))

    # OVERWRITE! ======================================================================================================
    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        return self.construct(*args, **kwargs)

    def __eq__(self, other) -> bool | NoReturn:
        return EqAux(self()).check_doubleside__bool(other)


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

        class Victim(DictAttrAnnotRequired):
            lowercase: str

        assert LambdaTryFail(Victim)
        assert not LambdaTrySuccess(Victim)
        assert LambdaTrySuccess(Victim, lowercase="lowercase")

    EXAMPLES
    --------
        if callables and LambdaTrySuccess(getattr, source, name) and callable(getattr(source, name)):
            continue

        so here raise is acceptable in getattr(source, name) in case of PROPERTY_RAISE
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

        if self.WHEN is When2.BEFORE:
            time.sleep(sec)
        result = self.construct(*args, **kwargs)
        if self.WHEN is When2.AFTER:
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
