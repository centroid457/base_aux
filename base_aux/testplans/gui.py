from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from base_aux.testplans.tc import *
from base_aux.testplans.tp_item import Base_TpItem

from base_aux.aux_attr.m1_annot_attr1_aux import *

from base_aux.pyqt.m0_static import *
from base_aux.pyqt.m0_base1_hl import *
from base_aux.pyqt.m4_gui import *
from base_aux.pyqt.m2_mods import *

from .tm__tcs import TableModel_Tps
from .tm__devs import TableModel_Devs
from .dialog import DialogsSetTp


# =====================================================================================================================
class TpHlStyles(HlStyles):
    RESULT: HlStyle = HlStyle(
        FORMAT=format_make("", "", "lightGrey"),
        P_ITEMS=[
            "validate_last_bool", "result",
        ],
        P_TEMPLATES=[
            r'.*%s.*',
        ],
    )
    RESULT_TRUE: HlStyle = HlStyle(
        FORMAT=format_make("", "", "lightGreen"),
        P_ITEMS=[
            "True",
        ],
        P_TEMPLATES=[
            r'.*validate_last_bool=%s.*',
            r'.*result[^=]*=%s.*',
            # r'.*valid[^=]*=%s.*',
        ],
    )
    RESULT_FALSE: HlStyle = HlStyle(
        FORMAT=format_make("", "", "pink"),
        P_ITEMS=[
            "False",
        ],
        P_TEMPLATES=[
            r'.*validate_last_bool=%s.*',
            r'.*result[^=]*=%s.*',
            # r'.*valid[^=]*=%s.*',
        ],
    )
    # yellow -----
    RESULT_FALSE_NOCUM: HlStyle = HlStyle(
        FORMAT=format_make("", "", "yellow"),
        P_ITEMS=[
            "ValidNoCum", "ValidSleep", "ValidBreak",
        ],
        P_TEMPLATES=[
            r'.*%s.*validate_last_bool=False.*',
        ],
    )
    SKIPPED_LINE: HlStyle = HlStyle(
        FORMAT=format_make("", "", "yellow"),
        P_ITEMS=[
        ],
        P_TEMPLATES=[
            r'.*skip_last=True.*',
        ],
    )
    BREAK: HlStyle = HlStyle(
        FORMAT=format_make("", "", "yellow"),
        P_ITEMS=[
            "ValidBreak",
        ],
        P_TEMPLATES=[
            r'.*%s.*validate_last_bool=True.*',
        ],
    )


PTE_RESULTS_EXAMPLE = """
ПРИМЕРНЫЙ ТЕКСТ ДЛЯ ПРОВЕРКИ


ПРОВЕРКА выделения текста результатов

Valid=None    #без явного bool значения
Result=True   #явное True
Valid=True    #явное True
Valid=False   #явное False
ValidNoCum(123x=False, validate_last_bool=True)
ValidNoCum(123x=True, validate_last_bool=False)  #неважный/неучтенный False

result__startup=True
------------------------------------------------------------
result=Valid(NAME=GET,skip_last=False,validate_last_bool=True,
...VALUE_LINK=<function SerialClient.__getattr__.<locals>.<lambda> at 0x000001E5AABF6FC0>,ARGS__VALUE=('PRSNT',),value_last=0,
...VALIDATE_LINK=0,validate_last=True,
,finished=True,timestamp_last=1730375894.4305248,
------------------------------------------------------------
result__teardown=ValidChains(NAME=,skip_last=False,validate_last_bool=True,
...VALUE_LINK=None,value_last=None,
...VALIDATE_LINK=True,validate_last=True,
,finished=True,timestamp_last=1730375895.0524113,
result__startup=ValidSleep(NAME=Sleep,skip_last=False,validate_last_bool=True,
___0:(START) len=3/timestamp=1730375895.0524113
___1:ValidNoCum(NAME=DUT.connect__only_if_address_resolved,skip_last=False,validate_last_bool=False,
___1:ValidNoCum(NAME=DUT.connect__only_if_address_resolved,skip_last=False,validate_last_bool=True,
___1:ValidNoCum(NAME=DUT.connect__only_if_address_resolved,skip_last=False,validate_last_bool=None,
___1:Valid(NAME=DUT.connect__only_if_address_resolved,skip_last=False,validate_last_bool=True,
...VALUE_LINK=<bound method SerialClient.connect__only_if_address_resolved of <DEVICES.ptb.Device object at 0x000001E5AAB4B050>>,value_last=True,
...VALIDATE_LINK=True,validate_last=True,
,finished=True,timestamp_last=1730375895.0524113,
___2:ValidRetry1(NAME=RST,skip_last=False,validate_last_bool=True,
...VALUE_LINK=<function SerialClient.__getattr__.<locals>.<lambda> at 0x000001E5AABF7240>,value_last=OK,
...VALIDATE_LINK=OK,validate_last=True,
,finished=True,timestamp_last=1730375896.3252466,
___3:ValidSleep(NAME=Sleep,skip_last=False,validate_last_bool=True,
...VALUE_LINK=<built-in function sleep>,ARGS__VALUE=(1,),value_last=None,
...VALIDATE_LINK=None,validate_last=True,
,finished=True,timestamp_last=1730375896.9521606,
___4:(FINISH) [result=False]/len=3
------------------------------------------------------------
DETAILS=====================
"""


