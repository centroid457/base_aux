from typing import *

from base_aux.objects import TypeChecker
from base_aux.funcs import *


# =====================================================================================================================
class ValidAux:
    """
    Try to keep all validating funcs in separated place
    """
    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_or_raise(
            cls,
            source: TYPE__VALID_SOURCE,
            *args: TYPE__VALID_ARGS,
            **kwargs: TYPE__VALID_KWARGS,
    ) -> Any | NoReturn:
        """
        SPECIFIC LOGIC
        --------------
        if callable meth/func - call and return result.
        else - return source.

        GOAL
        ----
        get common expected for any python code result - simple calculate or raise!
        because of get_result_or_exx is not enough!

        CREATED SPECIALLY FOR
        ---------------------
        GetattrPrefixInst
        """
        if TypeChecker.check__callable_func_meth_inst(source):
            result = source(*args, **kwargs)
        else:
            result = source
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_or_exx(
            cls,
            source: TYPE__VALID_SOURCE,
            *args: TYPE__VALID_ARGS,
            **kwargs: TYPE__VALID_KWARGS,
    ) -> Any | Exception:
        """
        GOAL
        ----
        same as get_result_or_raise but
        attempt to simplify result by not using try-sentence.
        so if get raise in get_result_or_raise - return Exx object

        USEFUL IDEA
        -----------
        1. in gui when its enough to get str() on result and see the result
        """
        args = (source, *args)
        try:
            result = cls.get_result_or_raise(*args, **kwargs)
        except Exception as exx:
            result = exx
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_result_bool(
            cls,
            source: TYPE__VALID_SOURCE,
            *args: TYPE__VALID_ARGS,
            **kwargs: TYPE__VALID_KWARGS,
    ) -> bool:
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
            result = cls.get_result_or_raise(source, *args, **kwargs)
            if TypeChecker.check__exception(result):
                return False
            return bool(result)
        except:
            return False

    # =================================================================================================================
    @classmethod
    def eq_doublesided_or_exx(cls, obj1: Any, obj2: Any, return_bool: bool = None) -> bool | Exception:
        """
        GOAL
        ----
        just a direct comparing code like
            self.validate_last = self.value_last == self.VALIDATE_LINK or self.VALIDATE_LINK == self.value_last
        will not work correctly

        if any result is True - return True.
        if at least one false - return False
        if both exx - return first exx  # todo: deside return False in here!

        CREATED SPECIALLY FOR
        ---------------------
        manipulate objects which have special methods for __cmp__
        for cases when we can switch places

        BEST USAGE
        ----------
            class ClsEq:
                def __init__(self, val):
                    self.VAL = val

                def __eq__(self, other):
                    return other == self.VAL

            assert ClsEq(1) == 1
            assert 1 == ClsEq(1)

            assert compare_doublesided(1, Cls(1)) is True
            assert compare_doublesided(Cls(1), 1) is True

        example above is not clear! cause of comparison works ok if any of object has __eq__() meth even on second place!
        but i think in one case i get Exx and with switching i get correct result!!! (maybe fake! need explore!)
        """
        try:
            result12 = obj1 == obj2
            if result12:
                return True
        except Exception as exx:
            result12 = exx

        try:
            result21 = obj2 == obj1
            if result21:
                return True
        except Exception as exx:
            result21 = exx

        try:
            result3 = obj2 is obj1
            if result3:
                return True
        except Exception as exx:
            result3 = exx
            pass

        if False in [result12, result21] or return_bool:
            return False
        else:
            return result12

    @classmethod
    def eq_doublesided__bool(cls, obj1: Any, obj2: Any) -> bool:
        """
        same as compare_doublesided_or_exx but
        in case of Exx - return False

        CREATED SPECIALLY FOR
        ---------------------
        Valid.value_validate
        """
        return cls.eq_doublesided_or_exx(obj1, obj2, return_bool=True)

    @classmethod
    def eq_doublesided__reverse(cls, obj1: Any, obj2: Any) -> bool:
        """
        just reverse result for compare_doublesided__bool
        so never get Exx, only bool
        """
        return cls.eq_doublesided__bool(obj1, obj2) is not True

    # =================================================================================================================
    @staticmethod
    def ltgt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        """
        NOTE
        ----
        1. important to keep source at first place!
        """
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def ltge(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source > low
        if high is not None:
            result &= source <= high
        return result

    @staticmethod
    def legt(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source < high
        return result

    @staticmethod
    def lege(source: Any, low: Any | None = None, high: Any | None = None) -> bool | Exception:
        result = True
        if low is not None:
            result &= source >= low
        if high is not None:
            result &= source <= high
        return result


# =====================================================================================================================
