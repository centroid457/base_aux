from typing import *
from base_aux.objects import *
from base_aux.exceptions import *

from base_aux.valid.valid_0_aux import ValidAux
from base_aux.classes.attr_1_aux import AttrAux


# =====================================================================================================================
class GetattrPrefixInst(AttrAux):
    """
    this is just a Base!

    EXAMPLES
    --------
    see GetattrPrefixInst_RaiseIf with tests
    """
    _GETATTR__PREFIXES: list[str] = []

    def __getattr__(self, item: str) -> Any | Callable | NoReturn:
        """
        SHARING PARAMS BETWEEN CALLABLE PREFIX/ITEM
        -------------------------------------------
        you can not use params! and not use callables (static attributes are available)!
        args - all - goes for ITEM
        kwargs - all uppercase - goes for PREFIX (after changing by lower())
        kwargs - others - goes for ITEM directly (without changing case)!

        if you provide not existed args/kwargs - you will get direct corresponding exception like "print(hello=1) -> TypeError: 'hello' is an invalid keyword argument for print() "

        NOTE
        ----
        0. CaseInSensitive!
        1. prefix - callable with first parameter as catching item_value (may be callable or not).
        2.You always need to CALL prefixed result! even if you access to not callable attribute!
        """
        for prefix in self._GETATTR__PREFIXES:
            prefix_original = self._attr_anycase__find(prefix, self)
            if not prefix_original:
                continue
            prefix_meth = getattr(self, prefix_original)

            if item.lower() == prefix.lower():
                return lambda *prefix_args, **prefix_kwargs: ValidAux.get_result_or_raise(prefix_meth, *prefix_args, **prefix_kwargs)

            if prefix_original and item.lower().startswith(prefix.lower()):
                item_short = item[len(prefix):]
                item_value = self._getattr_anycase(item_short, self)

                return lambda *meth_args, **meth_kwargs: ValidAux.get_result_or_raise(
                    prefix_meth,
                    *[ValidAux.get_result_or_raise(item_value, *meth_args, **{k:v for k,v in meth_kwargs.items() if not k.isupper()}), ],
                    **{k.lower():v for k,v in meth_kwargs.items() if k.isupper()}
                )

        raise AttributeError(item)


# =====================================================================================================================
class GetattrPrefixInst_RaiseIf(GetattrPrefixInst):
    """
    RULES
    -----
    """
    _GETATTR__PREFIXES = ["raise_if__", "raise_if_not__"]

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__(self, source: Any, _reverse: bool | None = None, comment: str = "") -> None | NoReturn:
        _reverse = _reverse or False
        result = ValidAux.get_result_or_exx(source)
        if TypeChecker.check__exception(result) or bool(result) != bool(_reverse):
            raise Exx__GetattrPrefix_RaiseIf(f"[raise_if__/{_reverse=}]met conditions ({source=}/{comment=})")

    def raise_if_not__(self, source: Any, comment: str = "") -> None | NoReturn:
        return self.raise_if__(source=source, _reverse=True, comment=comment)


# =====================================================================================================================
def _example():
    class GetattrPrefixInst_RaiseIf_data(GetattrPrefixInst_RaiseIf):
        ATTR0 = 0
        ATTR1 = 1
        def METH(self, arg1=1, arg2=2):
            return arg1 == arg2

    # ON ATTRIBUTE --------------------
    # apply prefix+item
    GetattrPrefixInst_RaiseIf_data().raise_if__attr0()  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__attr1()  # Exx__GetattrPrefix_RaiseIf

    # ON METH -------------------------
    # args - one
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(0)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2)  # Exx__GetattrPrefix_RaiseIf

    # args - several
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1,2)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2,2)  # Exx__GetattrPrefix_RaiseIf

    # kwargs
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2)  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2, arg2=2)  # Exx__GetattrPrefix_RaiseIf

    # send kwarg for PREFIX ----------
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2, comment="WRONG!")    # RAISE comment argument invalid for meth()!!!
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(1, arg2=2, COMMENT="CORRECT!")  # OK
    GetattrPrefixInst_RaiseIf_data().raise_if__meth(2, arg2=2, COMMENT="CORRECT!")  # Exx__GetattrPrefix_RaiseIf


# =====================================================================================================================
