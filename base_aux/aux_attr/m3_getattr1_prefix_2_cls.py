from typing import *


# =====================================================================================================================
class Meta_GaClsPrefix_Example(type):
    """
    NOTE
    ----
    THIS IS ONLY AS EXAMPLE!!! in any situation you need to create specific Meta-class!!!

    GOAL
    ----
    get attributes from CLASS! not instance!

    CREATED SPECIALLY FOR
    ---------------------
    the main goal

    BEST USAGE
    ----------
    for example usages see requirements.ReqCheckStr_Base, annot_attrs. or here _GetattrCls_Meta__Echo
    """
    # TODO: add example! + tests! +REF!
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
