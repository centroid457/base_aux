from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from base_aux.testplans.tc import *

from base_aux.pyqt.m0_static import *
from base_aux.pyqt.m0_base1_hl import *
from base_aux.pyqt.m4_gui import *
from base_aux.pyqt.m2_mods import *

from .tm import TpTableModel
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
class TpGuiBase(Gui):
    # OVERWRITTEN -----------------------------------
    START = False

    TITLE = "[TestPlan] Title"
    SIZE = (1500, 800)

    HL_STYLES = TpHlStyles()
    DIALOGS = DialogsSetTp

    # NEW -------------------------------------------
    DATA: "TpManager"

    def __init__(self, data):
        self.TITLE = f"[Тестплан]{data.STAND_NAME}/{data.STAND_DESCRIPTION[:20]}"
        super().__init__(data)

    def main_window__finalise(self):
        super().main_window__finalise()
        self.BTN_extended_mode.setChecked(True)

    # WINDOW ==========================================================================================================
    def wgt_create(self):
        self.BTN_create()
        self.CB_create()
        self.TV_create()
        self.PTE_create()
        self.HL_create()

        # LAYOUT_CONTROL ----------------------------------------------------------------------------------------------
        layout_control = QVBoxLayout()
        layout_control.setAlignment(ALIGNMENT.T)

        layout_control.addWidget(self.BTN_devs_detect)
        layout_control.addWidget(self.BTN_start)
        layout_control.addWidget(self.CB_tp_run_infinit)
        layout_control.addWidget(self.CB_tc_run_single)
        layout_control.addWidget(self.BTN_save)
        layout_control.addStretch()

        layout_control.addWidget(self.BTN_settings)
        layout_control.addWidget(self.BTN_clear_all)
        layout_control.addWidget(self.BTN_reset_all)
        layout_control.addWidget(self.BTN_extended_mode)

        # LAYOUT_MAIN -------------------------------------------------------------------------------------------------
        self.LAYOUT_MAIN = QHBoxLayout()
        self.LAYOUT_MAIN.addLayout(layout_control)
        self.LAYOUT_MAIN.addWidget(self.TV)
        self.LAYOUT_MAIN.addWidget(self.PTE)

        # CENTRAL -----------------------------------------------------------------------------------------------------
        self.CENTRAL_WGT.setLayout(self.LAYOUT_MAIN)

    # WGTS ============================================================================================================
    def BTN_create(self) -> None:
        self.BTN_devs_detect = QPushButton("определить устройства")

        self.BTN_start = QPushButton_Checkable(["ТЕСТИРОВАНИЕ запустить", "ТЕСТИРОВАНИЕ остановить"])
        self.BTN_start.setCheckable(True)

        self.BTN_settings = QPushButton("настройки")
        self.BTN_settings.setCheckable(True)

        self.BTN_save = QPushButton("Сохранить результаты")
        self.BTN_clear_all = QPushButton("Очистить все результаты")
        self.BTN_reset_all = QPushButton("Отключить все устройства")

        self.BTN_extended_mode = QPushButton("Расширенный режим")
        self.BTN_extended_mode.setCheckable(True)

    def CB_create(self) -> None:
        self.CB_tp_run_infinit = QCheckBox("бесконечный цикл тестирования")
        self.CB_tc_run_single = QCheckBox("запускать только выбранный тесткейс")

        # SETTINGS -------------------------
        # self.CB_tp_run_infinit.setText("CB_text")
        # self.CB_tp_run_infinit.setText("CB_text")

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
        # TODO: move examples to pyqtTemplate!
        self.TM = TpTableModel(self.DATA)

        self.TV = QTableView()
        self.TV.setModel(self.TM)
        self.TV.setSelectionMode(QTableView.SingleSelection)

        hh: QHeaderView = self.TV.horizontalHeader()
        # hh.setSectionHidden(self.TM.ADDITIONAL_COLUMNS - 1, True)
        hh.setSectionsClickable(False)
        # hh.setStretchLastSection(True)
        hh.setSectionResizeMode(QHeaderView.ResizeToContents)   # autoresize width!

        # hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # for index of column set stretch size
        # hh.setMinimumSize(0, QHeaderView.ResizeMode.Stretch)
        hh.setMinimumWidth(1000)    # dont understand it is not work at least with ResizeToContents

        self.TV.resizeColumnsToContents()
        self.TV.resizeRowsToContents()


    # SLOTS ===========================================================================================================
    def slots_connect(self):
        self.CB_tp_run_infinit.stateChanged.connect(self.CB_tp_run_infinit__changed)
        self.CB_tc_run_single.stateChanged.connect(self.CB_tc_run_single__changed)

        self.BTN_start.toggled.connect(self.BTN_start__toggled)
        self.BTN_settings.toggled.connect(self.BTN_settings__toggled)
        self.BTN_devs_detect.clicked.connect(self.BTN_devs_detect__clicked)
        self.BTN_save.clicked.connect(self.BTN_save__clicked)
        self.BTN_clear_all.clicked.connect(self.BTN_clear_all__clicked)
        self.BTN_reset_all.clicked.connect(self.BTN_reset_all__clicked)
        self.BTN_extended_mode.toggled.connect(self.BTN_extended_mode__toggled)

        # self.DATA.signal__tp_finished.connect(self.BTN_reset_all__clicked)
        self.DATA.signal__tp_finished.connect(lambda: self.BTN_start.setChecked(False))
        self.DATA.signal__tp_finished.connect(self.TM._data_reread)

        self.DATA.signal__devs_detected.connect(self.DIALOGS.finished__devs_detection)
        self.DATA.signal__tp_finished.connect(self.DIALOGS.finished__tp)

        Base_TestCase.signals.signal__tc_state_changed.connect(lambda _: self.TM._data_reread())

        self.TV.selectionModel().selectionChanged.connect(self.TV_selectionChanged)
        self.TV.horizontalHeader().sectionClicked.connect(self.TV_hh_sectionClicked)

    # -----------------------------------------------------------------------------------------------------------------
    def CB_tp_run_infinit__changed(self, state: Optional[int] = None) -> None:
        """
        :param state:
            0 - unchecked
            1 - halfCHecked (only if isTristate)
            2 - checked (even if not isTristate)
        """
        self.DATA.TP_RUN_INFINIT = bool(state)

    def CB_tc_run_single__changed(self, state: Optional[int] = None) -> None:
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

        self.TM._data_reread()

    def BTN_start__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"btn {state=}")
        if self.DATA.isRunning():
            state = False

        if state:
            self.DATA.start()
        elif not state:
            # if not self.DATA.isFinished():
            self.DATA.terminate()

        self.TM._data_reread()

    def BTN_settings__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"BTN_select_tc_on_duts__toggled {state=}")
        # self.TV.horizontalHeader().setSectionHidden(self.TM.ADDITIONAL_COLUMNS - 1, not state)
        self.TV.horizontalHeader().setSectionsClickable(state)
        self.TM.open__settings = state
        self.TM._data_reread()

    def BTN_devs_detect__clicked(self) -> None:
        self.DATA.DEVICES__BREEDER_CLS.group_call__("address_forget")
        self.DATA.DEVICES__BREEDER_CLS.CLS_LIST__DUT.ADDRESSES__SYSTEM.clear()
        self.TM._data_reread()
        # self.DATA.DEVICES__BREEDER_CLS.group_call__("address__resolve")    # MOVE TO THREAD??? no! not so need!
        self.DATA.DEVICES__BREEDER_CLS.resolve_addresses__cls()    # MOVE TO THREAD??? no! not so need!
        self.TM._data_reread()
        self.DATA.signal__devs_detected.emit()

    def BTN_save__clicked(self) -> None:
        self.DATA.save__results()
        self.DIALOGS.finished__save()

    def BTN_reset_all__clicked(self) -> None:
        self.DATA.DEVICES__BREEDER_CLS.group_call__("reset")

    def BTN_clear_all__clicked(self) -> None:
        self.DATA.tcs_clear()
        self.TM._data_reread()

    def BTN_extended_mode__toggled(self, state: Optional[bool] = None) -> None:
        self.PTE.setHidden(not state)

        hh: QHeaderView = self.TV.horizontalHeader()
        hh.setSectionHidden(self.TM.HEADERS.SKIP, not state)
        hh.setSectionHidden(self.TM.HEADERS.ASYNC, not state)
        hh.setSectionHidden(self.TM.HEADERS.STARTUP_CLS, not state)
        hh.setSectionHidden(self.TM.HEADERS.TEARDOWN_CLS, not state)

    def TV_hh_sectionClicked(self, index: int) -> None:
        if index == self.TM.HEADERS.STARTUP_CLS:
            pass

        if index == self.TM.HEADERS.TEARDOWN_CLS:
            pass

        if index in self.TM.HEADERS.DUTS:
            dut = self.DATA.DEVICES__BREEDER_CLS.LIST__DUT[self.TM.HEADERS.DUTS.get_listed_index__by_outer(index)]
            dut.SKIP_reverse()
            self.TM._data_reread()

    def TV_selectionChanged(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            # when item with noFlag IsSelectable
            return

        index: QModelIndex = first.indexes()[0]

        row = index.row()
        col = index.column()

        try:
            tc_cls = list(self.DATA.TCS_CLS)[row]
        except:
            tc_cls = None

        row_is_summary: bool = tc_cls is None

        if self.DATA._TC_RUN_SINGLE and not row_is_summary:
            self.DATA.tc_active = tc_cls

        if col == self.TM.HEADERS.STARTUP_CLS:
            if not row_is_summary:
                self.PTE.setPlainText(str(tc_cls.result__startup_cls))

        if col in self.TM.HEADERS.DUTS:
            if row_is_summary:
                pass    # TODO: add summary_result
            else:
                dut = self.DATA.DEVICES__BREEDER_CLS.LIST__DUT[col - self.TM.HEADERS.DUTS.START_OUTER]
                self.PTE.setPlainText(tc_cls.TCS__LIST[dut.INDEX].get__results_pretty())

        if col == self.TM.HEADERS.TEARDOWN_CLS:
            if not row_is_summary:
                self.PTE.setPlainText(str(tc_cls.result__teardown_cls))

        self.TM._data_reread()


# =====================================================================================================================
