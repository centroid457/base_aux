from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import *


# =====================================================================================================================
class NestIter_AttrNameValueNotPrivate:
    def __iter__(self) -> tuple[str, Any]:
        for name in AttrAux(self).iter__names_filter__not_private():
            value = getattr(self, name)
            yield name, value


# ---------------------------------------------------------------------------------------------------------------------
class NestIter_AttrNameValueNotHidden:
    def __iter__(self) -> tuple[str, Any]:
        for name in AttrAux(self).iter__names_filter__not_hidden():
            value = getattr(self, name)
            yield name, value


# =====================================================================================================================
class NestIter_AnnotNameValueNotPrivate:
    """
    SPECIALLY CREATED FOR
    ---------------------
    MsgStruct
    """
    def __iter__(self) -> tuple[str, Any]:
        for name in AnnotsAllAux(self).iter__names_filter__not_private():
            value = getattr(self, name)
            yield name, value


# ---------------------------------------------------------------------------------------------------------------------
class NestIter_AnnotNameValueNotHidden:
    def __iter__(self) -> tuple[str, Any]:
        for name in AnnotsAllAux(self).iter__names_filter__not_hidden():
            value = getattr(self, name)
            yield name, value


# =====================================================================================================================
def _examples() -> None:
    class Victim(NestIter_AttrNameValueNotPrivate):
        A0: int
        A1: int = 1

    victim = Victim()
    for name, value in victim:
        print(name, value)


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
