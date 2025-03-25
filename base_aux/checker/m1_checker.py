from typing import *
import platform

from base_aux.aux_types.m1_type_aux import *
from base_aux.base_statics.m2_exceptions import *
from base_aux.aux_attr.m1_annot_attr1_aux import *
from base_aux.aux_attr.m4_kits import *
from base_aux.aux_callable.m1_callable import *
from base_aux.base_statics.m1_types import *
from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.base_statics.m3_primitives import *


# =====================================================================================================================
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!


# =====================================================================================================================
class ValidAttrSource:
    _GETTER: Callable[..., Any] | Any = LambdaBool(LAMBDA_TRUE)
    _VALIDATOR: Lambda = LambdaBool(LAMBDA_TRUE)
    # A1: Lambda | ArgsKwargs | Any | Callable
    # A2: Lambda | ArgsKwargs | Any

    def __init__(self, validator = None, getter=None):
        if validator is not None:
            self._VALIDATOR = validator


# =====================================================================================================================
class ValidAttrAux(NestInit_Source):
    SOURCE: ValidAttrSource

    def check(self, value) -> AttrKit_Blank:
        result = {}

        for name in AttrAux(self.SOURCE).iter__names_not_hidden():
            value = getattr(self.SOURCE, name)

            try:
                if isinstance(value, Lambda):
                    value = value()
                elif isinstance(value, ArgsKwargs):
                    value = self.SOURCE._VALIDATOR.run(*ArgsKwargs.ARGS, **ArgsKwargs.KWARGS)
                else:
                    value = self.SOURCE._VALIDATOR.run(value)
            except Exception as exx:
                value = exx

            result.update({name: value})
        return AttrKit_Blank(**result)


# =====================================================================================================================
def _examples():
    class VictimSource(ValidAttrSource):
        _VALIDATOR: Lambda = Lambda(lambda: True)
        A1: Lambda | ArgsKwargs | Any = 123
        A2: Lambda | ArgsKwargs | Any = ArgsKwargs(123)
        A3: Lambda | ArgsKwargs | Any = Lambda(bool, 123)


    victim = ValidAttrAux(ValidAttrSource)


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
