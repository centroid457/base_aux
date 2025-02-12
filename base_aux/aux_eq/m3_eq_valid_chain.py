from base_aux.aux_eq.m2_eq_valid3_derivatives import *
from base_aux.aux_eq.m2_eq_valid1_base import EqValid_Base
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
@final
class EqValidChain(EqValid_Base):
    V_ARGS: tuple[EqValid_Base, ...]
    V_KWARGS: TYPING.KWARGS_FINAL    # TODO: add params for AllTrue/Any*/False*

    def validate(self, other_draft: Any) -> bool:
        other_final = other_draft

        for eq_i in self.V_ARGS:
            if eq_i != other_final:
                return False

            other_final = eq_i.OTHER_FINAL

        return True


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
