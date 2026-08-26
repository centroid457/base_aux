from base_aux.base_types.m0_static_typing import *
from base_aux.base_lambdas.m1_lambda import *


_NO_VARIANT = object()


# =====================================================================================================================
class Base_EqValid(NestCall_Resolve):
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
    VALIDATOR: TYPING.VALID_VALIDATOR    # DEFINE!!!

    V_ARGS: TYPING.ARGS_FINAL       # as variant for validation! can be blank!
    V_KWARGS: TYPING.KWARGS_FINAL   # as settings!

    CUMULATE_MODE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE

    OTHER_RESOLVE: bool = True   # goal: create chains with no ReCalculation inside
    OTHER_RAISED: bool = None   # RAISE ON CALCULATION OTHER_FINAL! not on equation!!!
    OTHER_FINAL: Any | Exception = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            *v_args,
            _validator: TYPING.VALID_VALIDATOR = None,
            _cumulate_mode: EnumAdj_BoolCumulate = None,
            _other_resolve: bool = None,
            # _other_druft: Any = None,     # DONT USE HERE! if need checking - create obj and use obj.validate(_other_druft)
            **v_kwargs,
    ) -> None:
        """
        :param _validator: dont use! define in new class as attribute
        """
        if _validator is not None:
            self.VALIDATOR = _validator

        if _cumulate_mode is not None:
            self.CUMULATE_MODE = _cumulate_mode

        if _other_resolve is not None:
            self.OTHER_RESOLVE = _other_resolve

        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)
        self.V_ARGS = v_args
        self.V_KWARGS = v_kwargs

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        v_args = self.V_ARGS
        v_kwargs = self.V_KWARGS
        _cumulate_mode = self.CUMULATE_MODE
        _other_resolve = self.OTHER_RESOLVE
        return f"{self.__class__.__name__}({v_args=}/{v_kwargs=}/{_cumulate_mode=}/{_other_resolve=})"

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
    def _other_resolve(self, other_draft: Any) -> None:
        # TODO: decide use or not callable other??? = USE! it is really need to validate callable!!!
        if self.OTHER_RESOLVE:
            try:
                self.OTHER_FINAL = Lambda(other_draft).resolve__raise()
                self.OTHER_RAISED = False
            except Exception as exc:
                self.OTHER_RAISED = True
                self.OTHER_FINAL = exc
        else:
            self.OTHER_FINAL = other_draft
            # self.OTHER_RAISED = False     # DONT PLACE HERE!!!

        self._other_final__push_chain()

    def _other_final__push_chain(self) -> None:
        """
        GOAL
        ---
        if object is CHAIN apply FinalValue from first chain without resolving in other chains!!!
        """
        for v_arg in self.V_ARGS:
            if isinstance(v_arg, Base_EqValid):
                v_arg.OTHER_RESOLVE = False
                v_arg.OTHER_RAISED = self.OTHER_RAISED

    # VALIDATE-1=VALUE SINGLE -----------------------------------------------------------------------------------------
    def __eq__(self, other_draft) -> bool:
        return self.resolve(other_draft)

    def __contains__(self, item) -> bool:
        return self.resolve(item)

    # VALIDATE-2=VALUE with argsKwrgs----------------------------------------------------------------------------------
    def resolve(self, other_draft: Any) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # OTHER_FINAL --------------------
        self._other_resolve(other_draft)

        # VALIDATE -----------------------
        for v_arg in (self.V_ARGS or (_NO_VARIANT,)):
            try:
                if v_arg is _NO_VARIANT:
                    # 1=ARGS BLANK --------------
                    result = bool(self.VALIDATOR(self.OTHER_FINAL, **self.V_KWARGS))
                else:
                    # 2=ARGS one or MORE --------------
                    result = bool(self.VALIDATOR(self.OTHER_FINAL, v_arg, **self.V_KWARGS))
            except Exception:
                result = False

            # CUMULATE --------
            if self.CUMULATE_MODE == EnumAdj_BoolCumulate.ALL_TRUE:
                if not result:
                    return False
            elif self.CUMULATE_MODE == EnumAdj_BoolCumulate.ANY_TRUE:
                if result:
                    return True
            elif self.CUMULATE_MODE == EnumAdj_BoolCumulate.ALL_FALSE:
                if result:
                    return False
            elif self.CUMULATE_MODE == EnumAdj_BoolCumulate.ANY_FALSE:
                if not result:
                    return True

        # FINAL - if not returned before ------------
        return self.CUMULATE_MODE in [EnumAdj_BoolCumulate.ALL_TRUE, EnumAdj_BoolCumulate.ALL_FALSE]


# =====================================================================================================================
