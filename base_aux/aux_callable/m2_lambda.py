import time
import pytest

# from base_aux.aux_argskwargs.m1_argskwargs import TYPING__LAMBDA_CONSTRUCTOR
# from base_aux.aux_types import TypeAux   # CIRCULAR IMPORT

from base_aux.aux_eq.m2_eq_aux import *
from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.base_nest_dunders.m3_calls import *


# =====================================================================================================================
# class LambdaSimple(NestInit_SourceKwArgs_Implicit, NestCall_Resolve):
#     """
#     NOTE
#     ----
#     CANT USE IT AS OBJECT IN THREAD!!!
#     so just use Lambda
#
#     GOAL
#     ----
#     simple replace common lambda func!
#     """
#     # SOURCE: Union[Callable[..., Any], Any, type]
#     #
#     # # =================================================================================================================
#     # def resolve(self, *args, **kwargs) -> Any | NoReturn:
#     #     if callable(self.SOURCE):
#     #         result = self.SOURCE(*args, **kwargs)
#     #     else:
#     #         result = self.SOURCE
#     #     return result
#     #
#     # # def __eq__(self, other: Any) -> bool | NoReturn:      # NOTE: DONT USE EQ!
#     # #     return EqAux(self()).check_doubleside__bool(other)
#     #
#     # def __bool__(self) -> bool | NoReturn:
#     #     return bool(self())
#     #
#     # # =================================================================================================================
#     # def check_raise(self, *args, **kwargs) -> bool:
#     #     try:
#     #         result = self(*args, **kwargs)
#     #         return False
#     #     except:
#     #         return True
#     #
#     # def check_no_raise(self, *args, **kwargs) -> bool:
#     #     return not self.check_raise(*args, **kwargs)
#     #
#     # def wait_finished(self, sleep: float = 1) -> None:
#     #     """
#     #     GOAL
#     #     ----
#     #     run if not started yet
#     #     then wait finished
#     #     """
#     #     if self.PROCESS_ACTIVE == Enum_ProcessStateActive.NONE:
#     #         self.run()
#     #
#     #     count = 1
#     #     while self.PROCESS_ACTIVE != Enum_ProcessStateActive.FINISHED:
#     #         print(f"wait_finished {count=}")
#     #         count += 1
#     #         time.sleep(sleep)


# =====================================================================================================================
class Lambda(NestInit_SourceKwArgs_Implicit, NestCall_Resolve):
    """
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

    NOTE
    ----
    no calling on init!

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
    here is not intended using indirect result like Exception! just raise if raised! so not safe state!

    NOTE
    ----
    CANT REPLACE LAMBDA IN ANY CASE!
        func_link = lambda *_args: getattr(victim, meth)(*_args)
    - will call at same time by Lambda, and if meth is not exists - return :
        Lambda(getattr(victim, meth), *args)


    TIP
    ---
    if need ARGS resolve by SingleMulty - do it before
        self.ARGS = ArgsKwargsAux(args).resolve_args()

    """
    SOURCE: Union[Callable[..., Any], Any, type]

    # thread ready -----
    PROCESS_ACTIVE: Enum_ProcessStateActive = Enum_ProcessStateActive.NONE
    RESULT: Any = None
    EXX: Optional[Exception] = None

    # UNIVERSAL =======================================================================================================
    def run(self, *args, **kwargs) -> None:
        """
        NOTE
        ----
        DONT USE for getting result! only to execute calculation process!!!
        and thread ready for start usage!
        """
        # ONLY ONE EXECUTION on instance!!! dont use locks! -------------
        if self.PROCESS_ACTIVE == Enum_ProcessStateActive.STARTED:
            return

        # WORK ----------------------------------------------------------
        self.PROCESS_ACTIVE = Enum_ProcessStateActive.STARTED
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
        self.PROCESS_ACTIVE = Enum_ProcessStateActive.FINISHED

    # =================================================================================================================
    def resolve(self, *args, **kwargs) -> Any | NoReturn:
        # OVERWRITE for derivatives!!!!
        self.run(*args, **kwargs)
        self.wait_finished()

        # FIN ----------------------------------------------------------
        if self.EXX is not None:
            raise self.EXX
        else:
            return self.RESULT

    def __eq__(self, other: Any) -> bool | NoReturn:        # TODO: decide deprecate???
        return EqAux(self()).check_doubleside__bool(other)

    def __bool__(self) -> bool | NoReturn:
        return bool(self())

    # =================================================================================================================
    def check_raise(self, *args, **kwargs) -> bool:     # TODO: decide what to do with different kwArgs in several starts/runs
        self.run(*args, **kwargs)
        self.wait_finished()

        # FIN ----------------------------------------------------------
        if self.EXX is not None:
            return True
        else:
            return False

    def check_no_raise(self, *args, **kwargs) -> bool:
        return not self.check_raise(*args, **kwargs)

    def wait_finished(self, sleep: float = 1, run: bool = None) -> None:
        """
        GOAL
        ----
        run if not started yet
        then wait finished

        NOTE
        ----
        dont forget using always after run!!!
        """
        if run or self.PROCESS_ACTIVE == Enum_ProcessStateActive.NONE:
            self.run()

        count = 1
        while self.PROCESS_ACTIVE != Enum_ProcessStateActive.FINISHED:
            print(f"wait_finished {count=}")
            count += 1
            time.sleep(sleep)

    # =================================================================================================================
    def expect__check_assert(
            self,
            # args: TYPING.ARGS_DRAFT = (),      # DONT USE HERE!!!
            # kwargs: TYPING.KWARGS_DRAFT = None,

            _EXPECTED: TYPING.EXPECTED = True,
            # EXACT VALUE (noCallable) OR AnyCLass - to cmp as isinstanceOrSubclass!!!
            _MARK: pytest.MarkDecorator | None = None,
            _COMMENT: str | None = None,
    ) -> None | NoReturn:
        """
        NOTE
        ----
        this is same as funcs.Valid! except following:
            - if validation is Fail - raise assert!
            - no skips/cumulates/logs/ last_results/*values

        GOAL
        ----
        test target func/obj with exact parameters
        no exception withing target func!

        SPECIALLY CREATED FOR
        ---------------------
        unit tests by pytest
        """
        args = self.ARGS
        kwargs = self.KWARGS
        comment = _COMMENT or ""

        # MARKS -------------------------
        # print(f"{pytest.mark.skipif(True)=}")
        if _MARK == pytest.mark.skip:
            pytest.skip("skip")
        elif isinstance(_MARK, pytest.MarkDecorator) and _MARK.name == "skipif" and all(_MARK.args):
            pytest.skip("skipIF")

        try:
            actual_value = self.resolve(*args, **kwargs)
        except Exception as exx:
            actual_value = exx  # this is an internal value! when use incorrect ArgsKw!!!

        print(f"Expected[{self.SOURCE}/{args=}/{kwargs=}//{actual_value=}/{_EXPECTED=}]")
        result = (
                TypeAux(actual_value).check__subclassed_or_isinst(_EXPECTED)
                or
                EqAux(actual_value).check_doubleside__bool(_EXPECTED)
        )
        if _MARK == pytest.mark.xfail:
            assert not result, f"[xfail]{comment}"
        else:
            assert result

    def expect__check_bool(self, *args, **kwargs) -> bool:
        """
        GOAL
        ----
        extend work for not only in unittests
        """
        try:
            self.expect__check_assert(*args, **kwargs)
            return True
        except:
            return False


# =====================================================================================================================
