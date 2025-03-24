from typing import *

from base_aux.aux_attr.m1_annot_attr1_aux import AnnotsAllAux


# =====================================================================================================================
class NestGA_AnnotAttrIC:
    def __getattr__(self, name: str) -> Any | NoReturn:
        return AnnotsAllAux(self).gai_ic(name)


# class NestSA_AttrAnycase:
#     # TODO: DEPRECATE!!! RecursionError ======================
#           IF NEED SET ANYCASE - USE DIRECT AnnotAux(obj).set*
#           if apply this variant - you can solve recursion BIT it will never create not exists attr!!! - bad news!!!
#     def __setattr__(self, name, value) -> None | NoReturn:
#         if AttrAux(self).anycase__check_exists(name):
#             return AttrAux(self).anycase__setattr(name, value)
#         else:
#             raise AttributeError(f"{name=}")


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSA_AttrAnycase(NestGA_AnnotAttrIC, NestSA_AttrAnycase):
#     # TODO: DEPRECATE!!! max depth recursion
#     pass


# =====================================================================================================================
class NestGI_AnnotAttrIC:
    def __getitem__(self, name: str | int) -> Any | NoReturn:
        return AnnotsAllAux(self).gai_ic(name)


# class NestSI_AttrAnycase:
#     # TODO: DEPRECATE!!! RecursionError ======================
#     def __setitem__(self, name, value) -> None | NoReturn:
#         return AttrAux(self).anycase__setitem(name, value)


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSI_AttrAnycase(NestGI_AnnotAttrIC, NestSI_AttrAnycase):
#     # TODO: DEPRECATE!!! RecursionError ======================
#     pass


# =====================================================================================================================
class NestGAI_AnnotAttrIC(NestGA_AnnotAttrIC, NestGI_AnnotAttrIC):
    pass


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSAI_AttrAnycase(NestGSA_AttrAnycase, NestGSI_AttrAnycase):
#     # TODO: DEPRECATE!!! RecursionError ======================
#     pass
#
#
# =====================================================================================================================
