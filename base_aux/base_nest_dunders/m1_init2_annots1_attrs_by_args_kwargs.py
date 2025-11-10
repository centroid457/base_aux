from base_aux.aux_eq.m2_eq_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttr_ByArgs:
    def __init__(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        AttrAux_AnnotsAll(self).sai__by_args(*args)
        super().__init__(**kwargs)


# =====================================================================================================================
class NestInit_AnnotsAttr_ByKwargs:
    """
    SPECIALLY CREATED FOR
    ---------------------
    HtmlTagParser to init attrs only by kwargs
    """
    def __init__(self, *args: Any, **kwargs: TYPING.KWARGS_FINAL) -> None | NoReturn:
        AttrAux_AnnotsAll(self).sai__by_kwargs(**kwargs)
        super().__init__(*args)


# =====================================================================================================================
class NestInit_AnnotsAttr_ByArgsKwargs(NestInit_AnnotsAttr_ByArgs, NestInit_AnnotsAttr_ByKwargs):     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
    NOTE
    ----
    1. for more understanding application/logic use annots at first place! and dont mess them. keep your code clear!
        class Cls(NestInit_AnnotsAttr_ByArgsKwargs):
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
        - if args more then annots - no matter+no exc
        - if kwargs use same keys - it will overwrite by kwargs (args set first)
    KWARGS
        - used for both annots/attrs (annots see first)
        - if not existed in Annots and Attrs - create new!
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
# class NestInit_AnnotsAttrByKwArgsIc(NestInit_AnnotsAttr_ByArgsKwargs, NestGSAI_AttrAnycase):   # IC - IS NOT WORKING!!!
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
