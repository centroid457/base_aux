from base_aux.aux_attr.m4_kits import *
from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_argskwargs.m1_argskwargs import *
from base_aux.aux_values.m4_primitives import *


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
class ValidAttr:
    _VALIDATOR: Lambda = LambdaBool(LAMBDA_TRUE)
    # A1: Lambda | ArgsKwargs | Any | Callable
    # A2: Lambda | ArgsKwargs | Any

    def __init__(self, validator = None):
        if validator is not None:
            self._VALIDATOR = validator

    def check(self, value: Callable[..., Any] | Any) -> AttrKit_Blank:
        value = CallableAux(value).resolve_exx()

        result = {}

        for name in AnnotsLastAux(self).iter__names_filter__not_hidden():
            attr_value = getattr(self, name)

            try:
                if isinstance(attr_value, Lambda):
                    result_validate = attr_value(value)
                elif isinstance(attr_value, ArgsKwargs):
                    result_validate = self._VALIDATOR.run(value, *ArgsKwargs.ARGS, **ArgsKwargs.KWARGS)
                else:   # Any
                    result_validate = attr_value == value
            except Exception as exx:
                result_validate = exx

            result.update({name: result_validate})
        return AttrKit_Blank(**result)


# =====================================================================================================================
def _examples():
    class Victim(ValidAttr):
        _VALIDATOR: Lambda = Lambda(lambda param: param == 111)
        A1: Lambda | ArgsKwargs | Any = 111
        A2: Lambda | ArgsKwargs | Any = 222
        # A2: Lambda | ArgsKwargs | Any = ArgsKwargs(111)
        # A3: Lambda | ArgsKwargs | Any = Lambda(True)

    victim = Victim()
    assert victim.check(111)


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
