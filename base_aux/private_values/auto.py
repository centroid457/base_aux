from typing import *

from . import *


# =====================================================================================================================
# TODO: add Csv???
class PrivateAuto(PrivateJson, PrivateIni, PrivateEnv):
    """This class will try all variants in order Json-Ini-Env.
    and take values ONLY from FIRST ONE source with all needed values!
    It will not merge sources!
    """
    def get_dict(self) -> Union[TYPE__PV_DICT, NoReturn]:
        annots = self.annots_get_set()
        annots_lower = set(map(str.lower, annots))

        for cls in [PrivateAuto, PrivateJson, PrivateIni, PrivateCsv]:
            try:
                self.FILENAME = super(cls, self).FILENAME
                self._filepath_apply_new()
                data = super(cls, self).get_dict()
                data_lower = set(map(str.lower, data))
                if data_lower.issuperset(annots_lower):
                    return data
            except:
                pass


# =====================================================================================================================
class PrivateAuthAuto(PrivateAuth, PrivateAuto):
    pass


class PrivateTgBotAddressAuto(PrivateTgBotAddress, PrivateAuto):
    pass


# =====================================================================================================================
