# from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Window(QWidget):
    COLUMNS = 5
    def __init__(self):
        super().__init__()

        layout_main = QHBoxLayout()
        self.setLayout(layout_main)

        font_names = QFontDatabase().families()
        col_len = len(font_names)//self.COLUMNS
        for col in range(self.COLUMNS):
            layout_col = QVBoxLayout()
            layout_main.addLayout(layout_col)

            index = 0
            while index < col_len:
                index += 1
                name = font_names.pop(0)
                wgt = QLabel(f"{name}")
                wgt.setFont(QFont(name))
                layout_col.addWidget(wgt)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