# =====================================================================================================================
class ListModel_Tp(QAbstractListModel):
    TP_ITEMS: list[Base_TpItem]

    def __init__(self, tp_items: list[Base_TpItem] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TP_ITEMS = tp_items or []
        self.TP_ITEMS = [*self.TP_ITEMS, ]

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.TP_ITEMS)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            tp_item = self.TP_ITEMS[index.row()]
            return tp_item.NAME


# =====================================================================================================================
class Base_TpGui(Gui):
    # OVERWRITTEN -----------------------------------
    START = False

    TITLE = "TestPlan"
    SIZE = (1500, 800)

    HL_STYLES = TpHlStyles()
    DIALOGS = DialogsSetTp

    # NEW -------------------------------------------
    DATA: "TpManager"

    def main_window__finalise(self):
        super().main_window__finalise()
        self.BTN_extended_mode.setChecked(True)

        self.CBB.setCurrentText(self.DATA.TP_ITEM.NAME)

    # WINDOW ==========================================================================================================
    def wgt_create(self):
        self.BTN_create()
        self.CHB_create()
        self.CBB_create()
        self.TV_create()
        self.PTE_create()
        self.HL_create()

        # LAYOUT_CONTROL ----------------------------------------------------------------------------------------------
        layout__control = QVBoxLayout()
        layout__control.setAlignment(ALIGNMENT.T)

        layout__control.addWidget(QLabel("Выбор тестплана:"))
        layout__control.addWidget(self.CBB)
        layout__control.addSpacing(20)

        layout__control.addWidget(QLabel("Тестирование:"))
        layout__control.addWidget(self.BTN_start)
        layout__control.addWidget(self.CHB_tp_run_infinit)
        layout__control.addWidget(self.CHB_tc_run_single)
        layout__control.addWidget(self.BTN_save)
        layout__control.addSpacing(20)

        layout__control.addWidget(QLabel("Устройства:"))
        layout__control.addWidget(self.BTN_devs_detect)
        layout__control.addWidget(self.BTN_tv_devs_show)
        layout__control.addWidget(self.BTN_reset_all)
        layout__control.addStretch()

        layout__control.addWidget(QLabel("Дополнительно:"))
        layout__control.addWidget(self.BTN_settings)
        layout__control.addWidget(self.BTN_tm_update)
        layout__control.addWidget(self.BTN_clear_all)
        layout__control.addWidget(self.BTN_extended_mode)

        # LAYOUT_TV -------------------------------------------------------------------------------------------------
        layout__tv = QVBoxLayout()
        layout__tv.setAlignment(ALIGNMENT.T)

        layout__tv.addWidget(self.TV_TCS)
        layout__tv.addWidget(self.TV_DEV)

        # LAYOUT_MAIN -------------------------------------------------------------------------------------------------
        self.LAYOUT_MAIN = QHBoxLayout()
        self.LAYOUT_MAIN.addLayout(layout__control)
        self.LAYOUT_MAIN.addLayout(layout__tv)
        self.LAYOUT_MAIN.addWidget(self.PTE)

        # CENTRAL -----------------------------------------------------------------------------------------------------
        self.CENTRAL_WGT.setLayout(self.LAYOUT_MAIN)

    # WGTS ============================================================================================================
    def BTN_create(self) -> None:
        self.BTN_devs_detect = QPushButton("Определить устройства")
        self.BTN_tv_devs_show = QPushButton_Checkable(["ОТОБРАЗИТЬ панель устройств", "СКРЫТЬ панель устройств"])

        self.BTN_start = QPushButton_Checkable(["ТЕСТИРОВАНИЕ запустить", "ТЕСТИРОВАНИЕ остановить"])
        self.BTN_start.setCheckable(True)

        self.BTN_settings = QPushButton("Настройки отобразить")
        self.BTN_settings.setCheckable(True)

        self.BTN_save = QPushButton("Сохранить результаты")
        self.BTN_tm_update = QPushButton("Обновить таблицу")
        self.BTN_clear_all = QPushButton("Очистить все результаты")
        self.BTN_reset_all = QPushButton("Отключить все устройства")

        self.BTN_extended_mode = QPushButton("Расширенный режим")
        self.BTN_extended_mode.setCheckable(True)

    def CHB_create(self) -> None:
        self.CHB_tp_run_infinit = QCheckBox("бесконечный цикл тестирования")
        self.CHB_tc_run_single = QCheckBox("запускать только выбранный тесткейс")

        # SETTINGS -------------------------
        # self.CHB_tp_run_infinit.setText("CB_text")
        # self.CHB_tp_run_infinit.setText("CB_text")

    def CBB_create(self) -> None:
        self.CBB = QComboBox()
        self.CBB.setModel(ListModel_Tp(self.DATA.TP_ITEMS()))
        # self.CBB.setDisabled(True)

    def PTE_create(self) -> None:
        self.PTE = QPlainTextEdit()

        # METHODS ORIGINAL ---------------------------------
        # self.PTE.setEnabled(True)
        # self.PTE.setUndoRedoEnabled(True)
        # self.PTE.setReadOnly(True)
        # self.PTE.setMaximumBlockCount(15)
        self.PTE.setMaximumWidth(500)

        # self.PTE.clear()
        self.PTE.appendPlainText(PTE_RESULTS_EXAMPLE)

        # self.PTE.appendHtml("")
        # self.PTE.anchorAt(#)
        # self.PTE.setSizeAdjustPolicy(#)
        # self.PTE.setHidden(True)

        # METHODS COMMON -----------------------------------
        self.PTE.setFont(QFont("Calibri (Body)", 7))

    def TV_create(self):
        self.TV_TCS__create()
        self.TV_DEV__create()

    def TV_TCS__create(self):
        self.TM_TCS = TableModel_Tps(self.DATA)

        self.TV_TCS = QTableView()
        self.TV_TCS.setModel(self.TM_TCS)
        self.TV_TCS.setSelectionMode(QTableView.SingleSelection)

        hh: QHeaderView = self.TV_TCS.horizontalHeader()
        # hh.setSectionHidden(self.TM_TCS.ADDITIONAL_COLUMNS - 1, True)
        hh.setSectionsClickable(False)
        # hh.setStretchLastSection(True)
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)   # autoresize width!

        # hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # for index of column set stretch size
        # hh.setMinimumSize(0, QHeaderView.ResizeMode.Stretch)
        hh.setMinimumWidth(1000)    # dont understand it is not work at least with ResizeToContents

        self.TV_TCS.resizeColumnsToContents()
        self.TV_TCS.resizeRowsToContents()

    def TV_DEV__create(self):
        self.TM_DEV = TableModel_Devs(self.DATA)

        self.TV_DEV = QTableView()
        self.TV_DEV.setModel(self.TM_DEV)
        self.TV_DEV.setSelectionMode(QTableView.SingleSelection)

        hh: QHeaderView = self.TV_DEV.horizontalHeader()
        # hh.setSectionHidden(self.TM_DEV.ADDITIONAL_COLUMNS - 1, True)
        hh.setSectionsClickable(False)
        # hh.setStretchLastSection(True)
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)  # autoresize width!

        # hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # for index of column set stretch size
        # hh.setMinimumSize(0, QHeaderView.ResizeMode.Stretch)
        hh.setMinimumWidth(1000)  # dont understand it is not work at least with ResizeToContents

        self.TV_DEV.resizeColumnsToContents()
        self.TV_DEV.resizeRowsToContents()

    # SLOTS ===========================================================================================================
    def slots_connect(self):
        self.CBB.activated[int].connect(self.CBB__changed)

        self.CHB_tp_run_infinit.stateChanged.connect(self.CHB_tp_run_infinit__changed)
        self.CHB_tc_run_single.stateChanged.connect(self.CHB_tc_run_single__changed)

        self.BTN_start.toggled.connect(self.BTN_start__toggled)
        self.BTN_settings.toggled.connect(self.BTN_settings__toggled)
        self.BTN_devs_detect.clicked.connect(self.BTN_devs_detect__clicked)
        self.BTN_tv_devs_show.toggled.connect(self.BTN_tv_devs_show__toggled)
        self.BTN_save.clicked.connect(self.BTN_save__clicked)
        self.BTN_tm_update.clicked.connect(self.TM_TCS._data_reread)
        self.BTN_clear_all.clicked.connect(self.BTN_clear_all__clicked)
        self.BTN_reset_all.clicked.connect(self.BTN_reset_all__clicked)
        self.BTN_extended_mode.toggled.connect(self.BTN_extended_mode__toggled)

        # self.DATA.signal__tp_finished.connect(self.BTN_reset_all__clicked)
        self.DATA.signal__tp_finished.connect(lambda: self.BTN_start.setChecked(False))
        self.DATA.signal__tp_finished.connect(self.TM_TCS._data_reread)

        self.DATA.signal__devs_detected.connect(self.DIALOGS.finished__devs_detection)
        self.DATA.signal__tp_finished.connect(self.DIALOGS.finished__tp)

        Base_TestCase.signals.signal__tc_state_changed.connect(lambda _: self.TM_TCS._data_reread())

        self.TV_TCS.selectionModel().selectionChanged.connect(self.TV_TCS__selectionChanged)
        self.TV_TCS.horizontalHeader().sectionClicked.connect(self.TV_TCS__hh_sectionClicked)

        self.TV_DEV.selectionModel().selectionChanged.connect(self.TV_DEV__selectionChanged)

    # -----------------------------------------------------------------------------------------------------------------
    def CBB__changed(self, index: Optional[int] = 0) -> None:
        tp_item = self.CBB.model().TP_ITEMS[index or 0]
        self.DATA.tp_item__init(tp_item)

        # ------------------------------
        self.TM_TCS.reinit(self.DATA)
        self.TM_TCS._data_reread()

        self.TM_DEV.reinit(self.DATA)
        self.TM_DEV._data_reread()

        # adjust ------------------------------
        self.TV_TCS.resizeColumnsToContents()
        self.TV_TCS.resizeRowsToContents()

    def CHB_tp_run_infinit__changed(self, state: Optional[int] = None) -> None:
        """
        :param state:
            0 - unchecked
            1 - halfCHecked (only if isTristate)
            2 - checked (even if not isTristate)
        """
        self.DATA.TP_RUN_INFINIT = bool(state)

    def CHB_tc_run_single__changed(self, state: Optional[int] = None) -> None:
        """
        :param state:
            0 - unchecked
            1 - halfCHecked (only if isTristate)
            2 - checked (even if not isTristate)
        """
        if state:
            self.DATA._TC_RUN_SINGLE = True
        else:
            self.DATA._TC_RUN_SINGLE = False
            if not self.DATA.isRunning():
                self.DATA.tc_active = None

        self.TM_TCS._data_reread()

    def BTN_start__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"btn {state=}")
        if self.DATA.isRunning():
            state = False

        if state:
            self.DATA.start()
        elif not state:
            # if not self.DATA.isFinished():
            self.DATA.terminate()

        self.TM_TCS._data_reread()

    def BTN_settings__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"BTN_select_tc_on_duts__toggled {state=}")
        # self.TV_TCS.horizontalHeader().setSectionHidden(self.TM_TCS.ADDITIONAL_COLUMNS - 1, not state)
        self.TV_TCS.horizontalHeader().setSectionsClickable(state)
        self.TM_TCS.open__settings = state
        self.TM_TCS._data_reread()

    def BTN_tv_devs_show__toggled(self, state) -> None:
        self.TV_DEV.setHidden(not state)

    def BTN_devs_detect__clicked(self) -> None:
        self.DATA.DEV_LINES("address_forget")
        self.DATA.DEV_LINES.DUT[0].ADDRESSES__SYSTEM.clear()
        self.TM_TCS._data_reread()
        # self.DATA.DEV_LINES.group_call__("address__resolve")    # MOVE TO THREAD??? no! not so need!
        self.DATA.DEV_LINES.resolve_addresses()    # MOVE TO THREAD??? no! not so need!
        self.TM_TCS._data_reread()
        self.DATA.signal__devs_detected.emit()

        self.TM_DEV._data_reread()

    def BTN_save__clicked(self) -> None:
        self.DATA.save__results()
        self.DIALOGS.finished__save()

    def BTN_reset_all__clicked(self) -> None:
        self.DATA.DEV_LINES.group_call__("reset")

    def BTN_clear_all__clicked(self) -> None:
        self.DATA.tcs_clear()
        self.TM_TCS._data_reread()

    def BTN_extended_mode__toggled(self, state: Optional[bool] = None) -> None:
        self.PTE.setHidden(not state)
        self.BTN_tv_devs_show.setChecked(state)

        hh: QHeaderView = self.TV_TCS.horizontalHeader()
        hh.setSectionHidden(self.TM_TCS.HEADERS.SKIP, not state)
        hh.setSectionHidden(self.TM_TCS.HEADERS.ASYNC, not state)
        hh.setSectionHidden(self.TM_TCS.HEADERS.STARTUP_CLS, not state)
        hh.setSectionHidden(self.TM_TCS.HEADERS.TEARDOWN_CLS, not state)

    # -----------------------------------------------------------------------------------------------------------------
    def TV_TCS__hh_sectionClicked(self, index: int) -> None:
        if index == self.TM_TCS.HEADERS.STARTUP_CLS:
            pass

        if index == self.TM_TCS.HEADERS.TEARDOWN_CLS:
            pass

        if index in self.TM_TCS.HEADERS.DUTS:
            dut = self.DATA.DEV_LINES.DUT[self.TM_TCS.HEADERS.DUTS.get_listed_index__by_outer(index)]
            dut.SKIP_reverse()
            self.TM_TCS._data_reread()

    def TV_TCS__selectionChanged(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            # when item with noFlag IsSelectable
            return

        try:
            index: QModelIndex = first.indexes()[0]
        except IndexError:
            # this happens when press any Arrow on Keyboard!
            return

        row = index.row()
        col = index.column()

        dut_index = col - self.TM_TCS.HEADERS.DUTS.START_OUTER

        try:
            tc_cls = list(self.DATA.TCS_CLS)[row]
        except:
            tc_cls = None

        row_is_summary: bool = tc_cls is None

        if self.DATA._TC_RUN_SINGLE and not row_is_summary:
            self.DATA.tc_active = tc_cls

        if col == self.TM_TCS.HEADERS.STARTUP_CLS:
            if not row_is_summary:
                self.PTE.setPlainText(str(tc_cls.result__startup_cls))

        if col in self.TM_TCS.HEADERS.DUTS:
            if row_is_summary:
                pass    # TODO: add summary_result
            else:

                dut = self.DATA.DEV_LINES.DUT[dut_index]
                self.PTE.setPlainText(tc_cls.TCS_LINE[dut_index].get__results_pretty())

        if col == self.TM_TCS.HEADERS.TEARDOWN_CLS:
            if not row_is_summary:
                self.PTE.setPlainText(str(tc_cls.result__teardown_cls))

        self.TM_TCS._data_reread()

    def TV_DEV__selectionChanged(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            # when item with noFlag IsSelectable
            return

        try:
            index: QModelIndex = first.indexes()[0]
        except IndexError:
            # this happens when press any Arrow on Keyboard!
            return

        row = index.row()
        col = index.column()

        try:
            # print(f"{self.DATA.DEV_LINES.names()()=}")
            dev_group_name = self.DATA.DEV_LINES.names()[row]
        except:
            return

        index = col - self.TM_DEV.HEADERS.DEVICE.START_OUTER
        try:
            dev_inst = self.DATA.TP_ITEM.DEV_LINES[dev_group_name][index]
        except:
            dev_inst = self.DATA.TP_ITEM.DEV_LINES[dev_group_name]

        text = AnnotsAllAux(dev_inst).dump_str__pretty()
        self.PTE.setPlainText(text)

        self.TM_DEV._data_reread()


# =====================================================================================================================
