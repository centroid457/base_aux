from typing import *

from .m2_annot1_aux import AnnotAttrAux


# =====================================================================================================================
class NestGI_AnnotIC:
    def __getitem__(self, name_index: str | int) -> Any | NoReturn:
        return AnnotAttrAux(self).gai_ic(name_index)


# =====================================================================================================================
