from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.aux_attr.m1_attr2_nest1_gsai_anycase import *
from base_aux.aux_cmp_eq.m2_eq_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrByKwArgs(NestGAI_AttrIC):     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
    NOTE
    ----
    for more understanding application/logic use annots at first place! and dont mess them. keep your code clear!
        class Cls(NestInit_AnnotsAttrByKwArgs):
            A1: Any
            A2: Any
            A3: Any = 1
            A4: Any = 1

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
        AnnotsAux(self).set_annots_attrs__by_args_kwargs(*args, **kwargs)
        AnnotsAux(self).check_all_defined_or_raise()    # fixme: is it really need? i think yes! use default values for noRaise!


# ---------------------------------------------------------------------------------------------------------------------
# class NestInit_AnnotsAttrByKwArgsIc(NestInit_AnnotsAttrByKwArgs, NestGSAI_AttrAnycase):   # IC - IS NOT WORKING!!!
#     """
#     SAME AS - 1=parent
#     -------
#     but attrs access will be IgnoreCased
#     """
#     pass


# ---------------------------------------------------------------------------------------------------------------------
def examples__NestInit():
    class Example(NestInit_AnnotsAttrByKwArgs):
        A1: Any
        A2: Any = None
        A3 = None

    try:
        Example()
        assert False
    except:
        assert True

    assert Example(a1=1).A1 == 1
    assert Example(1, a1=2).A1 == 2

    assert Example(1).A1 == 1
    assert Example(1).A2 == None
    assert Example(1).A3 == None

    assert Example(1, 1, 1).A1 == 1
    assert Example(1, 1, 1).A2 == 1
    assert Example(1, 1, 1).A3 == None
    assert Example(1, 1, a3=1).A3 == 1


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
