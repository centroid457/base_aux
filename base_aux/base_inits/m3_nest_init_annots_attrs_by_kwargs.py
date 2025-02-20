from typing import *

from base_aux.aux_attr.m4_nest_eq_attrs import NestEq_Attrs
from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.aux_eq.m1_eq_aux import *


# =====================================================================================================================
class NestInit_AnnotsAttrsByKwArgs:     # NOTE: dont create AnnotsOnly/AttrsOnly! always use this class!
    """
    NOTE
    ----
    for more understanding application/logic use annots at first place! and dont mess them. keep your code clear!
        class Cls(NestInit_AnnotsAttrsByKwArgs):
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
        AnnotsAux(self).set_values__by_args_kwargs(*args, **kwargs)
        AnnotsAux(self).check_all_defined_or_raise()    # fixme: is it really need? i think yes! use default values for noRaise!


# ---------------------------------------------------------------------------------------------------------------------
class NestInit_AnnotsAttrByKwArgsIC(NestInit_AnnotsAttrsByKwArgs, NestGSAI_AttrAnycase):
    """
    SAME AS - 1=parent
    -------
    but attrs access will be IgnoreCased
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
def examples__NestInit():
    class Example(NestInit_AnnotsAttrsByKwArgs):
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


# ---------------------------------------------------------------------------------------------------------------------
@final
class Init_AnnotsAttrsByKwArgs(NestInit_AnnotsAttrsByKwArgs, NestEq_Attrs):
    """
    GOAL
    ----
    1/ generate object with exact attrs values by Kwargs like template
    2/ for further comparing by Eq
    3/ all callables will resolve as Exx

    NOTE
    ----
    IgnoreCase applied!

    SAME AS - NestInit_AnnotsAttrsByKwArgs
    --------------------------------------
    but
        - used as final
        - args useless

    WHY NOT - just EqValid_*
    ------------------------
    1/ cause you will not keep simple direct object with attrs!
    2/ EqValid_* will be created! further!

    MAYBE
    -----
    need rename just for Attrs*!?
    """
    # DONT ADD ANY NOT HIDDEN ATTRS!!!!


# ---------------------------------------------------------------------------------------------------------------------
def examples__Init():
    class Example:
        A0: Any
        A1: Any = 1

    assert Init_AnnotsAttrsByKwArgs(a1=1) == Example()
    assert Init_AnnotsAttrsByKwArgs(a1=11) != Example()

    assert Init_AnnotsAttrsByKwArgs(a0=1) != Example()


# =====================================================================================================================
if __name__ == '__main__':
    examples__Init()


# =====================================================================================================================
