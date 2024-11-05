from typing import *
import time

from .valid_0_aux import ValidAux

from base_aux.objects import TypeChecker
from base_aux.funcs import TYPE__ARGS, TYPE__KWARGS, args__ensure_tuple, TYPE__EXCEPTION, TYPE__SOURCE_LINK, ValueNotExist


# =====================================================================================================================
TYPE__VALIDATE_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[Any, ...], bool | NoReturn]]
TYPE__BOOL_LINK = Union[bool, Any, TYPE__EXCEPTION, Callable[[...], bool | NoReturn]]


# =====================================================================================================================
class Valid(ValidAux):
    """
    GOAL
    ----
    1. get value from somewhere and clearly validate it.
    2. ability to log result in appropriate way by using template-pattern for msg log

    CREATED SPECIALLY FOR
    ---------------------
    testplans sequences or same staff

    CONSTRAINTS
    -----------
    1. Exceptions
    any exception is a special state!
    so dont try to compare Exception with any real NoExx value or validate it in validator_link!
    if expect exception just place it directly in Validator!

    2. Callables
    only funcs/methods will be called
    if Class - no call! no init!

    3. VALIDATE
    if final value - it will be compared directly by compare_doublesided.
    So be careful about True (as default) and apply LAMBDA_BOOL(VALUE) if you need bool(val) comparing!

    BEST USAGE
    ----------

    WHY NOT: 1?
    -----------

    WHY NOT: 2?
    -----------
    """

    NAME: str = ""      # TODO: realise access to Valid from Chains!
    COMMENT: str = ""

    SKIP_LINK: TYPE__BOOL_LINK = None
    VALUE_LINK: TYPE__SOURCE_LINK
    VALIDATE_LINK: TYPE__VALIDATE_LINK = True
    VALIDATE_RETRY: int = 0
    REVERSE_LINK: TYPE__BOOL_LINK = None    # in case of REVERSE - REAL RESULT IS validate_last_bool!!!!

    ARGS__VALUE: TYPE__ARGS = ()
    ARGS__VALIDATE: TYPE__ARGS = ()
    KWARGS__VALUE: TYPE__KWARGS = None
    KWARGS__VALIDATE: TYPE__KWARGS = None

    # RESULT ACTUAL ------------------------------
    timestamp_last: float | None = None
    skip_last: bool = False
    finished: bool | None = None
    value_last: Any | Exception = None              # direct result value for calculating func value_link
    validate_last: None | bool | Exception = True   # direct result value for calculating func validate_link === decide using only bool???
    reverse_last: None | bool = None
    validate_last_bool: bool    # represented value for validation
    log_lines: list[str] = None

    # CHAINS -------------------------------------
    CHAIN__CUM: bool = True
    CHAIN__FAIL_STOP: bool = True

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            value_link: TYPE__SOURCE_LINK = ValueNotExist,
            validate_link: Optional[TYPE__VALIDATE_LINK] = None,
            validate_retry: Optional[int] = None,
            skip_link: Optional[TYPE__BOOL_LINK] = None,
            reverse_link: Optional[TYPE__BOOL_LINK] = None,

            args__value: TYPE__ARGS = (),
            args__validate: TYPE__ARGS = (),

            kwargs__value: TYPE__KWARGS = None,
            kwargs__validate: TYPE__KWARGS = None,

            name: Optional[str] = None,
            comment: Optional[str] = None,

            chain__cum: Optional[bool] = None,
            chain__fail_stop: Optional[bool] = None,
    ):
        """
        :param value_link: None - for cmp by eq/ne! other types - for direct usage
        :param validate_link:
        :param skip_link:
        :param args__value:
        :param args__validate:
        :param kwargs__value:
        :param kwargs__validate:
        :param name:
        :param comment:
        :param chain__cum:
        :param chain__fail_stop:
        """
        self.clear()

        self.VALUE_LINK = value_link

        if validate_link is not None:
            self.VALIDATE_LINK = validate_link
        if validate_retry is not None:
            self.VALIDATE_RETRY = validate_retry
        if reverse_link is not None:
            self.REVERSE_LINK = reverse_link
        if skip_link is not None:
            self.SKIP_LINK = skip_link

        # ARGS/KWARGS --------------------------------
        self.ARGS__VALUE = args__ensure_tuple(args__value)
        self.ARGS__VALIDATE = args__ensure_tuple(args__validate)

        self.KWARGS__VALUE = kwargs__value or {}
        self.KWARGS__VALIDATE = kwargs__validate or {}

        # INFO ---------------------------------------
        if name:
            self.NAME = name
        if comment:
            self.COMMENT = comment

        # CHAINS -------------------------------------
        if chain__cum is not None:
            self.CHAIN__CUM = chain__cum
        if chain__fail_stop is not None:
            self.CHAIN__FAIL_STOP = chain__fail_stop

    def clear(self):
        self.timestamp_last = None
        self.skip_last = False
        self.finished = None
        self.value_last = None
        self.validate_last = True
        self.log_lines = []

    @property
    def validate_last_bool(self) -> bool:
        """
        this is link name for bool(result)
        """
        return bool(self)

    def get_finished_result_or_none(self) -> None | bool:
        """
        GOAL
        ----
        attempt to make ability to get clear result by one check (for Gui)

        :return: if not finished - None
            if finished - validate_last_bool
        """
        if self.finished is None:
            return None
        else:
            return self.validate_last_bool

    def run__if_not_finished(self) -> bool:
        if not self.finished:
            return self.run()
        else:
            return bool(self)

    def run(self, value_link: Any = ValueNotExist) -> bool:
        """
        CONSTRAINTS
        -----------
        careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)

        :param value_link: BE CAREFUL created specially for value_link=ValueNotExist on init
        """
        if value_link == ValueNotExist:
            value_link = self.VALUE_LINK

        self.clear()
        self.timestamp_last = time.time()

        # SKIP ---------------------
        self.skip_last = self.get_result_bool(self.SKIP_LINK)

        if not self.skip_last:
            retry_count = 0
            # WORK =======================
            self.finished = False

            while True:
                self.clear()
                self.timestamp_last = time.time()

                # VALUE ---------------------
                self.value_last = self.get_result_or_exx(value_link, args=self.ARGS__VALUE, kwargs=self.KWARGS__VALUE)

                # VALIDATE ------------------
                if isinstance(self.value_last, Exception) and not TypeChecker.check__exception(self.VALIDATE_LINK):
                    self.validate_last = False

                elif TypeChecker.check__exception(self.VALIDATE_LINK):
                    self.validate_last = TypeChecker.check__nested__by_cls_or_inst(self.value_last, self.VALIDATE_LINK)

                elif TypeChecker.check__callable_func_meth_inst(self.VALIDATE_LINK):
                    args_validate = (self.value_last, *self.ARGS__VALIDATE)
                    self.validate_last = self.get_result_or_exx(self.VALIDATE_LINK, args=args_validate, kwargs=self.KWARGS__VALIDATE)

                else:
                    self.validate_last = self.compare_doublesided_or_exx(self.value_last, self.VALIDATE_LINK)

                # FINISH retry
                if not self.VALIDATE_RETRY or retry_count == self.VALIDATE_RETRY or self.validate_last_bool:
                    break
                else:
                    retry_count += 1

            if self.REVERSE_LINK:
                self.reverse_last = self.get_result_bool(self.REVERSE_LINK)

            self.finished = True
            # ============================

        # FINISH final ---------------------
        return self.validate_last_bool

    # def validate(self, value_link: Any = ValueNotExist) -> bool:

    def __bool__(self) -> bool:
        if not self.finished:
            return False

        if self.reverse_last:
            return self.validate_last != True       # dont use validate_last_bool!!! recursion!
        else:
            return self.validate_last == True

    def __str__(self) -> str:
        # main ---------------
        # # TODO: apply name from source!!! if not passed???
        # STR_PATTERN: str = (
        #     "{0.__class__.__name__}(validate_last_bool={0.validate_last_bool},validate_last={0.validate_last},\n"
        #     "...VALUE_LINK={0.VALUE_LINK},ARGS__VALUE={0.ARGS__VALUE},KWARGS__VALUE={0.KWARGS__VALUE},value_last={0.value_last},\n"
        #     "...VALIDATE_LINK={0.VALIDATE_LINK},ARGS__VALIDATE={0.ARGS__VALIDATE},KWARGS__VALIDATE={0.KWARGS__VALIDATE},\n"
        #     "...skip_last={0.skip_last},NAME={0.NAME},finished={0.finished},timestamp_last={0.timestamp_last})"
        # )
        # result_str = STR_PATTERN.format(self)

        # -------------------------------------
        result_str = f"{self.__class__.__name__}(NAME={self.NAME},skip_last={self.skip_last},validate_last_bool={self.validate_last_bool}"
        if self.reverse_last:
            result_str += f",reverse_last={self.reverse_last}"
        result_str += f",\n"

        # value ----
        result_str += f"...VALUE_LINK={self.VALUE_LINK}"
        if self.ARGS__VALUE:
            result_str += f",ARGS__VALUE={self.ARGS__VALUE}"
        if self.KWARGS__VALUE:
            result_str += f",KWARGS__VALUE={self.KWARGS__VALUE}"
        result_str += f",value_last={self.value_last},\n"

        # validate ----
        result_str += f"...VALIDATE_LINK={self.VALIDATE_LINK}"
        if self.ARGS__VALIDATE:
            result_str += f",ARGS__VALIDATE={self.ARGS__VALIDATE}"
        if self.KWARGS__VALIDATE:
            result_str += f",KWARGS__VALIDATE={self.KWARGS__VALIDATE}"

        result_str += f",validate_last={self.validate_last}"
        if self.REVERSE_LINK:
            result_str += f"*REVERSE_LINK={self.REVERSE_LINK}"
        result_str += f",\n"

        # finish ----
        result_str += f",finished={self.finished},timestamp_last={self.timestamp_last},"

        # log ----------------
        for index, line in enumerate(self.log_lines):
            result_str += "\n" + f"{index}:".rjust(5, '_') + line

        return result_str

    def __repr__(self) -> str:
        return str(self)

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other) -> bool:
        """
        GOAL
        ----
        use created object (with not defined value_link=None) as validator by EQ/NE inline methods!

        USAGE
        -----
        assert 1.0 >= 1
        assert float("1.0") >= 1
        assert "1.0" == Valid(validate_link=lambda x: float(x) >= 1)

        SPECIALLY CREATED FOR
        --------------------
        test uart devises by schema!

        assert "220.0V" == ValueUnit(...)
        assert "OFF" == ValueVariant("OFF", ["OFF", "ON"])
        assert "1.0" == Valid(validate_link=lambda x: float(x) >= 1)

        ValidTypeFloat = Valid(validate_link=lambda x: isinstance(x, float))
        assert "1.0" != ValidTypeFloat()
        assert 1.0 == ValidTypeFloat()
        """
        if self.VALUE_LINK == ValueNotExist:
            return self.run(other)
        else:
            # todo: maybe its not so good here/need ref? - seems OK!
            return self.run__if_not_finished() == other


# =====================================================================================================================
