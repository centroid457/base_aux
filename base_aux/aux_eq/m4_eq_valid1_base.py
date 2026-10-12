from base_aux.base_types.m0_static_typing import *
from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_eq.m3_eq_other1_resolved import *


_NO_VARIANT = object()


# ======================================================================================================================
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
    VALIDATOR: TYPING.VALID_VALIDATOR                   # reDEFINE!!!

    # FIXME: NAMES available: PATCH/MODIFIER/PREPARSE!!!
    MODIFIERS_TRY__DEF: TYPING.MODIFIERS_TRY__DRAFT = None   # FINAL MAIN MODIFIER!!!
    modifiers_try: TYPING.MODIFIERS_TRY__FINAL

    CUMULATE_MODE: EnumAdj_BoolCumulate = EnumAdj_BoolCumulate.ALL_TRUE

    v_args: TYPING.ARGS_FINAL       # as variant for validation! can be blank!
    v_kwargs: TYPING.KWARGS_FINAL   # as settings!

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            *v_args,
            _cumulate_mode: EnumAdj_BoolCumulate = None,
            _modifiers_pre: TYPING.MODIFIERS_TRY__DRAFT = None,
            **v_kwargs,
    ) -> None:
        # CUMULATE  ---------------------------
        if _cumulate_mode is not None:
            self.CUMULATE_MODE = _cumulate_mode

        # MODIFIERS ---------------------------
        self.modifiers_try = []

        if _modifiers_pre:
            if callable(_modifiers_pre):
                self.modifiers_try.append(_modifiers_pre)
            elif isinstance(_modifiers_pre, (list, tuple, set)):
                for item in _modifiers_pre:
                    if not callable(item):
                        msg = f"Incorrect type usage {item=}/{_modifiers_pre=}"
                        raise Exception(msg)
                    self.modifiers_try.append(item)
            else:
                raise Exception(f"incorrect type {_modifiers_pre=}/{type(_modifiers_pre)=}")

        if self.MODIFIERS_TRY__DEF:
            if callable(self.MODIFIERS_TRY__DEF):
                self.modifiers_try.append(self.MODIFIERS_TRY__DEF)
            elif isinstance(self.MODIFIERS_TRY__DEF, (list, tuple, set)):
                for item in self.MODIFIERS_TRY__DEF:
                    if not callable(item):
                        msg = f"Incorrect type usage {item=}/{self.MODIFIERS_TRY__DEF=}"
                        raise Exception(msg)
                    self.modifiers_try.append(item)

        # ARGS/KWARGS -------------------------
        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)
        self.v_args = v_args
        self.v_kwargs = v_kwargs

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        v_args = self.v_args
        v_kwargs = self.v_kwargs
        _cumulate_mode = self.CUMULATE_MODE
        return f"{self.__class__.__name__}({v_args=}/{v_kwargs=}/{_cumulate_mode=})"

    def __repr__(self):
        return str(self)

    def VALIDATOR(self, other_final, *v_args, **v_kwargs) -> bool | NoReturn:
        return NotImplemented

    # DOUBT ------------------------------------------------------------------------------------------------------------
    def __iter__(self) -> Iterable[Any]:
        """
        NOTE
        ----
        not always correct!
        best usage for EqVariants or for any object with several args (Reqexp/...)

        # TODO: DEPRECATE??? - think no!!
        """
        yield from self.v_args

    # VALIDATE-1=VALUE SINGLE ------------------------------------------------------------------------------------------
    def __eq__(self, other_draft) -> bool:
        return self.resolve(other_draft)

    def __contains__(self, item) -> bool:
        return self.resolve(item)

    # VALIDATE-2=VALUE with argsKwrgs-----------------------------------------------------------------------------------
    def resolve(self, other_draft: Any | OtherResolved) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # OTHER_FINAL --------------------
        other_resolved: OtherResolved = OtherResolved(other_draft, self.modifiers_try)

        # VALIDATE -----------------------
        for v_arg in (self.v_args or (_NO_VARIANT,)):
            try:
                if isinstance(v_arg, Base_EqValid):
                    # Передаем уже разрешенное значение вложенному валидатору
                    result = v_arg.resolve(other_resolved)
                elif v_arg is _NO_VARIANT:
                    # 1=ARGS BLANK --------------
                    result = bool(self.VALIDATOR(other_resolved, **self.v_kwargs))
                else:
                    # 2=ARGS one or MORE --------------
                    result = bool(self.VALIDATOR(other_resolved, v_arg, **self.v_kwargs))
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


# ======================================================================================================================
