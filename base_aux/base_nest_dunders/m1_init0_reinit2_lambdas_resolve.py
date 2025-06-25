from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class NestInit_AttrsLambdaResolve:
    """
    find and call all Lambda aux_attr On class inition
    GOAL
    ----
    if you need create object in classAttribute only on real inition of class
    useful in case of raising exx on init, but you want to pass instance in class attribute with inplace initiation

    REASON EXAMPLE
    --------------
    all class attributes will be calculated on import!
    class Cls:
        OK: int = int("1")
        # FAIL_ON_IMPORT: int = int("hello")    # ValueError: invalid literal for int() with base 10: 'hello'
        FAIL_ON_INIT: int = None

        def __init__(self, *args, **kwargs):
            if self.FAIL_ON_INIT is None:
                self.FAIL_ON_INIT = int("hello")    # this wount raise on import!

    Cls()   # ValueError: invalid literal for int() with base 10: 'hello'
    """

    def __init__(self, *args, **kwargs) -> None | NoReturn:
        for name in AttrAux_Existed(self).iter__names_filter__not_private():
            try:        # smtimes it isnot correct!!! some objects have many attrs Properties then could Raise!
                value = getattr(self, name)
            except:
                continue

            if isinstance(value, (Lambda, NestCall_Resolve)):
                setattr(self, name, value())

        super().__init__(*args, **kwargs)


# =====================================================================================================================
