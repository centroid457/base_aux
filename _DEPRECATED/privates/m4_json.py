from typing import *
import json

from base_aux.privates.m0_base import *
from base_aux.privates.m6_derivative_base import *


# =====================================================================================================================
class PrivateJson(PrivateBase):
    FILENAME: str = "pv.json"

    def get_dict(self) -> TYPING.KWARGS_FINAL | NoReturn:
        """
        section only in first level!
        """
        try:
            json_data = json.loads(self._text)
        except Exception as exc:
            msg = f"[CRITICAL] incorrect format file!\n{exc!r}"
            print(msg)
            raise exc

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
