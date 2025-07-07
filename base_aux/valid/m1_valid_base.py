import datetime

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_argskwargs.m2_argskwargs_aux import *
from base_aux.aux_eq.m2_eq_aux import *
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
class Valid:
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


    ATTRS
    =====
    :ivar REVERSE_LINK:
    created specially for applying DRY in testplans - then PSU will not PowerOk on different HvIn
    """

    NAME: str = ""      # TODO: realise access to Valid from Chains!
    COMMENT: str = ""

    SKIP_LINK: TYPING.BOOL_DRAFT = None
    VALUE_LINK: TYPING.LAMBDA_DRAFT
    VALIDATE_LINK: TYPING__VALID_VALIDATOR = True
    VALIDATE_RETRY: int = 0
    REVERSE_LINK: TYPING.BOOL_DRAFT = None    # in case of REVERSE - REAL RESULT IS validate_last_bool!!! idea is validate_last have direct validationResult but reversing goes into validate_last_bool

    ARGS__VALUE: TYPING.ARGS_FINAL = ()
    ARGS__VALIDATE: TYPING.ARGS_FINAL = ()

    KWARGS__VALUE: TYPING.KWARGS_FINAL = None
    KWARGS__VALIDATE: TYPING.KWARGS_FINAL = None

    # RESULT ACTUAL ------------------------------
    timestamp_last: datetime.datetime | None = None
    skip_last: TYPING.RESULT__BOOL = False
    STATE_ACTIVE: EnumAdj_ProcessStateActive = EnumAdj_ProcessStateActive.NONE
    value_last: TYPING.RESULT__ANY_EXX = None               # direct result value for calculating func value_link
    validate_last: TYPING.RESULT__BOOL_EXX = True   # direct result value for calculating func validate_link === decide using only bool???
    reverse_last: TYPING.RESULT__BOOL = None
    validate_last_bool: TYPING.RESULT__BOOL         # represented value for validation
    log_lines: list[str] = None

    # CHAINS -------------------------------------
    CHAIN__CUM: bool = True
    CHAIN__FAIL_STOP: bool = True

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            value_link: TYPING.LAMBDA_DRAFT = NoValue,
            validate_link: Optional[TYPING__VALID_VALIDATOR] = None,
            validate_retry: Optional[int] = None,
            skip_link: TYPING.BOOL_DRAFT= None,
            reverse_link: TYPING.BOOL_DRAFT = None,

            args__value: TYPING.ARGS_DRAFT = (),
            args__validate: TYPING.ARGS_DRAFT = (),

            kwargs__value: TYPING.KWARGS_DRAFT = None,
            kwargs__validate: TYPING.KWARGS_DRAFT = None,

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
        self.ARGS__VALUE = ArgsKwargsAux(args__value).resolve_args()
        self.ARGS__VALIDATE = ArgsKwargsAux(args__validate).resolve_args()

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
        self.STATE_ACTIVE = EnumAdj_ProcessStateActive.NONE
        self.value_last = None
        self.validate_last = True
        self.log_lines = []

    def check__active(self) -> bool:
        return self.STATE_ACTIVE == EnumAdj_ProcessStateActive.STARTED

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
        if self.STATE_ACTIVE == EnumAdj_ProcessStateActive.FINISHED:
            return self.validate_last_bool
        else:
            return None

    def run__if_not_finished(self) -> bool:
        if self.STATE_ACTIVE == EnumAdj_ProcessStateActive.FINISHED:
            return bool(self)
        else:
            return self.run()

    def __call__(self, *args, **kwargs) -> bool:
        return self.run(*args, **kwargs)

    def run(self, value_link: Any = NoValue) -> bool:
        """
        CONSTRAINTS
        -----------
        careful about 1 comparing (assert 0 == False, assert 1 == True, assert 2 != True)

        :param value_link: BE CAREFUL created specially for value_link=NoValue on init
        """
        if value_link == NoValue:
            value_link = self.VALUE_LINK

        self.clear()

        # SKIP ---------------------
        self.skip_last = Lambda(self.SKIP_LINK).resolve__bool()

        if not self.skip_last:
            retry_count = 0
            # WORK =======================
            self.STATE_ACTIVE = EnumAdj_ProcessStateActive.STARTED

            while True:
                self.clear()
                self.timestamp_last = datetime.datetime.now()

                # VALUE ---------------------
                self.value_last = Lambda(value_link, *self.ARGS__VALUE, **self.KWARGS__VALUE).resolve__exx()

                # VALIDATE ------------------
                if isinstance(self.value_last, Exception) and not TypeAux(self.VALIDATE_LINK).check__exception():
                    self.validate_last = False

                elif TypeAux(self.VALIDATE_LINK).check__exception():
                    self.validate_last = TypeAux(self.value_last).check__nested__from_cls_or_inst(self.VALIDATE_LINK)

                elif TypeAux(self.VALIDATE_LINK).check__callable_func_meth_inst():
                    self.validate_last = Lambda(self.VALIDATE_LINK, self.value_last, *self.ARGS__VALIDATE, **self.KWARGS__VALIDATE).resolve__exx()

                else:
                    self.validate_last = EqAux(self.value_last).check_doubleside__exx(self.VALIDATE_LINK)

                # FINISH retry
                if not self.VALIDATE_RETRY or retry_count == self.VALIDATE_RETRY or self.validate_last_bool:
                    break
                else:
                    retry_count += 1

            if self.REVERSE_LINK:
                self.reverse_last = Lambda(self.REVERSE_LINK).resolve__bool()

            self.STATE_ACTIVE = EnumAdj_ProcessStateActive.FINISHED
            # ============================

        # FINISH final ---------------------
        return self.validate_last_bool

    # def validate(self, value_link: Any = NoValue) -> bool:

    def __bool__(self) -> bool:
        if self.skip_last:
            return True

        if self.STATE_ACTIVE != EnumAdj_ProcessStateActive.FINISHED:
            return False

        if self.reverse_last:
            return self.validate_last != True       # dont use validate_last_bool!!! recursion!
        else:
            return self.validate_last == True

    def get_logstr_attr(self, item: str, prefix: str = "", suffix: str = "", only_if_have_value: bool = None) -> str:
        """
        return at least blank line if no value
        """
        value = getattr(self, item)
        if value or not only_if_have_value:
            return f"{prefix}{item}={value}{suffix}"
        else:
            return ""

    def get_logstr_attr_if_have_value(self, item: str, prefix: str = "", suffix: str = "") -> str:
        return self.get_logstr_attr(item=item, prefix=prefix, suffix=suffix, only_if_have_value=True)

    def __str__(self) -> str:
        # main ---------------
        # # TODO: apply name from source!!! if not passed???
        # STR_PATTERN: str = (
        #     "{0.__class__.__name__}(validate_last_bool={0.validate_last_bool},validate_last={0.validate_last},\n"
        #     "...VALUE_LINK={0.VALUE_LINK},ARGS__VALUE={0.ARGS__VALUE},KWARGS__VALUE={0.KWARGS__VALUE},value_last={0.value_last},\n"
        #     "...VALIDATE_LINK={0.VALIDATE_LINK},ARGS__VALIDATE={0.ARGS__VALIDATE},KWARGS__VALIDATE={0.KWARGS__VALIDATE},\n"
        #     "...skip_last={0.skip_last},NAME={0.NAME},STATE_ACTIVE={0.STATE_ACTIVE},timestamp_last={0.timestamp_last})"
        # )
        # result_str = STR_PATTERN.format(self)

        # -------------------------------------
        result_str = f"{self.__class__.__name__}("
        result_str += self.get_logstr_attr_if_have_value("NAME")
        result_str += self.get_logstr_attr("validate_last_bool", prefix=",")
        result_str += f",\n"

        # VARIATIONS ----
        if self.SKIP_LINK:
            result_str += self.get_logstr_attr("SKIP_LINK", prefix="...")
            result_str += self.get_logstr_attr("skip_last", prefix=",")
            result_str += f",\n"

        if self.REVERSE_LINK:
            result_str += self.get_logstr_attr("REVERSE_LINK", prefix="...")
            result_str += self.get_logstr_attr("reverse_last", prefix=",")
            result_str += f",\n"

        # value ----
        result_str += self.get_logstr_attr("VALUE_LINK", prefix="...")
        result_str += self.get_logstr_attr_if_have_value("ARGS__VALUE", prefix=",")
        result_str += self.get_logstr_attr_if_have_value("KWARGS__VALUE", prefix=",")
        result_str += self.get_logstr_attr("value_last", prefix=",")
        result_str += f",\n"

        # validate ----
        result_str += self.get_logstr_attr("VALIDATE_LINK", prefix="...")
        result_str += self.get_logstr_attr_if_have_value("ARGS__VALIDATE", prefix=",")
        result_str += self.get_logstr_attr_if_have_value("KWARGS__VALIDATE", prefix=",")
        result_str += self.get_logstr_attr("validate_last", prefix=",")
        result_str += f",\n"

        # finish ----
        result_str += self.get_logstr_attr("STATE_ACTIVE", prefix="...")
        result_str += f",\n"
        result_str += self.get_logstr_attr("timestamp_last", prefix="...")

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
        if self.VALUE_LINK == NoValue:
            return self.run(other)
        else:
            # todo: maybe its not so good here/need ref? - seems OK!
            return self.run__if_not_finished() == other


# =====================================================================================================================
