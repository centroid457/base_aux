from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from base_aux.pyqt.dialog import DialogsSet


# SET ============================================================================================================
class DialogsSetTp(DialogsSet):
    """
    attempt to keep all available dialogs for current project in one place!
    so to be sure there are no any other available!
    """
    @staticmethod
    def info__about(*args) -> int:
        wgt = QMessageBox()
        wgt.setMaximumWidth(1000)
        answer = wgt.information(
            None,
            "О программе",
            (
                "ООО Элемент-Инжиниринг,\n"
                "Программа проведения тестирования блоков питания\n"
                "(стендовые испытания ОТК)"
             )
        )
        # return always 1024
        return answer

    @staticmethod
    def finished__devs_detection(*args) -> int:
        wgt = QMessageBox()
        wgt.resize(1000, 1000)
        wgt.setBaseSize(1000, 1000)
        wgt.setToolTip("hello")
        answer = wgt.information(
            None,
            "Определение устройств",
            (
                "Процесс завершен" + " "*30
            )
        )
        # return always 1024
        return answer

    @staticmethod
    def finished__tp(*args) -> int:
        answer = QMessageBox.information(
            None,
            "Тестирование",
            (
                "Процесс завершен"
             )
        )
        # return always 1024
        return answer

    @staticmethod
    def finished__save(*args) -> int:
        answer = QMessageBox.information(
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
    # DialogsSetTp.info__about()
    DialogsSetTp.finished__devs_detection()
    # DialogsSetTp.finished__tp()
    # DialogsSetTp.finished__save()


# =====================================================================================================================
