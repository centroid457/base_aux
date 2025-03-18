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

    WHY NOT 2=CallableAux
    ------------------------
    here is not intended using indirect result like Exception! so NO CallingResolve!
    """
    SOURCE: Union[Callable, Any, type]

    PROCESS_ACTIVE: Enum_ProcessActive = Enum_ProcessActive.NONE
    RESULT: Any = None
    EXX: Optional[Exception] = None

    # UNIVERSAL =======================================================================================================
    def construct(self, *args, **kwargs) -> None:
        # ONLY ONE EXECUTION on instance!!! dont use locks! -------------
        if self.PROCESS_ACTIVE == Enum_ProcessActive.STARTED:
            return
        self.PROCESS_ACTIVE = Enum_ProcessActive.STARTED

        # WORK ----------------------------------------------------------
        self.RESULT = None
        self.EXX = None

        args = args or self.ARGS
        kwargs = {**self.KWARGS, **kwargs}

        try:
            if callable(self.SOURCE):  # callable accept all variants! TypeAux.check__callable_func_meth_inst_cls!
                self.RESULT = self.SOURCE(*args, **kwargs)
            else:
                self.RESULT = self.SOURCE
        except Exception as exx:
            print(f"{exx!r}")
            self.EXX = exx

        # FIN ----------------------------------------------------------
        self.PROCESS_ACTIVE = Enum_ProcessActive.FINISHED

    def run(self) -> None:
        """
        GOAL
        ----
        thread purpose
        """
        self.construct()

    # OVERWRITE! ======================================================================================================
    def __call__(self, *args, **kwargs) -> Any | NoReturn:
        self.construct(*args, **kwargs)

        if self.EXX is not None:
            raise self.EXX
        else:
            return self.RESULT

    def __eq__(self, other) -> bool | NoReturn:
        return EqAux(self()).check_doubleside__bool(other)

    # =================================================================================================================
    def check_raise(self, *args, **kwargs) -> bool:     # TODO: decide what to do with different kwArgs in several starts/runs
        self.construct(*args, **kwargs)
        self.wait_finished()
        if self.EXX is not None:
            return True
        else:
            return False

    def check_no_raise(self, *args, **kwargs) -> bool:
        return not self.check_raise(*args, **kwargs)

    def wait_finished(self, sleep: float = 1) -> None:
        if self.PROCESS_ACTIVE == Enum_ProcessActive.NONE:
            self.run()

        count = 1
        while self.PROCESS_ACTIVE != Enum_ProcessActive.FINISHED:
            print(f"wait_finished {count=}")
            count += 1
            time.sleep(sleep)

    # -----------------------------------------------------------------------------------------------------------------
    def __bool__(self) -> bool | NoReturn:
        return bool(self())


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
    def __call__(self, *args, **kwargs) -> bool | NoReturn:
        self.construct(*args, **kwargs)

        if self.EXX is not None:
            raise self.EXX
        else:
            return bool(self.RESULT)


class LambdaBoolReversed(LambdaBool):
    """
    just a reversed LambdaBool
    """
    def __call__(self, *args, **kwargs) -> bool | NoReturn:
        self.construct(*args, **kwargs)

        if self.EXX is not None:
            raise self.EXX
        else:
            return not bool(self.RESULT)


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
        self.construct(*args, **kwargs)

        if self.EXX is not None:
            return False
        else:
            return True


class LambdaTryFail(LambdaTrySuccess):
    def __call__(self, *args, **kwargs) -> bool:
        self.construct(*args, **kwargs)

        if self.EXX is not None:
            return True
        else:
            return False


# =====================================================================================================================
class LambdaSleep(Lambda):
    """
    just delay construction
    """
    WHEN: Enum_When2 = Enum_When2.BEFORE
    SEC: float = 1

    def __init__(self, sec: float = None, *args, **kwargs) -> None:
        if sec is not None:
            self.SEC = sec
        super().__init__(*args, **kwargs)

    def __call__(self, sec: float = None, *args, **kwargs) -> Any | NoReturn:
        if sec is None:
            sec = self.SEC

        if self.WHEN is Enum_When2.BEFORE:
            time.sleep(sec)

        self.construct(*args, **kwargs)

        if self.WHEN is Enum_When2.AFTER:
            time.sleep(sec)

        if self.EXX is not None:
            raise self.EXX
        else:
            return self.RESULT


# ---------------------------------------------------------------------------------------------------------------------
class LambdaSleepAfter(LambdaSleep):
    """
    CREATED SPECIALLY FOR
    ---------------------
    UART/ATC tests for RST command
    """
    WHEN: Enum_When2 = Enum_When2.AFTER


# =====================================================================================================================
