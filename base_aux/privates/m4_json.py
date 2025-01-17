from typing import *
import json

from base_aux.privates.m0_base import *
from base_aux.privates.m6_derivatives import *


# =====================================================================================================================
class PrivateJson(PrivateBase):
    FILENAME: str = "pv.json"

    def get_dict(self) -> Union[TYPE__PV_DICT, NoReturn]:
        """
        section only in first level!
        """
        try:
            json_data = json.loads(self._text)
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            print(msg)
            raise exx

        if self.SECTION:
            json_data = json_data.get(self.SECTION)

        if json_data:
            return json_data
        else:
            msg = f"[CRITICAL] NO [{self.SECTION=} in {self.filepath=}]\n"
            msg += self._text
            print(msg)


# =====================================================================================================================
class PrivateAuthJson(PrivateAuth, PrivateJson):
    pass


class PrivateTgBotAddressJson(PrivateTgBotAddress, PrivateJson):
    pass


# =====================================================================================================================
