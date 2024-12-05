from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# =====================================================================================================================
# original names is not enough soft and comfortable for eyes!
# try to use ROUND NUMBERS!!! start use 0/100/200/255!!!
class COLOR_TUPLE_RGB:
    LIGHT_RED: tuple[int, int, int] = (255, 200, 200)
    LIGHT_GREEN: tuple[int, int, int] = (200, 255, 200)
    LIGHT_BLUE: tuple[int, int, int] = (200, 200, 255)
    LIGHT_YELLOW: tuple[int, int, int] = (255, 255, 100)
    LIGHT_GREY_240: tuple[int, int, int] = (240, 240, 240)   # #f2f2f2
    LIGHT_GREY_220: tuple[int, int, int] = (220, 220, 220)
    LIGHT_GREY_150: tuple[int, int, int] = (150, 150, 150)
    WHITE: tuple[int, int, int] = (255, 255, 255)


class MARGINS:
    _0000: QMargins = QMargins(0, 0, 0, 0)
    _5555: QMargins = QMargins(5, 5, 5, 5)
    _9595: QMargins = QMargins(9, 5, 9, 5)


class ALIGNMENT:
    T: Qt.Alignment = Qt.Alignment(Qt.AlignTop)
    TL: Qt.Alignment = Qt.Alignment(Qt.AlignTop | Qt.AlignLeft)
    TR: Qt.Alignment = Qt.Alignment(Qt.AlignTop | Qt.AlignRight)

    C: Qt.Alignment = Qt.Alignment(Qt.AlignVCenter | Qt.AlignHCenter)
    CH: Qt.Alignment = Qt.Alignment(Qt.AlignHCenter)
    CV: Qt.Alignment = Qt.Alignment(Qt.AlignVCenter)

    CT: Qt.Alignment = Qt.Alignment(Qt.AlignHCenter | Qt.AlignTop)
    CB: Qt.Alignment = Qt.Alignment(Qt.AlignHCenter | Qt.AlignBottom)
    CL: Qt.Alignment = Qt.Alignment(Qt.AlignVCenter | Qt.AlignLeft)
    CR: Qt.Alignment = Qt.Alignment(Qt.AlignVCenter | Qt.AlignRight)


# =====================================================================================================================
