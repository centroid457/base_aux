import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from typing import *


# =====================================================================================================================
pass


# =====================================================================================================================
class Gui(QWidget):
    TITLE: str = "[GUI] Universal"
    _QAPP: QApplication = QApplication([])

    def __init__(self):
        super().__init__()

        self.wgt_create()
        self.wgt_main__apply_settings()
        self.slots_connect()

        # GUI SHOW ----------------------------------------------------------------------------------------------------
        self.show()
        exit_code = self._QAPP.exec_()
        if exit_code == 0:
            print(f"[OK]GUI({exit_code=})closed correctly")
        else:
            print(f"[FAIL]GUI({exit_code=})closed INCORRECTLY")
        sys.exit(exit_code)

    def wgt_main__apply_settings(self) -> None:
        # MAIN WINDOW -------------------------------------------------------------------------------------------------
        self.setWindowTitle(self.TITLE)

        self.setMinimumSize(300, 100)
        # self.setMinimumWidth(300)
        # self.setMinimumHeight(100)

        self.resize(300, 100)

    def wgt_create(self) -> None:
        # GRID --------------------------------------------------------------------------------------------------------
        layout_grid = QGridLayout()
        layout_grid.setSpacing(2)
        layout_grid.addWidget(QLabel("STLINK"), 0, 0)
        layout_grid.addWidget(QLabel("0"), 0, 1)
        layout_grid.addWidget(QLabel("1"), 0, 2)

        # START -------------------------------------------------------------------------------------------------------
        self.btn_start = QPushButton("START")
        self.btn_start.setCheckable(True)

        # layout ------------------------------------------------------------------------------------------------------
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_grid)
        layout_main.addWidget(self.btn_start)
        self.setLayout(layout_main)

    def slots_connect(self) -> None:
        self.btn_start.toggled.connect(self.btn_toggled)

    def btn_toggled(self, _state: Optional[bool] = None) -> None:
        print(f"btn {_state=}")


# =====================================================================================================================
if __name__ == '__main__':
    Gui()


# =====================================================================================================================
