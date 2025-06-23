from base_aux.base_nest_dunders.m4_gsai_ic__annots import *
from base_aux.aux_eq.m2_eq_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrByKwArgs(NestGAI_AnnotAttrIC):     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
    TODO: delete nesting NestGAI_AnnotAttrIC!!! use it in LastNext class!

    NOTE
    ----
    1. for more understanding application/logic use annots at first place! and dont mess them. keep your code clear!
        class Cls(NestInit_AnnotsAttrByKwArgs):
            A1: Any
            A2: Any
            A3: Any = 1
            A4: Any = 1

    2. mutable values are acceptable!!!

    GOAL
    ----
    init annots/attrs by params in __init__

    LOGIC
    -----
    ARGS
        - used for ANNOTS ONLY - used as values! not names!
        - inited first without Kwargs sense
        - if args less then annots - no matter
        - if args more then annots - no matter+no exx
        - if kwargs use same keys - it will overwrite by kwargs (args set first)
    KWARGS
        - used for both annots/attrs (annots see first)
        - if not existed in Annots and Attrs - create new!
    """
    def __init__(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        AttrAux_AnnotsAll(self).reinit__mutable_values()  # keep on first step!!! reinit only defaults from classvalues!
        AttrAux_AnnotsAll(self).sai__by_args_kwargs(*args, **kwargs)
        AttrAux_AnnotsAll(self).annots__check_all_defined_or_raise()    # fixme: is it really need? i think yes! use default values for noRaise!


# ---------------------------------------------------------------------------------------------------------------------
# class NestInit_AnnotsAttrByKwArgsIc(NestInit_AnnotsAttrByKwArgs, NestGSAI_AttrAnycase):   # IC - IS NOT WORKING!!!
#     """
#     SAME AS - 1=parent
#     -------
#     but attrs access will be IgnoreCased
#     """
#     pass


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
