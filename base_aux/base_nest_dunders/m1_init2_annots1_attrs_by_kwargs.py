from base_aux.aux_eq.m2_eq_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrByKwArgs:     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
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
        AttrAux_AnnotsAll(self).sai__by_args_kwargs(*args, **kwargs)
        super().__init__()


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
