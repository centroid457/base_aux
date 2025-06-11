from base_aux.aux_callable.m1_callable import *
from base_aux.aux_values.m2_types import *


# =====================================================================================================================
class Base_EqValid:
    """
    RULES
    -----
    1/ ALL not defined *ARGS/**KWARGS WHAT PASSED INTO INIT WOULD PASS INTO VALIDATOR() after other_final

    NOTE
    ----
    1/ preferably not use directly this object!
    USE DERIVATIVES!!! without validator passing

    2/ MAIN IDEA - NEVER RAISED!!! if any - return FALSE!!! if need - check manually!
    why so? - because i need smth to make a tests with final result of any source!
    dont mind reason!

    GOAL
    ----
    base object to make a validation by direct comparing with other object
    no raise

    USAGE
    -----
    for testing some other value with EqValidator
    1/ create validator object with exact params
    2/ use next operators for validating
        - EQ(eqObj == otherValue)
        - CONTAIN(otherValue in eqObj)
    No matter what eqObj is doing CONTAIN always will work!

    IF raised on any variant - pass to nest variant!

    USING TRICK (GOOD PRACTICE)
    ---------------------------
    any parameter could have exclude/skip variants with cmp by direct EQ operator for each value or IN operator for all values
    you can change logic by ising EqValid values instead of simple generics
    Example
        def dump_attrs(obj: Any, skip_names: list[str] = None):
            pass
            ...

        dump_attrs(Cls(), skip_names=["exit", call1, call2, call3])
        dump_attrs(Cls(), skip_names=["exit", EqValid_Startswith(call)])
    """
    VALIDATOR: TYPE__VALID_VALIDATOR    # DEFINE!!!

    V_ARGS: TYPING.ARGS_FINAL       # as variant for validation! can be blank!
    V_KWARGS: TYPING.KWARGS_FINAL   # as settings!

    # NOTE: use only one param! - IRESULT_REVERSE or IRESULT_CUMULATE!!!
    #   IRESULT_REVERSE - used for validation result!
    #   IRESULT_CUMULATE - used for cumulating ARGS validation results! - ignored FOR SINGLE result!
    #   DONT add REVERSE FinalResult! it intended in IRESULT_CUMULATE!!!
    IRESULT_REVERSE: bool = None
    IRESULT_CUMULATE: Enum_BoolCumulate = Enum_BoolCumulate.ALL_TRUE

    OTHER_FINAL__RESOLVE: bool = True   # goal: create chains with no ReCalculation inside
    OTHER_RAISED: bool = None   # RAISE ON CALCULATION OTHER_FINAL! not on equation!!!
    OTHER_FINAL: Any | Exception = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            *v_args,
            _validator: TYPE__VALID_VALIDATOR = None,
            _iresult_reverse: bool = None,
            _iresult_cumulate: Enum_BoolCumulate = None,
            _other_final__resolve: bool = None,
            **v_kwargs,
    ) -> None:
        """
        :param _validator: dont use! define in new class as attribute
        """
        if _validator is not None:
            self.VALIDATOR = _validator

        if _iresult_reverse is not None:
            self.IRESULT_REVERSE = _iresult_reverse

        if _iresult_cumulate is not None:
            self.IRESULT_CUMULATE = _iresult_cumulate

        if _other_final__resolve is not None:
            self.OTHER_FINAL__RESOLVE = _other_final__resolve

        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)
        self.V_ARGS = v_args
        self.V_KWARGS = v_kwargs

    def __str__(self):
        args = self.V_ARGS
        kwargs = self.V_KWARGS
        _iresult_reverse = self.IRESULT_REVERSE
        _iresult_cumulate = self.IRESULT_CUMULATE
        _other_final__resolve = self.OTHER_FINAL__RESOLVE
        return f"{self.__class__.__name__}({args=}/{kwargs=}/{_iresult_reverse=}/{_iresult_cumulate=}/{_other_final__resolve=})"

    def __repr__(self):
        return str(self)

    def VALIDATOR(self, other_final, *v_args, **v_kwargs) -> bool | NoReturn:
        return NotImplemented

    # DOUBT -----------------------------------------------------------------------------------------------------------
    def __iter__(self) -> Iterable[Any]:
        """
        NOTE
        ----
        not always correct!
        best usage for EqVariants or for any object with several args (Reqexp/...)

        # TODO: DEPRECATE??? - think no!!
        """
        yield from self.V_ARGS

    # PREPARES --------------------------------------------------------------------------------------------------------
    def other_final__resolve(self, other_draft: Any, *other_args, **other_kwargs) -> None:
        # TODO: decide use or not callable other??? = USE! it is really need to validate callable!!!
        if self.OTHER_FINAL__RESOLVE:
            try:
                self.OTHER_FINAL = CallableAux(other_draft).resolve_raise(*other_args, **other_kwargs)
                self.OTHER_RAISED = False
            except Exception as exx:
                self.OTHER_RAISED = True
                self.OTHER_FINAL = exx
        else:
            self.OTHER_FINAL = other_draft
            # self.OTHER_RAISED = False     # DONT PLACE HERE!!!

        self._chain_push_tail()

    def _chain_push_tail(self) -> None:
        """
        GOAL
        ---
        if object is CHAIN apply FinalValue from first chain without resolving in other chains!!!
        """
        for v_arg in self.V_ARGS:
            if isinstance(v_arg, Base_EqValid):
                v_arg.OTHER_FINAL__RESOLVE = False
                v_arg.OTHER_RAISED = self.OTHER_RAISED

    # VALIDATE-1=VALUE SINGLE -----------------------------------------------------------------------------------------
    def __eq__(self, other_draft) -> bool:
        return self.validate(other_draft)

    def __contains__(self, item) -> bool:
        return self.validate(item)

    # VALIDATE-2=VALUE with argsKwrgs----------------------------------------------------------------------------------
    def __call__(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        NOTE
        ----
        other_args/* - only for manual usage!
        typically used only other and only by direct eq(o1 == o2)
        """
        return self.validate(other_draft, *other_args, **other_kwargs)

    def validate(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # OTHER_FINAL --------------------
        self.other_final__resolve(other_draft, *other_args, **other_kwargs)

        # VALIDATION --------------------
        # 1=SINGLE
        if not self.V_ARGS:
            validator_result = CallableAux(self.VALIDATOR).resolve_bool(self.OTHER_FINAL, **self.V_KWARGS)
            if self.IRESULT_REVERSE:
                result = not validator_result
            else:
                result = validator_result
            return result

        else:
            for v_arg in self.V_ARGS:
                validator_result = CallableAux(self.VALIDATOR).resolve_bool(self.OTHER_FINAL, v_arg, **self.V_KWARGS)
                if self.IRESULT_REVERSE:
                    result = not validator_result
                else:
                    result = validator_result

                # CUMULATE --------
                if self.IRESULT_CUMULATE == Enum_BoolCumulate.ALL_TRUE:
                    if not result:
                        return False
                elif self.IRESULT_CUMULATE == Enum_BoolCumulate.ANY_TRUE:
                    if result:
                        return True
                elif self.IRESULT_CUMULATE == Enum_BoolCumulate.ALL_FALSE:
                    if result:
                        return False
                elif self.IRESULT_CUMULATE == Enum_BoolCumulate.ANY_FALSE:
                    if not result:
                        return True

            # FINAL ------------
            if self.IRESULT_CUMULATE in [Enum_BoolCumulate.ALL_TRUE, Enum_BoolCumulate.ALL_FALSE]:
                return True
            else:
                return False


# =====================================================================================================================
