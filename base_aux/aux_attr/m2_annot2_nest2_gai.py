from typing import *

from .m2_annot1_aux import AnnotAttrAux


# =====================================================================================================================
class NestGI_AnnotIC:
    def __getitem__(self, name_index: str | int) -> Any | NoReturn:
        # INDEX ----------
        try:
            index = int(name_index)
            return AnnotAttrAux(self).value_annot__get_by_index(index)
        except:
            pass








# =====================================================================================================================
