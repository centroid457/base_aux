from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .base import Data_


# =====================================================================================================================
class HeaderViewCB(QHeaderView):
    """
    THIS IS THE ONLY WAY TO PUT CHECKBOXES INTO HEADER!

    work as additional to tableModel!
    this is always exists in TV as default! but we can change some behaviour!
    """
    # SIGNALS ---------------------------------------------
    signal__state_changed = pyqtSignal(list)
    sectionCountChanged: pyqtSignal
    sectionClicked: pyqtSignal
    sectionDoubleClicked: pyqtSignal
    sectionPressed: pyqtSignal
    sectionEntered: pyqtSignal
    sectionMoved: pyqtSignal
    geometriesChanged: pyqtSignal

    # ORIGINAL ---------------------------------------------
    setSectionHidden: Callable  # (logicalIndex, hide)
    setSectionsMovable: Callable  # (movable)
    setVisible: Callable  # (visible)
    resizeSection: Callable  # (logicalIndex, size)

    # NEW --------------------------------------------------
    DATA: Data_ = None

    def __init__(self, data: Data_, orientation=Qt.Horizontal, parent=None):
        self.DATA = data
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.sectionClicked.connect(self.on_sectionClicked)

    def count(self):
        return len(self.DATA.DEVS)

    # def mouseDoubleClickEvent(self, e, QMouseEvent=None): # real signature unknown; restored from __doc__
    #     """ mouseDoubleClickEvent(self, e: Optional[QMouseEvent]) """
    #     pass

    # def mousePressEvent(self, e, QMouseEvent=None):
    #     """ mousePressEvent(self, e: Optional[QMouseEvent]) """
    #     pass

    def paintSection(self, painter: Optional[QPainter], rect: QRect, logicalIndex: int) -> None:
        painter.save()
        QHeaderView.paintSection(self, painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex > 0:
            option = QStyleOptionButton()
            # option.initFrom(self)             # not necessary
            # option.iconSize = QSize(10, 10)   # not necessary

            # var1=чекбокс позиционирование -------------------------
            # option.rect = rect  # center
            # option.rect = QRect(10, 10, 10, 10)
            # option.rect = QRect(rect.left(), 0, 20, 20)
            option.rect = QRect(rect.left(), rect.top(), 20, 20)

            dut = self.DATA.DEVS[logicalIndex - 1]
            if not dut.SKIP:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, option, painter)

    def on_sectionClicked(self, index: int) -> None:
        if index > 0:
            dut = self.DATA.DEVS[index - 1]
            dut.SKIP_reverse()
            # self.TM._data_reread()    # DONT NEED!!!!


# =====================================================================================================================
