from typing import *
from configparser import ConfigParser

from base_aux.privates.m0_static import *
from base_aux.privates.m0_base import *
from base_aux.privates.m6_derivative_base import *


# =====================================================================================================================
class PrivateIni(PrivateBase):
    """Get values from Ini file.
    Not recommended using DEFAULT SECTION!
    """
    FILENAME: str = "pv.ini"

    def get_dict(self) -> Union[TYPE__PV_DICT, NoReturn]:
        ini = ConfigParser()

        try:
            ini.read_string(self._text)
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            print(msg)
            raise exx

        if not self.SECTION or self.SECTION == "DEFAULT" or ini.has_section(section=self.SECTION):
            result = dict(ini[self.SECTION or "DEFAULT"])
            return result
        else:
            msg = f"[CRITICAL] NO [{self.SECTION=} in {self.filepath=}]\n"
            msg += self._text
            print(msg)


# =====================================================================================================================
class PrivateAuthIni(PrivateAuth, PrivateIni):
    pass


class PrivateTgBotAddressIni(PrivateTgBotAddress, PrivateIni):
    pass


# =====================================================================================================================
