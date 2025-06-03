from base_aux.aux_callable.m1_callable import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
class Base_EqValid:
    """
    MAIN IDEA
    ---------
    ALL WHAT PASSED INTO INIT WOULD PASS INTO VALIDATOR() AFTER FIRST ARG (OTHER)

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
    1/ create/select validator object
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

        dump_attrs(Cls(), skip_names=[exit, call1, call2, call3])
        dump_attrs(Cls(), skip_names=[exit, EqValid_Startswith(call)])
    """
    VALIDATOR: TYPE__VALID_VALIDATOR    # DEFINE!!!

    V_ARGS: TYPING.ARGS_FINAL
    V_KWARGS: TYPING.KWARGS_FINAL

    REVERSE: bool = None

    OTHER_RAISED: bool = None
    OTHER_FINAL: Any | Exception = None

    def __init__(self, *v_args, reverse: bool = None, **v_kwargs) -> None:
        if reverse is not None:
            self.REVERSE = reverse

        # super(ArgsKwargs, self).__init__(*v_args, **v_kwargs)
        self.V_ARGS = v_args
        self.V_KWARGS = v_kwargs

    def __str__(self):
        args = self.V_ARGS
        kwargs = self.V_KWARGS
        reverse = self.REVERSE
        return f"{self.__class__.__name__}({args=},{kwargs=},{reverse=})"

    def __repr__(self):
        """
        GOAL
        ----
        used in
        """
        return str(self)

    def __eq__(self, other_draft) -> bool:
        return self.validate(other_draft)

    def __call__(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        NOTE
        ----
        other_args/* - only for manual usage!
        typically used only other and only by direct eq(o1 == o2)
        """
        return self.validate(other_draft, *other_args, **other_kwargs)

    def __contains__(self, item) -> bool:
        return self.validate(item)

    def __iter__(self) -> Iterable[Any]:
        """
        NOTE
        ----
        not always correct!
        best usage for EqVariants or for any object with several args (Reqexp/...)
        """
        yield from self.V_ARGS

    def validate(self, other_draft: Any, *other_args, **other_kwargs) -> bool:
        """
        GOAL
        ----
        validate smth with special logic
        """
        # ------
        # TODO: decide use or not callable other??? = USE! it is really need to validate callable!!!
        try:
            self.OTHER_FINAL = CallableAux(other_draft).resolve_raise(*other_args, **other_kwargs)
            self.OTHER_RAISED = False
        except Exception as exx:
            self.OTHER_RAISED = True
            self.OTHER_FINAL = exx

        result = CallableAux(self.VALIDATOR).resolve_bool(self.OTHER_FINAL, *self.V_ARGS, **self.V_KWARGS)
        if self.REVERSE:
            result = not result
        return result

    def VALIDATOR(self, other_final, *v_args, **v_kwargs) -> bool | NoReturn:
        return NotImplemented


# =====================================================================================================================
