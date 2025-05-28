from typing import *
import time

from PyQt5.QtCore import QThread, pyqtSignal

from base_aux.servers.m1_client_requests import *
from base_aux.loggers.m1_logger import *
from base_aux.path2_file.m3_filetext import *

# ---------------------------------------------------------------------------------------------------------------------
from base_aux.testplans.tc import Base_TestCase
from base_aux.testplans.devices import Base_Device, DeviceKit
from base_aux.testplans.gui import Base_TpGui
from base_aux.testplans.api import TpApi_FastApi
from base_aux.testplans.stand import Base_Stand


# =====================================================================================================================
class TpManager(Logger, QThread):
    signal__tp_start = pyqtSignal()
    signal__tp_stop = pyqtSignal()
    signal__tp_finished = pyqtSignal()
    signal__devs_detected = pyqtSignal()

    _signal__tp_reset_duts_sn = pyqtSignal()

    # SETTINGS ------------------------------------------------------
    TP_RUN_INFINIT: bool | None = None     # True - when run() started - dont stop!
    TP_RUN_INFINIT__TIMEOUT: int = 3

    _TC_RUN_SINGLE: bool | None = None

    START__GUI_AND_API: bool = True

    API_SERVER__START: bool = True
    API_SERVER__CLS: type[TpApi_FastApi] = TpApi_FastApi
    api_server: TpApi_FastApi

    GUI__START: bool = True
    GUI__CLS: type[Base_TpGui] = Base_TpGui

    api_client: Client_RequestsStack = Client_RequestsStack()   # todo: USE CLS!!! + add start

    # AUX -----------------------------------------------------------
    STANDS: 'Stands'
    STAND: Base_Stand

    __tc_active: Optional[type[Base_TestCase]] = None

    # =================================================================================================================
    @property
    def tc_active(self) -> type[Base_TestCase] | None:
        return self.__tc_active

    @tc_active.setter
    def tc_active(self, value: type[Base_TestCase] | None) -> None:
        self.__tc_active = value

    def tp__check_active(self) -> bool:
        result = self.tc_active is not None and self.tc_active.STATE_ACTIVE__CLS == Enum_ProcessStateActive.STARTED
        return result

    # =================================================================================================================
    def __init__(self):
        super().__init__()

        self.slots_connect()
        self.init_post()

        # FINAL FREEZE ----------------
        if self.START__GUI_AND_API:
            self.start__gui_and_api()

    def init_post(self) -> None | NoReturn:     # DO NOT DELETE
        """
        GOAL
        ----
        additional user init method

        SPECIALLY CREATED FOR
        ---------------------
        serial devises resolve addresses
        """

    def start__gui_and_api(self) -> None:
        if self.API_SERVER__START:
            self.LOGGER.debug("starting api server")
            self.api_server = self.API_SERVER__CLS(data=self)
            self.api_server.start()

        # last execution --------------------------------------
        if self.GUI__START:
            self.LOGGER.debug("starting gui")
            self.gui = self.GUI__CLS(self)

            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            self.gui.run()
        elif self.API_SERVER__START:
            self.api_server.wait()  # it is ok!!!

    def slots_connect(self) -> None:
        self.signal__tp_start.connect(self.start)
        self.signal__tp_stop.connect(self.terminate)

        Base_TestCase.signals.signal__tc_state_changed.connect(self.post__tc_results)

    # =================================================================================================================
    @classmethod
    def stand__init(cls, item: Base_Stand = None) -> None:
        if item is not None:
            cls.STAND = item

    def tcs_clear(self) -> None:
        for tc_cls in self.STAND.TCSc_LINE:
            tc_cls.clear__cls()

    # =================================================================================================================
    def tp__startup(self) -> bool:
        """
        Overwrite with super! super first!
        """
        self.STAND.DEV_LINES("connect__only_if_address_resolved")  #, group="DUT")   # dont connect all here! only in exact TC!!!!????
        return True

    def tp__teardown(self) -> None:
        """
        Overwrite with super! super last!
        """
        if self.tc_active and (self.tc_active.STATE_ACTIVE__CLS == Enum_ProcessStateActive.STARTED or self.tc_active.result__teardown_cls is None):
            self.tc_active.terminate__cls()
        if not self._TC_RUN_SINGLE:
            self.tc_active = None

        self.STAND.DEV_LINES("disconnect")

        # self.signal__tp_finished.emit()   # dont place here!!!

    # =================================================================================================================
    def terminate(self) -> None:
        pass

        need_msg: bool = False
        if self.isRunning():
            need_msg = True
            super().terminate()

        # TERMINATE CHILDS!!! ---------------------
        # ObjectInfo(self.currentThread()).print()    # cant find childs!!!

        # finish active ----------------------------
        if self.tc_active:
            self.tc_active.terminate__cls()

        # finish ----------------------------
        self.tp__teardown()
        if need_msg:
            self.signal__tp_finished.emit()

    def run(self) -> None:
        self.LOGGER.debug("TP START")
        if self.tp__check_active():
            return

        cycle_count = 0
        while True:
            if not self._TC_RUN_SINGLE:
                self.tcs_clear()

            cycle_count += 1

            if self.tp__startup():
                # tcs_to_execute = list(filter(lambda x: not x.SKIP, self.STAND.TCSc_LINE))
                tcs_to_execute = self.STAND.TCSc_LINE

                if self._TC_RUN_SINGLE:
                    if not self.tc_active:
                        try:
                            self.tc_active = list(filter(lambda x: not x.SKIP, self.STAND.TCSc_LINE))[0]
                        except:
                            self.tc_active = self.STAND.TCSc_LINE[0]

                    self.tc_active.run__cls()

                else:
                    # MULTY
                    for tc_new in tcs_to_execute:     # TODO: place cls_prev into TcBaseCls!!! and clear on finish???
                        if tc_new.SKIP:
                            continue

                        # SWITCH/ROLL ---------
                        tc_prev = self.tc_active
                        self.tc_active = tc_new

                        tc_executed__result = self.tc_active.run__cls(cls_prev=tc_prev)

                        if tc_executed__result is False:
                            break

            # EXIT/STOP LAST TC
            # if self.tc_active and self.tc_active.STATE_ACTIVE__CLS != None:
            #     self.tc_active.teardown__cls()
            # FINISH TP CYCLE ---------------------------------------------------
            self.tp__teardown()
            self.LOGGER.debug("TP FINISH")

            # RESTART -----------------------------------------------------
            if not self.TP_RUN_INFINIT:
                break

            time.sleep(self.TP_RUN_INFINIT__TIMEOUT)

        # FINISH TP TOTAL ---------------------------------------------------
        self.signal__tp_finished.emit()

    # =================================================================================================================
    # FIXME: REF!!!
    def post__tc_results(self, tc_inst: Base_TestCase) -> None:
        # CHECK ------------------------------------------
        if not self.api_client or tc_inst.result is None:
            return

        # WORK ------------------------------------------
        try:
            tc_results = tc_inst.get__results()
        except:
            tc_results = {}

        body = {
            **self.STAND.stand__get_info__short(),
            **tc_results,
        }
        self.api_client.send(body=body)


# =====================================================================================================================
class TpInsideApi_Runner(TpApi_FastApi):
    """
    REASON:
    in windows Base_TestCase works fine by any variance GUI__START/API_SERVER__START
    in Linux it is not good maybe cause of nesting theme=Thread+Async+Threads

    so this is the attempt to execute correctly TP in Linux by deactivating GUI and using theme=Async+Threads

    UNFORTUNATELY: ITS NOT WORKING WAY for linux!!!
    """
    TP_CLS: type[TpManager] = TpManager

    def __init__(self, *args, **kwargs):

        self.TP_CLS.START__GUI_AND_API = False
        self.data = self.TP_CLS()

        super().__init__(*args, **kwargs)
        self.run()


# =====================================================================================================================
