from typing import *
import pathlib


# =====================================================================================================================
TYPE__PV_DICT = dict[str, Any]
TYPE__PATH = Union[str, pathlib.Path]
TYPE__VALUE = Union[str, NoReturn, None]


# =====================================================================================================================
class Exx__FileNotExists(Exception):
    """Any final exception when value can't be get.
    """


class Exx__SameKeys(Exception):
    """Same keys NOT allowed!
    """


# =====================================================================================================================
