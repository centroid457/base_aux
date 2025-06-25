import platform

from base_aux.lambdas.m1_lambda import Lambda
from base_aux.aux_types.m0_static_types import *
from base_aux.aux_types.m0_static_typing import TYPING

# =====================================================================================================================
TYPE__VALUES = Union[str, list[str], dict[str, bool | None]]


# =====================================================================================================================
class Meta_GetattrClassmethod(type):
    """
    GOAL
    ----
    ability to apply classmethod for __getattr__

    WHY USE IT
    ==========
    cause of direct __getattr__ usage - is not applicable!

        class Cls:
        @classmethod
        def __getattr__(cls, item):
            print(item)

        Cls.hello()

        # RESULT
            Cls.hello()
            ^^^^^^^^^
        AttributeError: type object 'Cls' has no attribute 'hello'

    WHY WE NEED CLASSMETH instead of simple SELFMETHOD
    --------------------------------------------------
    1. ability to use methods without creating instances - its a quick/simple
        from requirements import ReqCheckStr_Os
        ReqCheckStr_Os.raise_if_not__LINUX
    """
    # dont change markers! use exists!
    _MARKER__BOOL_IF: str = "bool_if__"
    _MARKER__BOOL_IF_NOT: str = "bool_if_not__"

    _MARKER__RAISE_IF: str = "raise_if__"
    _MARKER__RAISE_IF_NOT: str = "raise_if_not__"

    check__wo_raise: Callable
    check__w_raise: Callable

    def __getattr__(cls, item: str) -> bool | None | NoReturn:
        """if no exists attr/meth
        """
        if item.lower().startswith(cls._MARKER__BOOL_IF.lower()):
            attr_name = item.lower().replace(cls._MARKER__BOOL_IF.lower(), "")
            return lambda: cls().check__wo_raise(value_acceptance=attr_name, _reverse=False, _meet_true=False)
        elif item.lower().startswith(cls._MARKER__BOOL_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__BOOL_IF_NOT.lower(), "")
            return lambda: cls().check__wo_raise(value_acceptance=attr_name, _reverse=True, _meet_true=False)

        elif item.lower().startswith(cls._MARKER__RAISE_IF.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF.lower(), "")
            return lambda: not cls().check__w_raise(value_acceptance=attr_name, _reverse=True, _meet_true=False) or None
        elif item.lower().startswith(cls._MARKER__RAISE_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF_NOT.lower(), "")
            return lambda: not cls().check__w_raise(value_acceptance=attr_name, _reverse=False, _meet_true=False) or None

        else:
            msg = f"[ERROR] META:'{cls.__name__}' CLASS has no attribute '{item}'"
            raise AttributeError(msg)


