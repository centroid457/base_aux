from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from base_aux.pyqt.m1_dialog import Dialogs


# SET ============================================================================================================
class DialogsTp(Dialogs):
    @classmethod
    def info__about(cls, *args) -> int:
        wgt = QMessageBox()
        if not cls._apply_new__or_activate_last(name="info__about", wgt=wgt):
            return 1024
        wgt.setMaximumWidth(1000)
        answer = wgt.information(
            None,
            "О программе",
            (
                "LLC,\n"
                "Программа проведения тестирования"
             )
        )
        # return always 1024
        return answer

    @classmethod
    def finished__devs_detection(cls, *args) -> int:
        wgt = QMessageBox()
        if not cls._apply_new__or_activate_last(name="finished__devs_detection", wgt=wgt):
            return 1024
        wgt.resize(1000, 1000)
        wgt.setBaseSize(1000, 1000)
        answer = wgt.information(
            None,
            "Определение устройств",
            (
                "Процесс завершен" + " "*30
            )
        )
        # return always 1024
        return answer

    @classmethod
    def finished__tp(cls, *args) -> int:
        wgt = QMessageBox()
        if not cls._apply_new__or_activate_last(name="finished__tp", wgt=wgt):
            return 1024
        answer = wgt.information(
            None,
            "Тестирование",
            (
                "Процесс завершен"
             )
        )
        # return always 1024
        return answer

    @classmethod
    def finished__save(cls, *args) -> int:
        wgt = QMessageBox()
        if not cls._apply_new__or_activate_last(name="finished__save", wgt=wgt):
            return 1024
        answer = wgt.information(
            None,
            "Сохранение",
            (
                "Процесс завершен"
             )
        )
        # return always 1024
        return answer


# =====================================================================================================================
if __name__ == '__main__':
    # DialogsTp.info__about()
    DialogsTp.finished__devs_detection()
    # DialogsTp.finished__tp()
    # DialogsTp.finished__save()


# =====================================================================================================================
