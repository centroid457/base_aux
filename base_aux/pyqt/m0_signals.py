from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# =====================================================================================================================
class Base_Signals(QObject):
    """
    see tests for usage examples

    RULES_LINE
    -----
    1. try connect and emit it in other classes!
    2. PARAMS
        - use always exact params COUNT as DEFINED in signal
        - use always defined TYPE!
        in this way it will be clearly/direct/expected behaviour and this is only best way!!!
        other variants - could work unobvious and very unexpected (see tests as examples)!!!

    EXCEPTIONS
    ----------
    in PyQt you will not get an Exx! just stop the program!
    1. if your code stops on EMIT() - see the exact target! don't forget use mandatory params!
    """
    pass
    # TYPICAL SIGNALS
    # signal__finished = pyqtSignal()
    # signal__stop = pyqtSignal()
    # signal__send_value = pyqtSignal(int)
    # signal__send_values = pyqtSignal(int, int)


# =====================================================================================================================
