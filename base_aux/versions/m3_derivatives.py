from typing import *
import sys

from base_aux.versions.m2_version import *


# =====================================================================================================================
class Version_Python(Version):
    """
    GOAL
    ----
    version of python interpreter
    """
    SOURCE = sys.version.split()[0]


# =====================================================================================================================
