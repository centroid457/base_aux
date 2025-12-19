from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_enums.m2_enum1_adj import EnumAdj_When2


# =====================================================================================================================
class Lambda_Bool(Lambda):
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
        skip_link__direct = Lambda_Bool(bool)  # correct
        skip_link__reversal = not bool  # incorrect
        skip_link__reversal = Lambda_Bool(bool, attr).get_reverse  # correct

    but here we can use lambda
        skip_link__reversal = lambda attr: not bool(attr)  # correct but not so convenient ???

    PARAMS
    ------
    :ivar BOOL_REVERSE: just for Lambda_BoolReversed, no need to init
    """
    def resolve(self, *args, **kwargs) -> bool | NoReturn:
        self.run(*args, **kwargs)

        if self.EXC is not None:
            raise self.EXC
        else:
            return bool(self.RESULT)


# ---------------------------------------------------------------------------------------------------------------------
class Lambda_BoolReversed(Lambda_Bool):
    """
    just a reversed Lambda_Bool
    """
    def resolve(self, *args, **kwargs) -> bool | NoReturn:
        self.run(*args, **kwargs)

        if self.EXC is not None:
            raise self.EXC
        else:
            return not bool(self.RESULT)


# =====================================================================================================================
class Lambda_TrySuccess(Lambda_Bool):
    """
    just an ability to check if object is not raised on call

    BEST PRACTICE
    -------------
    1. direct/quick/shortest checks without big trySentence
        if Lambda_TrySuccess(func):
            return func()

    2. pytestSkipIf
        @pytest.mark.skipif(Lambda_TryFail(func), ...)

    3. pytest assertions

        class Victim(DictIcKeys_Ga_AnnotRequired):
            lowercase: str

        assert Lambda_TryFail(Victim)
        assert not Lambda_TrySuccess(Victim)
        assert Lambda_TrySuccess(Victim, lowercase="lowercase")

    EXAMPLES
    --------
        if callables and Lambda_TrySuccess(getattr, source, name) and callable(getattr(source, name)):
            continue

        so here raise is acceptable in getattr(source, name) in case of PROPERTY_RAISE
    """
    def resolve(self, *args, **kwargs) -> bool:
        self.run(*args, **kwargs)

        if self.EXC is not None:
            return False
        else:
            return True


# ---------------------------------------------------------------------------------------------------------------------
class Lambda_TryFail(Lambda_TrySuccess):
    def resolve(self, *args, **kwargs) -> bool:
        self.run(*args, **kwargs)

        if self.EXC is not None:
            return True
        else:
            return False


# =====================================================================================================================
class Lambda_Sleep(Lambda):
    """
    GOAL
    ----
    it is not just a sleep func!
    it sleep added for other func! - before or after its execution!
    """
    WHEN: EnumAdj_When2 = EnumAdj_When2.BEFORE
    SEC: float = 1

    def __init__(self, *args, sec: float = None, **kwargs) -> None:
        if sec is not None:
            self.SEC = sec
        super().__init__(*args, **kwargs)

    def resolve(self, sec: float = None, *args, **kwargs) -> Any | NoReturn:
        if sec is None:
            sec = self.SEC

        if self.WHEN is EnumAdj_When2.BEFORE:
            time.sleep(sec)

        self.run(*args, **kwargs)

        if self.WHEN is EnumAdj_When2.AFTER:
            time.sleep(sec)

        if self.EXC is not None:
            raise self.EXC
        else:
            return self.RESULT


# ---------------------------------------------------------------------------------------------------------------------
class Lambda_SleepAfter(Lambda_Sleep):
    """
    CREATED SPECIALLY FOR
    ---------------------
    UART/ATC tests for RST command
    """
    WHEN: EnumAdj_When2 = EnumAdj_When2.AFTER


# =====================================================================================================================
