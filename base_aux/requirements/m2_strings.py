from typing import *
import platform

from base_aux.aux_types.m1_type_aux import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_callable.m1_callable import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
TYPE__VALUES = Union[str, list[str], dict[str, bool | None]]


# =====================================================================================================================
class Meta_GetattrClassmethod(type):
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
        from requirements import ReqCheckStr_Os
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
            return lambda: cls().check_no_raise(values=attr_name, _raise=False, _reverse=False, _meet_true=False)
        elif item.lower().startswith(cls._MARKER__BOOL_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__BOOL_IF_NOT.lower(), "")
            return lambda: cls().check_no_raise(values=attr_name, _raise=False, _reverse=True, _meet_true=False)

        elif item.lower().startswith(cls._MARKER__RAISE_IF.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF.lower(), "")
            return lambda: not cls().check_raise(values=attr_name, _raise=True, _reverse=True, _meet_true=False) or None
        elif item.lower().startswith(cls._MARKER__RAISE_IF_NOT.lower()):
            attr_name = item.lower().replace(cls._MARKER__RAISE_IF_NOT.lower(), "")
            return lambda: not cls().check_raise(values=attr_name, _raise=True, _reverse=False, _meet_true=False) or None

        else:
            msg = f"[ERROR] META:'{cls.__name__}' CLASS has no attribute '{item}'"
            raise AttributeError(msg)


# =====================================================================================================================
class Base_ReqCheckStr(metaclass=Meta_GetattrClassmethod):
    """
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
    :ivar _RAISE: raise in case of inacceptance
    :ivar _MEET_TRUE: you can use requirement class for check only false variant
    :ivar _CHECK_FULLMATCH:
        True - if need fullmatch (but always case-insensitive)
        False - if partial match by finding mentioned values in _value_actual

    :ivar _GETTER: function which will get the exact value to check
    :ivar _value_actual:
    """

    # NOTE: HIDDEN NAMES IS IMPORTANT! separate attrs Variants from privateAux
    pass

    # SETTINGS -------------------------------------
    _GETTER: Union[Callable[..., Union[str, Any]], Any] = None

    # AUX ---------------------------------------
    _RAISE: bool = True
    _MEET_TRUE: bool = True     # DONT DELETE!!! used like selector!
    _CHECK_FULLMATCH: bool = True

    # temporary ------------------------------------------
    _value_actual: Optional[str]

    # TODO: use instance! no classmethods! + check on instantiating!?? +del meta??  ---NO!!!!
    # NOTES:
    #   classmethods = keep all!!! for class!
    #   instantiating use for CHECK_RAISE/NORASE!!!

    # TODO: add values as dict??? - it would be direct great!
    # TODO: use setter as source
    # TODO: add properties ANY/ALL_True/False
    # TODO: del _meet_true
    # TODO: reuse validator with callableAuxResolve instead of _check_fullmatch

    @classmethod
    @property
    def ANY_TRUE(self) -> bool:
        pass

    @classmethod
    @property
    def ANY_FALSE(self) -> bool:
        pass

    @classmethod
    @property
    def ALL_TRUE(self) -> bool:
        pass

    @classmethod
    @property
    def ALL_FALSE(self) -> bool:
        pass

    def __init__(
            self,
            _getter: Callable[..., str] = None,
            _raise: Optional[bool] = None,
            _meet_true: Optional[bool] = None,
            _check_fullmatch: Optional[bool] = None
    ):
        # INIT SETTINGS ----------------------------------
        if _getter is not None:
            self._GETTER = _getter
        if _raise is not None:
            self._RAISE = _raise
        if _meet_true is not None:
            self._MEET_TRUE = _meet_true
        if _check_fullmatch is not None:
            self._CHECK_FULLMATCH = _check_fullmatch

    def __getattr__(self, item):
        """
        apply access to not exists methods from instance! in metaclass we have only access as classmethods!
        """
        # return super().__getattr__(item)    # AttributeError: 'super' object has no attribute '__getattr__'. Did you mean: '__setattr__'?
        return Meta_GetattrClassmethod.__getattr__(self.__class__, item)

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
    def _value_actual__get(cls) -> str | NoReturn:
        cls._value_actual = CallableAux(cls._GETTER).resolve_raise()
        cls._value_actual = str(cls._value_actual).lower()
        return cls._value_actual

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def check_no_raise(cls, *args, **kwargs) -> bool:
        try:
            return cls.check_raise(*args, **kwargs)
        except:
            return False

    @classmethod
    def check_raise(
            cls,
            values: TYPE__VALUES | None = None,
            _raise: Optional[bool] = None,
            _reverse: Optional[bool] = None,    # special for bool_if_not__* like methods
            _meet_true: bool | None = None,
    ) -> Union[bool, None] | NoReturn:
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
                raise Exx__Requirement(msg)
            else:
                return False

        if result in (True, None):
            return result
        else:
            msg = f"[WARN] value is not [{cls.__name__}/{cls._value_actual=}/req={values}]"
            print(msg)
            if _raise:
                raise Exx__Requirement(msg)
            else:
                return False


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

    assert not ReqCheckStr_Os_MY().check_no_raise()


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