# =====================================================================================================================
class Base_ReqCheckStr(metaclass=Meta_GetattrClassmethod):
    """
    GOAL
    ----
    check requirements with self exclusive

    IDEA
    ----
    1/ annots names - used as str params for validating
    2/ annots values - used as acceptance (True/False/None)
    3/ expecting find first match (originally obly one) and decide what to do with it
        - if False value in cls - Raise
        - if True value in cls - assumed correct check/requirements met!

    RULES
    -----
    all check variants keep in not hidden annots

    Base class for check exact requirement by string value

    NOTE
    ----
    USUALLY YOU DONT NEED USING IT LIKE INSTANCE!
    just create appropriate class with _GETTER +add bare annotations with markers (see examples like ReqCheckStr_Os)

    VARIANTS for check
    ------------------
    add attributes with bool values (case-insensitive)
        - True - if value is definitely acceptable - Always need at least one True!!!
        - False - if not definitely acceptable
        - None - if requirement is undefined

    SETTINGS
    --------
    :ivar _MEET_TRUE: you can use requirement class for check only false variant
    :ivar _GETTER: function which will get the exact value to check
    :ivar _value_actual:
    """

    # NOTE: HIDDEN NAMES IS IMPORTANT! separate attrs Variants from privateAux
    pass

    # SETTINGS -------------------------------------------
    _GETTER: Union[Callable[..., Union[str, Any]], Any] = None
    _VALIDATOR: Callable[[Any, Any], bool | NoReturn] = lambda source, var: str(source).lower() == str(var).lower()

    # AUX ------------------------------------------------
    _MEET_TRUE: bool = True     # DONT DELETE!!! used like selector! used as validator

    # temporary ------------------------------------------
    _value_actual: Optional[str]

    # TODO: separate ATTRS in KIT and

    # TODO: use instance! no classmethods! + check on instantiating!?? +del meta??  ---NO!!!!
    # NOTES:
    #   classmethods = keep all!!! for class!
    #   instantiating use for CHECK_RAISE/NORASE!!!

    # TODO: add values as dict??? - it would be direct great!
    # TODO: use setter as source
    # TODO: add properties ANY/ALL_True/False
    # TODO: del _meet_true
    # TODO: reuse validator with callableAuxResolve instead of _validator

    # @classmethod
    # @property
    # def ANY_TRUE(self) -> bool:
    #     pass
    #
    # @classmethod
    # @property
    # def ANY_FALSE(self) -> bool:
    #     pass
    #
    # @classmethod
    # @property
    # def ALL_TRUE(self) -> bool:
    #     pass
    #
    # @classmethod
    # @property
    # def ALL_FALSE(self) -> bool:
    #     pass

    def __init__(
            self,
            _getter: Callable[..., str] = None,
            _meet_true: Optional[bool] = None,
            _validator: Callable[[Any, Any], bool | NoReturn] = None
    ):
        # INIT SETTINGS ----------------------------------
        if _getter is not None:
            self._GETTER = _getter
        if _meet_true is not None:
            self._MEET_TRUE = _meet_true
        if _validator is not None:
            self._VALIDATOR = _validator

    def __getattr__(self, item):
        """
        apply access to not exists methods from instance! in metaclass we have only access as classmethods!
        """
        # return super().__getattr__(item)    # AttributeError: 'super' object has no attribute '__getattr__'. Did you mean: '__setattr__'?
        return Meta_GetattrClassmethod.__getattr__(self.__class__, item)

    @classmethod
    def _values_acceptance__get_from_cls(cls) -> dict[str, bool | None]:
        """get settings from class"""
        result = {}
        for attr in dir(cls):
            attr_value = getattr(cls, attr)
            if not attr.startswith("_") and not callable(attr_value) and isinstance(attr_value, (bool, type(None))):
                result.update({attr: attr_value})
        return result

    @classmethod
    def _value_actual__get(cls) -> str | NoReturn:
        cls._value_actual = Lambda(cls._GETTER).resolve__raise()
        cls._value_actual = str(cls._value_actual).lower()
        return cls._value_actual

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def check__wo_raise(cls, *args, **kwargs) -> TYPING.RESULT__BOOL_NONE:
        try:
            return cls.check__w_raise(*args, **kwargs)
        except Exception as exx:
            print(f"{exx!r}")
            return False

    @classmethod
    def check__w_raise(
            cls,
            value_acceptance: TYPE__VALUES | None = None,
            _reverse: bool = None,    # special for bool_if_not__* like methods
            _meet_true: bool = None,
    ) -> TYPING.RESULT__BOOL_RAISE_NONE:
        # SETTINGS -------------------------------------------------------
        if _meet_true is None:
            _meet_true = cls._MEET_TRUE

        # VALUES ---------------------------------------------------------
        # use values-1=from class settings -----------
        if value_acceptance is None:
            value_acceptance = cls._values_acceptance__get_from_cls()

        # use values-2=as exact one -----------
        if isinstance(value_acceptance, str):
            value_acceptance = {value_acceptance: True}

        # use values-3=as exact several -----------
        if isinstance(value_acceptance, (list, tuple)):
            value_acceptance = dict.fromkeys(value_acceptance, True)

        # REVERSE apply --------------------------------------------------
        if _reverse:
            for value, acceptance in value_acceptance.items():
                if acceptance in (True, False):
                    value_acceptance[value] = not acceptance

        # VALUE ACTUAL ---------------------------------------------------
        _value_actual = cls._value_actual__get()

        # WORK -----------------------------------------------------------
        match = None
        _acceptance = None
        for value, _acceptance in value_acceptance.items():
            match = cls._VALIDATOR(_value_actual, value)
            if match:
                break

        if match:
            acceptance = _acceptance
        else:
            acceptance = not _reverse

        # acceptance --------------
        result = None
        if acceptance is True:
            result = match
        elif acceptance is False:
            result = not match
        elif acceptance is None:
            result = None

        # FINAL --------------
        if _meet_true is True and result is None:
            msg = f"[WARN] value is not MeetTrue [{cls.__name__}/{cls._value_actual=}/req={value_acceptance}]"
            raise Exx__Expected(msg)

        if result in (True, None):
            return result
        else:
            msg = f"[WARN] value is not [{cls.__name__}/{cls._value_actual=}/req={value_acceptance}]"
            raise Exx__Expected(msg)


# =====================================================================================================================
class ReqCheckStr_Os(Base_ReqCheckStr):
    _GETTER: Callable = platform.system
    _MEET_TRUE: bool = False        # need to use class as checker

    LINUX: bool
    WINDOWS: bool

    # DERIVATIVES --------
    bool_if__LINUX: TYPING.CALLABLE__BOOL_NONE
    bool_if__WINDOWS: TYPING.CALLABLE__BOOL_NONE
    bool_if_not__LINUX: TYPING.CALLABLE__BOOL_NONE
    bool_if_not__WINDOWS: TYPING.CALLABLE__BOOL_NONE

    raise_if__LINUX: TYPING.CALLABLE__RAISE_NONE
    raise_if__WINDOWS: TYPING.CALLABLE__RAISE_NONE
    raise_if_not__LINUX: TYPING.CALLABLE__RAISE_NONE
    raise_if_not__WINDOWS: TYPING.CALLABLE__RAISE_NONE


# ---------------------------------------------------------------------------------------------------------------------
def _examples():
    # 1=direct сlass
    assert ReqCheckStr_Os.bool_if__WINDOWS()
    assert not ReqCheckStr_Os.bool_if_not__WINDOWS()
    try:
        ReqCheckStr_Os.raise_if__LINUX()
        assert False
    except:
        pass

    # 2=user object - best way!
    class ReqCheckStr_Os_MY(ReqCheckStr_Os):
        LINUX: bool = True
        WINDOWS: bool = False

    assert not ReqCheckStr_Os_MY().check__wo_raise()


# =====================================================================================================================
class ReqCheckStr_Arch(Base_ReqCheckStr):
    _GETTER: Callable = platform.machine
    _MEET_TRUE: bool = False

    AMD64: bool      # standard PC
    x86_64: bool     # wsl standard
    AARCH64: bool    # raspberry=ARM!

    # DERIVATIVES --------
    raise_if_not__AARCH64: TYPING.CALLABLE__RAISE_NONE


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
