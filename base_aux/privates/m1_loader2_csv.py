from typing import *
import re

from base_aux.privates.m0_static import *
from base_aux.privates.m1_loader0_base import *
from base_aux.privates.m1_loader6_derivatives import *


# =====================================================================================================================
class PrivateCsv(PrivateBase):
    """Get values from CSV file as dict format.

    this is not actually about private values!
    It was created for parsing stdout from CLI commands about device info,
    which is has data like

    skip all nonames.

    skip all lines with no separator.
        C:\\Users\\a.starichenko>STM32_Programmer_CLI --verbosity 1 --connect port=swd index=0
              -------------------------------------------------------------------
                               STM32CubeProgrammer v2.14.0
              -------------------------------------------------------------------

        ST-LINK SN  : 323609013212354D434B4E00
        ST-LINK FW  : V2J29S7
        Board       : --
        Voltage     : 3.26V
        SWD freq    : 4000 KHz
        Connect mode: Normal
        Reset mode  : Software reset
        Device ID   : 0x410
        Revision ID : Rev X
        Device name : STM32F101/F102/F103 Medium-density
        Flash size  : 128 KBytes (default)
        Device type : MCU
        Device CPU  : Cortex-M3
        BL Version  : --


        C:\\Users\\a.starichenko>
    """
    FILENAME = "pv.csv"
    SEPARATOR: str = ":"
    SPACE_IN_KEYS: str = "_"
    RAISE_SAME_KEYS: bool = True
    LINE_SKIP__FIRST: Optional[int] = None
    LINE_SKIP__LAST: Optional[int] = None
    LINE_SKIP__REGEXP: Optional[str] = None

    def get_dict(self) -> Union[TYPE__PV_DICT, NoReturn]:
        result = {}
        lines = self._text.splitlines()[self.LINE_SKIP__FIRST:]
        if self.LINE_SKIP__LAST:
            lines = lines[:-self.LINE_SKIP__LAST]

        for line in lines:
            if self.SEPARATOR not in line:
                continue
            if self.LINE_SKIP__REGEXP and re.search(pattern=self.LINE_SKIP__REGEXP, string=line):
                continue

            key, value = line.split(sep=self.SEPARATOR, maxsplit=1)
            key: str = key.strip()
            key = re.sub(pattern=r"\s", repl=self.SPACE_IN_KEYS, string=key)
            value: str = value.strip()

            if not key:
                continue

            if key in result and self.RAISE_SAME_KEYS:
                raise Exx__SameKeys

            result.update({key: value})

        return result


# =====================================================================================================================
class PrivateAuthCsv(PrivateAuth, PrivateCsv):
    pass


class PrivateTgBotAddressCsv(PrivateTgBotAddress, PrivateCsv):
    pass


# =====================================================================================================================
