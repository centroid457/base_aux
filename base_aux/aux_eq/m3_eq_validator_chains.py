from typing import *

import re
from base_aux.aux_types.m0_primitives import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_source.m2_source_kwargs import *
from base_aux.aux_types.m0_types import TYPE__VALID_VALIDATOR
from base_aux.aux_callable.m1_callable_aux import *
from base_aux.aux_eq.m2_eq_validator import *


# =====================================================================================================================
@final
class EqValidChain(EqValid_Base):
    V_ARGS: Iterable[EqValid_Base]
    V_KWARGS: TYPE__KWARGS_FINAL

    def validate(self, other_draft: Any) -> bool:
        other_final = other_draft

        for eq_i in self.V_ARGS:
            if eq_i != other_final:
                return False

            other_final = eq_i.OTHER_RESULT

        return True


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
