import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def info():
    QMessageBox.information(
        None,
        'О программе',
        'This is important information.'
    )


# =====================================================================================================================
if __name__ == '__main__':
    app = QApplication([])
    print(info())
    app.exec()


# =====================================================================================================================
