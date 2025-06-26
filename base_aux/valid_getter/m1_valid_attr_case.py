import platform

from base_aux.base_lambdas.m1_lambda import *

from base_aux.aux_eq.m3_eq_valid1_base import *
from base_aux.aux_eq.m3_eq_valid3_derivatives import *
from base_aux.base_nest_dunders.m4_gsai_ic__annots import *

from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_types.m0_static_types import *
from base_aux.base_types.m0_static_typing import *


# =====================================================================================================================
# FIXME: FINISH! its just a zero start - not working!!!

class Base_ValidAccepts:
    OTHER_DRAFT: Any | Callable = True
    EQ_VARIANTS: dict[str, Any | Base_EqValid] = {}
    EQ_ACCEPTS: dict[str, bool | None] = {}

    def __init__(self, other_draft: Any = NoValue, **eq_variants: Any | Base_EqValid) -> None:
        if other_draft is not NoValue:
            self.OTHER_DRAFT = other_draft

        if eq_variants:
            self.EQ_VARIANTS = eq_variants

    # -----------------------------------------------------------------------------------------------------------------
    def raise_if__accepts_fail(self, **eq_accepts: bool | None) -> None | NoReturn:
        eq_accepts = {key.lower(): value for key, value in {**self.EQ_ACCEPTS, **eq_accepts}.items()}
        for name, accept in eq_accepts.items():
            if accept is not None:
                validate = self.OTHER_DRAFT == self.EQ_VARIANTS[name]
                result = accept and validate
                if not result:
                    msg = f"{name=}/{accept=}/{validate=}"
                    raise Exx__ValueNotValidated(msg)

    def bool_if__accepts_meet(self, **accepts: bool | None) -> bool | NoReturn:
        try:
            self.raise_if__accepts_fail(**accepts)
            return True
        except Exx__ValueNotValidated:
            return False
        except Exception as exx:
            raise exx


# # =====================================================================================================================
# class ValidAccepts_OS(Base_ValidAccepts):
#     OTHER_DRAFT: Any = platform.system
#
#     LINUX: Union[Base_EqValid, bool] = EqValid_EQ_StrIc("LINUX")
#     WINDOWS: Union[Base_EqValid, bool] = EqValid_EQ_StrIc("WINDOWS")
#
#
# # =====================================================================================================================
# # if __name__ == "__main__":
# #     assert ValidAccepts_OS("liNUX", linux=True).bool_if__accepts_meet()
#
#
# # =====================================================================================================================
# @pytest.mark.parametrize(
#     argnames="cls, _EXPECTED",
#     argvalues=[
#         # (Base_ValidAccepts, set()),
#         (ValidAccepts_OS, {"LINUX", "WINDOWS"}),
#     ]
# )
# def test__items_eq(cls, _EXPECTED):
#     Lambda(set(cls().items_eq())).expect__check_assert(_EXPECTED)
#
#
# # =====================================================================================================================
