from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.pyqt import TableModelTemplate
from base_aux.breeders import *


# =====================================================================================================================
class TpTableModel(TableModelTemplate):
    DATA: "TpMultyDutBase"
    HEADERS: "Headers"

    # AUX -------------------------------------------
    open__settings: Optional[bool] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Headers(BreederStrStack):
            TESTCASE: int = 0
            SKIP: None = None
            ASYNC: None = None
            STARTUP_CLS: None = None
            DUTS: BreederStrSeries = BreederStrSeries(None, self.DATA.DEVICES__BREEDER_CLS.COUNT)
            TEARDOWN_CLS: None = None
            # FIXME: need resolve COUNT over DevicesIndexed!!!

        self.HEADERS = Headers()

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS__CLS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return self.HEADERS.count()

    # def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
    #     if role == Qt.DisplayRole:
    #         # ------------------------------
    #         if orientation == Qt.Horizontal:
    #             return self.HEADERS[section]
    #
    #         # ------------------------------
    #         if orientation == Qt.Vertical:
    #             return str(section + 1)

    def flags(self, index: QModelIndex) -> int:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        # -------------------------------------------------------------------------------------------------------------
        flags = super().flags(index)

        if col in [self.HEADERS.SKIP, self.HEADERS.ASYNC] or col in self.HEADERS.DUTS:
            flags |= Qt.ItemIsUserCheckable
            # flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass

        # clear SELECTABLE ---------

        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()
        tc_cls = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS:
            index = col - self.HEADERS.DUTS.START_OUTER
            dut = self.DATA.DEVICES__BREEDER_CLS.LIST__DUT[index]
            tc_inst = tc_cls.TCS__LIST[index]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == self.HEADERS.TESTCASE:
                return f"{tc_cls.NAME}"
            if col == self.HEADERS.SKIP:
                return '+' if tc_cls.SKIP else '-'
            if col == self.HEADERS.ASYNC:
                return '+' if tc_cls.ASYNC else '-'

            # STARTUP -------------------
            if col == self.HEADERS.STARTUP_CLS:
                group_name = tc_cls.MIDDLE_GROUP__NAME or ""
                if tc_cls.result__startup_cls is None:
                    return group_name
                elif bool(tc_cls.result__startup_cls) is True:
                    return f'+{group_name}'
                elif bool(tc_cls.result__startup_cls) is False:
                    return f'-{group_name}'

            # DUTS -------------------
            if col in self.HEADERS.DUTS:
                if tc_inst:
                    if tc_inst.result is None:
                        return ""
                    else:
                        if bool(tc_inst.result):
                            return "PASS"
                        else:
                            return "FAIL"

            # TEARDOWN -------------------
            if col == self.HEADERS.TEARDOWN_CLS:
                if tc_cls.result__teardown_cls is None:
                    return
                elif bool(tc_cls.result__teardown_cls) is True:
                    return '+'
                elif bool(tc_cls.result__teardown_cls) is False:
                    return '-'

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.ToolTipRole:
            if col == self.HEADERS.TESTCASE:
                return f"{tc_cls.DESCRIPTION}"
            elif col in self.HEADERS.DUTS and tc_inst:
                return f"{tc_inst.result}"

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
            if col == self.HEADERS.TESTCASE:
                return Qt.AlignVCenter
            else:
                return Qt.AlignCenter

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:
            if tc_cls.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:
            if tc_cls.SKIP:
                return QColor('#e2e2e2')

            # ACTIVE ---------------------
            if col == self.HEADERS.TESTCASE:
                if self.DATA.tc_active == tc_cls:
                    return QColor("#FFFF50")

            # STARTUP -------------------
            if col == self.HEADERS.STARTUP_CLS:
                if tc_cls.result__startup_cls is None:
                    return
                elif bool(tc_cls.result__startup_cls) is True:
                    return QColor("#50FF50")
                elif bool(tc_cls.result__startup_cls) is False:
                    return QColor("#FF5050")

            # DUTS -------------------
            if col in self.HEADERS.DUTS:
                if tc_inst.skip_tc_dut or dut.SKIP or not dut.DEV_FOUND:
                    return QColor('#e2e2e2')
                elif tc_inst.result__startup is not None and not bool(tc_inst.result__startup):
                    return QColor("#FFa0a0")
                elif tc_inst.isRunning():
                    return QColor("#FFFF50")
                elif bool(tc_inst.result) is True:
                    return QColor("#00FF00")
                elif bool(tc_inst.result) is False:
                    if tc_inst.result is None:
                        return
                    else:
                        return QColor("#FF5050")
                # elif

            # TEARDOWN -------------------
            if col == self.HEADERS.TEARDOWN_CLS:
                if tc_cls.result__teardown_cls is None:
                    return
                elif bool(tc_cls.result__teardown_cls) is True:
                    return QColor("#50FF50")
                elif bool(tc_cls.result__teardown_cls) is False:
                    return QColor("#FF5050")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if self.open__settings:
                if col == self.HEADERS.SKIP:
                    if tc_cls.SKIP:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
                if col == self.HEADERS.ASYNC:
                    if tc_cls.ASYNC:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
                if col in self.HEADERS.DUTS:
                    if not tc_inst.SKIP and not dut.SKIP:
                        if tc_inst.skip_tc_dut:
                            return Qt.Unchecked
                        else:
                            return Qt.Checked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.FontRole:
            if tc_cls == self.DATA.tc_active:
                # QFont("Arial", 9, QFont.Bold)
                font = QFont()

                font.setBold(True)
                # font.setItalic(True)

                # font.setOverline(True)  # надчеркнутый
                # font.setStrikeOut(True)  # зачеркнутый
                font.setUnderline(True)  # подчеркнутый

                # не понял!! --------------------
                # font.setStretch(5)
                # font.setCapitalization()

                return font

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        # PREPARE -----------------------------------------------------------------------------------------------------
        row = index.row()
        col = index.column()
        tc_cls = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS:
            index = col - self.HEADERS.DUTS.START_OUTER
            dut = self.DATA.DEVICES__BREEDER_CLS.LIST__DUT[index]
            tc_inst = tc_cls(index=index)

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == self.HEADERS.SKIP:
                tc_cls.SKIP = value == Qt.Checked

            if col == self.HEADERS.ASYNC:
                tc_cls.ASYNC = value == Qt.Checked

            if col in self.HEADERS.DUTS:
                if tc_inst:
                    tc_inst.skip_tc_dut = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
