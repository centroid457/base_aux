from typing import *
from object_info import *
import platform


# =====================================================================================================================
TYPE__VALUES = Union[str, list[str], dict[str, bool | None]]

TYPE__RESULT_BOOL = Callable[..., bool]
TYPE__RESULT_RAISE = Callable[..., Optional[NoReturn]]


# =====================================================================================================================
class Exx_RequirementCantGetActualValue(Exception):
    """
    """


class Exx_Requirement(Exception):
    """Some of the requirements are not match
    """


# =====================================================================================================================
class _GetattrClassmethod_Meta(type):
    """ability to apply classmethod for __getattr__

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
        from requirements_checker import ReqCheckStr_Os
        ReqCheckStr_Os.raise_if_not__LINUX
    """

    # dont change markers! use exists!
    _MARKER__BOOL_IF: str = "bool_if__"
    _MARKER__BOOL_IF_NOT: str = "bool_if_not__"
    _MARKER__RAISE_IF: str = "raise_if__"
    _MARKER__RAISE_IF_NOT: str = "raise_if_not__"

    def __getattr__(cls, item: str):
        """if no exists attr/meth
        """
        if item.lower().startswith(cls._MARKER__BOOL_IF.lower()):
            attr_name = item.lower().replace(cls._MARKER__BOOL_IF.lower(), "")
            return lambda: cls.check(values=attr_name, _raise=False, _reverse=False, _meet_true=False)
        elif item.lower().startswith(cls._MARKER__BOOL_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__BOOL_IF_NOT.lower(), "")
            return lambda: cls.check(values=attr_name, _raise=False, _reverse=True, _meet_true=False)

        elif item.lower().startswith(cls._MARKER__RAISE_IF.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF.lower(), "")
            return lambda: not cls.check(values=attr_name, _raise=True, _reverse=True, _meet_true=False) or None
        elif item.lower().startswith(cls._MARKER__RAISE_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF_NOT.lower(), "")
            return lambda: not cls.check(values=attr_name, _raise=True, _reverse=False, _meet_true=False) or None

        else:
            msg = f"[ERROR] META:'{cls.__name__}' CLASS has no attribute '{item}'"
            raise AttributeError(msg)


