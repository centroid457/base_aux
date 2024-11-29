from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.breeders import *
from .base import Data_
from base_aux.classes import Translator


# =====================================================================================================================
class Headers(BreederStrStack):
    NAME: int = 0
    BATCH: BreederStrSeries = BreederStrSeries(1, 4)


# =====================================================================================================================
class TableModelTemplate(QAbstractTableModel):
    DATA: Data_
    HEADERS: BreederStrStack = Headers()
    HTRANSLATOR: Translator = None

    # METHODS USER ----------------------------------------------------------------------------------------------------
    def __init__(self, data: Optional[Any] = None):
        super().__init__(parent=None)
        self.DATA = data

    def _data_reread(self) -> None:
        """
        just redraw model by reread all data!
        """
        self.endResetModel()

    # =================================================================================================================
    def rowCount(self, parent: Any = None, *args, **kwargs) -> int:
        return len(self.DATA.ROWS)

    def columnCount(self, parent: Any = None, *args, **kwargs) -> int:
        return len(self.DATA.DEVS) + 1

    # =================================================================================================================
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:      # in headerData WORK ONLY DisplayRole+TOOLTIP!!!
            if orientation == Qt.Horizontal:
                value = self.HEADERS[section]
                if self.HTRANSLATOR:
                    value = self.HTRANSLATOR(value)
                return value

            if orientation == Qt.Vertical:
                return str(section + 1)

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.ToolTipRole:
            if orientation == Qt.Horizontal:
                return self.HEADERS[section]

        # # -------------------------------------------------------------------------------------------------------------
        # if role == Qt.CheckStateRole:      # ЧЕКБОКСЫ  - IS IT WORK???
        #     # -------------------
        #     dut = None
        #     if section > 0:
        #         return Qt.Checked
        #
        #         dut = self.DATA.DEVS[section - 1]
        #
        #         if section % 2:
        #             return Qt.Unchecked
        #         else:
        #             return Qt.Checked

        # -------------------------------------------------------------------------------------------------------------
        # if role == Qt.BackgroundColorRole:  # DONT WORK!!!
        #     return QColor('red')
        #
        #     # -------------------
        #     dut = None
        #     if section > 1:
        #         dut = self.DATA.DEVS[section - 1]
        #         if not hasattr(dut, "SKIP"):
        #             dut.SKIP = False
        #
        #         if not dut.SKIP:
        #             return QColor('#f2f2f2')

    # def setHeaderData(self, section: int, orientation: Qt.Orientation, value: Any, role: int = Qt.DisplayRole) -> bool:
    #     # -------------------------------------------------------------------------------------------------------------
    #     if orientation == Qt.Vertical:
    #         return super().setHeaderData(section, orientation, value, role)
    #
    #     # -------------------------------------------------------------------------------------------------------------
    #     if orientation == Qt.Horizontal:
    #         # -------------------
    #         dut = None
    #         if section > 0:
    #             dut = self.DATA.DEVS[section - 1]
    #
    #         # -------------------
    #         if role == Qt.CheckStateRole:      # ЧЕКБОКСЫ
    #             if section == 1:
    #                 return "NAME"
    #             if section > 0:
    #                 return f"{section}"
    #
    #     return True

    # =================================================================================================================
    def flags(self, index: QModelIndex) -> int:
        """
        VARIANTS FLAGS
        --------------
        flags = Qt.NoItemFlags              # 0=без флагов - полное отключение и деактивация всего
        flags |= Qt.ItemIsSelectable        # 1=выделяется цветом при выборе, иначе только внешней рамкой!
        flags |= Qt.ItemIsEditable          # 2=можно набирать с клавиатуры!
        flags |= Qt.ItemIsDragEnabled       # 4=
        flags |= Qt.ItemIsDropEnabled       # 8=
        flags |= Qt.ItemIsUserCheckable     # 16=для чекбоксов дает возможность их изменять мышью!
        flags |= Qt.ItemIsEnabled           # 32=если нет - будет затенен! без возможности выбора!
        flags |= Qt.ItemIsTristate=ItemIsAutoTristate    # 64=включение промежуточного значения чекбокса
        flags |= Qt.ItemNeverHasChildren    # 128=
        flags |= Qt.ItemIsUserTristate      # 256=
        """
        col = index.column()
        row = index.row()

        flags = super().flags(index)    # recommended using as default! and switching exact flags

        if col == 0:
            # FIXME: HEADER CAUSE EXCEPTION CLOSE!

            flags = Qt.NoItemFlags  # 0=без флагов - полное отключение и деактивация всего
            # flags |= Qt.ItemIsSelectable  # 1=выделяется цветом при выборе, иначе только внешней рамкой!
            # flags |= Qt.ItemIsEditable  # 2=можно набирать с клавиатуры!
            # flags |= Qt.ItemIsDragEnabled  # 4=
            # flags |= Qt.ItemIsDropEnabled  # 8=
            flags |= Qt.ItemIsUserCheckable  # 16=для чекбоксов дает возможность их изменять мышью!
            flags |= Qt.ItemIsEnabled  # 32=если нет - будет затенен! без возможности выбора!
            flags |= Qt.ItemIsTristate  #=ItemIsAutoTristate  # 64=включение промежуточного значения чекбокса
            # flags |= Qt.ItemNeverHasChildren  # 128=
            # flags |= Qt.ItemIsUserTristate  # 256=

        return flags

    # =================================================================================================================
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # if not index.isValid():
        #     return QVariant()
        """
        ROLES
        -------------
        DisplayRole = 0
        DecorationRole = 1
        EditRole = 2
        ToolTipRole = 3
        StatusTipRole = 4
        WhatsThisRole = 5
        FontRole = 6
        TextAlignmentRole = 7

        BackgroundRole=BackgroundColorRole = 8
        ForegroundRole=TextColorRole = 9

        CheckStateRole = 10
        SizeHintRole = 13
        InitialSortOrderRole = 14
        UserRole = 256
        """
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        tc = list(self.DATA.ROWS)[row]
        dut = None
        if col in self.HEADERS.BATCH:
            dut = self.DATA.DEVS[col-1]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col < 0:
                print(f"STOP{index=}")
            if col == 0:
                return f'{tc.NAME}'
            if col in self.HEADERS.BATCH:
                return f'{dut.result}'

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextAlignmentRole:
            """
            VARIANTS ALIGN
            --------------
            not exists NAME!!!} = 0         # (LEFT+TOP) [[[[[[[[DEFAULT IS [LEFT+TOP]]]]]]]]]

            AlignLeft=AlignLeading = 1      # LEFT(+TOP)
            AlignRight=AlignTrailing = 2    # RIGHT(+TOP)

            AlignTop = 32       # TOP(+LEFT)
            AlignBottom = 64    # BOT(+LEFT)

            AlignHCenter = 4    # HCENTER(+TOP)
            AlignVCenter = 128  # VCENTER(+LEFT)
            AlignCenter = 132   # VCENTER+HCENTER

            # =====MAYBE DID NOT FIGURED OUT!!!
            AlignAbsolute = 16      # (LEFT+TOP) == asDEFAULT
            AlignBaseline = 256     # (LEFT+TOP) == asDEFAULT

            AlignJustify = 8        # (LEFT+TOP) == asDEFAULT

            AlignHorizontal_Mask = 31   # TOP+RIGHT
            AlignVertical_Mask = 480    # LEFT+VCENTER
            """
            if col == 0:
                return Qt.AlignVCenter
            if col in self.HEADERS.BATCH:
                return Qt.AlignCenter

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.FontRole:
            if row % 2:
                # QFont("Arial", 9, QFont.Bold)
                font = QFont()

                font.setBold(True)
                font.setItalic(True)

                font.setOverline(True)      # надчеркнутый
                font.setStrikeOut(True)     # зачеркнутый
                font.setUnderline(True)     # подчеркнутый

                # не понял!! --------------------
                # font.setStretch(5)
                # font.setCapitalization()

                return font

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:   # =BackgroundRole
            if tc.SKIP or (dut and dut.SKIP):
                return QColor('#e2e2e2')

            if col in self.HEADERS.BATCH:
                if tc.result is True:
                    return QColor("green")
                if tc.result is False:
                    return QColor("red")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:   # =ForegroundRole
            if tc.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:   # для чекбоксов!
            """
            VARIANTS CHECK
            --------------
            Unchecked (или 0) - флажок сброшен;
            PartiallyChecked (или 1) - флажок частично установлен;
            Checked (или 2) - флажок установлен
            """
            if col == 0:
                if tc.SKIP is True:
                    return Qt.Unchecked
                elif tc.SKIP is False:
                    return Qt.Checked
                else:
                    return Qt.PartiallyChecked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.ToolTipRole:
            return f"{row}/{col}"

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DecorationRole:   # ИКОНКА в ячейке слева!
            # может не работать! не работало с первого раза, НО потом вдруг заработало само собой когда добавил SizeHintRole!!! больше не пропадало!!!
            if col == 1 and not tc.SKIP:
                icon = QIcon()
                icon.addPixmap(QPixmap('logo.jpg'))
                return icon

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.SizeHintRole:     # размер ячейки!
            """
            IMPORTANT: 
            1. meaning like MinimumSize!
            2. BUT if there are IconOrCheck exists - size will be same as before adding it and HIDING oversized text
            """
            if col in self.HEADERS.BATCH:
                return QSize(5, 5)

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        """
        NOTE: при фактическом изменении ОБЯЗАТЕЛЬНО возвращать TRUE!!! Иначе Exx!!!!
        in other cases you can return True either, or None!
        """
        # TODO: ALWAYS START data_reread after any SETDATA
        # if not index.isValid():
        #     return False

        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        tc = list(self.DATA.ROWS)[row]
        if col in self.HEADERS.BATCH:
            dut = self.DATA.DEVS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:      # ЧЕКБОКСЫ
            # need used flag ItemIsUserCheckable!
            if col == 0:
                tc.SKIP = value == Qt.Unchecked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.EditRole:
            # need used flag ItemIsEditable!
            if col == 0:
                print("EditRole")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.SizeHintRole:
            # хотел увидеть изменение размера НО ЭТО ТАК НЕ РАБОТАЕТ!!!
            print("SizeHintRole")

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
