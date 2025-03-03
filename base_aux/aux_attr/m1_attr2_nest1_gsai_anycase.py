from typing import *
from base_aux.aux_attr.m1_attr1_aux import AttrAux


# =====================================================================================================================
class NestGA_AttrIC:
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)


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
# class NestGSA_AttrAnycase(NestGA_AttrIC, NestSA_AttrAnycase):
#     # TODO: DEPRECATE!!! max depth recursion
#     pass


# =====================================================================================================================
class NestGI_AttrIC:
    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getitem(name)


# class NestSI_AttrAnycase:
#     # TODO: DEPRECATE!!! RecursionError ======================
#     def __setitem__(self, name, value) -> None | NoReturn:
#         return AttrAux(self).anycase__setitem(name, value)


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSI_AttrAnycase(NestGI_AttrIC, NestSI_AttrAnycase):
#     # TODO: DEPRECATE!!! RecursionError ======================
#     pass


# =====================================================================================================================
class NestGAI_AttrIC(NestGA_AttrIC, NestGI_AttrIC):
    pass


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSAI_AttrAnycase(NestGSA_AttrAnycase, NestGSI_AttrAnycase):
#     # TODO: DEPRECATE!!! RecursionError ======================
#     pass
#
#
# =====================================================================================================================