# =====================================================================================================================
class ReqCheckStr_Base(metaclass=_GetattrClassmethod_Meta):
    """Base class for check exact requirement by string value

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
    :ivar _RAISE: raise in case of inacceptance
    :ivar _MEET_TRUE: you can use requirement class for check only false variant
    :ivar _CHECK_FULLMATCH:
        True - if need fullmatch (but always case-insensitive)
        False - if partial match by finding mentioned values in _value_actual

    :ivar _GETTER: function which will get the exact value to check
    :ivar _sample_actual:
    """
    # SETTINGS -------------------------------------
    _GETTER: Union[Callable[..., Union[str, Any]], Any] = None

    # AUX ---------------------------------------
    _RAISE: bool = True
    _MEET_TRUE: bool = True
    _CHECK_FULLMATCH: bool = True

    # temporary ------------------------------------------
    _value_actual: Optional[str]

    # TODO: add values as dict??? - it would be direct great!

    def __init__(
            self,
            _getter: Callable[..., str] = None,
            _raise: Optional[bool] = None,
            _meet_true: Optional[bool] = None,
            _check_fullmatch: Optional[bool] = None
    ):
        # INIT SETTINGS ----------------------------------
        if _getter is not None:
            self.__class__._GETTER = _getter
        if _raise is not None:
            self._RAISE = _raise
        if _meet_true is not None:
            self._MEET_TRUE = _meet_true
        if _check_fullmatch is not None:
            self._CHECK_FULLMATCH = _check_fullmatch

        # WORK -------------------------------------------
        self.check()

    def __getattr__(self, item):
        """
        apply access to not exists methods from instance! in metaclass we have only access as classmethods!
        """
        # return super().__getattr__(item)    # AttributeError: 'super' object has no attribute '__getattr__'. Did you mean: '__setattr__'?
        return _GetattrClassmethod_Meta.__getattr__(self.__class__, item)

    @classmethod
    def values_acceptance__get(cls) -> dict[str, bool | None]:
        """get settings from class"""
        values = {}
        for attr in dir(cls):
            attr_value = getattr(cls, attr)
            if not attr.startswith("_") and not callable(attr_value) and isinstance(attr_value, (bool, type(None))):
                values.update({attr: attr_value})
        return values

    @classmethod
    def _value_actual__get(cls) -> Union[str, NoReturn]:
        if not cls._GETTER:
            msg = f"[ERROR] incomplete settings [{cls._GETTER=}]"
            raise Exx_RequirementCantGetActualValue(msg)

        if TypeChecker.check__callable_func_meth_inst(cls._GETTER):
            try:
                cls._value_actual = str(cls._GETTER()).lower()
            except Exception as exx:
                raise Exx_RequirementCantGetActualValue(repr(exx))
        else:
            cls._value_actual = str(cls._GETTER).lower()

        return cls._value_actual

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def check(
            cls,
            values: TYPE__VALUES | None = None,
            _raise: Optional[bool] = None,
            _reverse: Optional[bool] = None,    # special for bool_if_not__* like methods
            _meet_true: bool | None = None,
    ) -> Union[bool, NoReturn, None]:
        # SETTINGS -------------------------------------------------------
        if _raise is None:
            _raise = cls._RAISE
        _reverse = _reverse or False

        if _meet_true is None:
            _meet_true = cls._MEET_TRUE

        # VALUES ---------------------------------------------------------
        # use values-1=from class settings -----------
        if values is None:
            values = cls.values_acceptance__get()

        # use values-2=as exact one -----------
        if isinstance(values, str):
            values = {values: True}

        # use values-3=as exact several -----------
        if isinstance(values, list):
            values = dict.fromkeys(values, True)

        # REVERSE ---------------------------------------------------
        if _reverse:
            for value, acceptance in values.items():
                if acceptance in (True, False):
                    values[value] = not acceptance

        # VALUE ACTUAL ---------------------------------------------------
        _value_actual = cls._value_actual__get()

        # WORK -----------------------------------------------------------
        match = None
        _acceptance = None
        for value, _acceptance in values.items():
            match = (
                (cls._CHECK_FULLMATCH and value.lower() == _value_actual.lower())
                or
                (not cls._CHECK_FULLMATCH and value.lower() in _value_actual.lower())
            )
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
            msg = f"[WARN] value is not MeetTrue [{cls.__name__}/{cls._value_actual=}/req={values}]"
            print(msg)
            if _raise:
                raise Exx_Requirement(msg)
            else:
                return False

        if result in (True, None):
            return result
        else:
            msg = f"[WARN] value is not [{cls.__name__}/{cls._value_actual=}/req={values}]"
            print(msg)
            if _raise:
                raise Exx_Requirement(msg)
            else:
                return False


# =====================================================================================================================
class ReqCheckStr_Os(ReqCheckStr_Base):
    _GETTER: Callable = platform.system
    _MEET_TRUE: bool = False        # need to use class as checker

    LINUX: bool
    WINDOWS: bool

    # DERIVATIVES --------
    bool_if__LINUX: TYPE__RESULT_BOOL
    bool_if__WINDOWS: TYPE__RESULT_BOOL
    bool_if_not__LINUX: TYPE__RESULT_BOOL
    bool_if_not__WINDOWS: TYPE__RESULT_BOOL

    raise_if__LINUX: TYPE__RESULT_RAISE
    raise_if__WINDOWS: TYPE__RESULT_RAISE
    raise_if_not__LINUX: TYPE__RESULT_RAISE
    raise_if_not__WINDOWS: TYPE__RESULT_RAISE


# =====================================================================================================================
class ReqCheckStr_Arch(ReqCheckStr_Base):
    _GETTER: Callable = platform.machine
    _MEET_TRUE: bool = False

    AMD64: bool      # standard PC
    x86_64: bool     # wsl standard
    AARCH64: bool    # raspberry=ARM!

    # DERIVATIVES --------
    raise_if_not__AARCH64: TYPE__RESULT_RAISE


# =====================================================================================================================
