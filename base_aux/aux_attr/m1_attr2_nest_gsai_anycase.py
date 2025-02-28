from typing import *
from base_aux.aux_attr.m1_attr1_aux import AttrAux


# =====================================================================================================================
class NestGA_AttrAnycase:
    def __getattr__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getattr(name)


# class NestSA_AttrAnycase:
#     # TODO: DEPRECATE!!! max depth recursion
#     def __setattr__(self, name, value) -> None | NoReturn:
#         return AttrAux(self).anycase__setattr(name, value)


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSA_AttrAnycase(NestGA_AttrAnycase, NestSA_AttrAnycase):
#     # TODO: DEPRECATE!!! max depth recursion
#     pass


# =====================================================================================================================
class NestGI_AttrAnycase:
    def __getitem__(self, name) -> Any | NoReturn:
        return AttrAux(self).anycase__getitem(name)


# class NestSI_AttrAnycase:
#     # TODO: DEPRECATE!!! max depth recursion
#     def __setitem__(self, name, value) -> None | NoReturn:
#         return AttrAux(self).anycase__setitem(name, value)


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSI_AttrAnycase(NestGI_AttrAnycase, NestSI_AttrAnycase):
#     # TODO: DEPRECATE!!! max depth recursion
#     pass


# =====================================================================================================================
class NestGAI_AttrAnycase(NestGA_AttrAnycase, NestGI_AttrAnycase):
    pass


# ---------------------------------------------------------------------------------------------------------------------
# class NestGSAI_AttrAnycase(NestGSA_AttrAnycase, NestGSI_AttrAnycase):
#     # TODO: DEPRECATE!!! max depth recursion
#     pass
#
#
# # =====================================================================================================================
