from typing import *
import time
import json
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from base_aux.servers.m1_client_requests import *
from base_aux.aux_datetime.m1_datetime import *
from base_aux.loggers.m1_logger import *
from base_aux.path2_file.m4_fileattrs import *


# =====================================================================================================================
from .tc import Base_TestCase
from .devices import Base_Device, Base_Device, DevicesBreeder, _DevicesBreeder_Example
from .gui import Base_TpGui
from .api import TpApi_FastApi
from .tp_item import Base_TpItem


# =====================================================================================================================
class StandInfo:
    """
    GOAL
    ----
    separate info about real ArmStand from TpInfo
    """
    NAME: str = "[DEF] STAND NAME"
    DESCRIPTION: str = "[DEF] STAND DESCRIPTION"
    SN: str = "[DEF] STAND SN"


# =====================================================================================================================
class TpManager(Logger, QThread):
    signal__tp_start = pyqtSignal()
    signal__tp_stop = pyqtSignal()
    signal__tp_finished = pyqtSignal()
    signal__devs_detected = pyqtSignal()

    _signal__tp_reset_duts_sn = pyqtSignal()

    # SETTINGS ------------------------------------------------------
    TP_RUN_INFINIT: bool | None = None     # True - when run() started - dont stop!
    TP_RUN_INFINIT__TIMEOUT: int = 1

    _TC_RUN_SINGLE: bool | None = None

    START__GUI_AND_API: bool = True

    API_SERVER__START: bool = True
    API_SERVER__CLS: type[TpApi_FastApi] = TpApi_FastApi
    api_server: TpApi_FastApi

    GUI__START: bool = True
    GUI__CLS: type[Base_TpGui] = Base_TpGui

    api_client: Client_RequestsStack = Client_RequestsStack()   # todo: USE CLS!!! + add start

    DIRPATH_RESULTS: Union[str, Path] = "RESULTS"

    # AUX -----------------------------------------------------------
    STAND: StandInfo

    TP_ITEMS: 'TpItems'
    TP_ITEM: Base_TpItem
    DEVICES__BREEDER_CLS: type[DevicesBreeder]
    TCS_CLS: dict[type[Base_TestCase], bool]     # todo: RENAME TO clss!!!
    # {
    #     Tc1: True,
    #     Tc2: True
    # }

    # DEVICES__BREEDER_INST: list[Union[str, type[Base_Device]]]    # settings
    # [
    #     Dev1,
    #     Dev2
    # ]

    __tc_active: Optional[type[Base_TestCase]] = None
    progress: int = 0   # todo: use as property? by getting from TCS???

    # =================================================================================================================
    @property
    def tc_active(self) -> type[Base_TestCase] | None:
        return self.__tc_active

    @tc_active.setter
    def tc_active(self, value: type[Base_TestCase] | None) -> None:
        self.__tc_active = value

    def tp__check_active(self) -> bool:
        result = self.tc_active is not None and self.progress not in [0, 100]
        return result

    # =================================================================================================================
    def __init__(self):
        super().__init__()

        # results --------
        self.DIRPATH_RESULTS = pathlib.Path(self.DIRPATH_RESULTS)
        if not self.DIRPATH_RESULTS.exists():
            self.DIRPATH_RESULTS.mkdir(parents=True, exist_ok=True)

        self.tp_item__init()
        self.slots_connect()

        self.STAND = StandInfo()

        try:
            self.STAND = FileAttrs_Loader(target=self.STAND, keypath=("STAND",), filepath="STAND.ini").resolve()
        except:
            pass

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
        self._signal__tp_reset_duts_sn.connect(self.DEVICES__BREEDER_CLS._debug__duts__reset_sn)

        Base_TestCase.signals.signal__tc_state_changed.connect(self.post__tc_results)

    # =================================================================================================================
    def tp_item__init(self, item: Base_TpItem = None) -> None:
        if item is not None:
            self.TP_ITEM = item

        self.TCS_CLS = self.TP_ITEM.TCS_CLS
        self.DEVICES__BREEDER_CLS = self.TP_ITEM.DEV_BREEDER

        self.DEVICES__BREEDER_CLS.generate__objects()

        for tc_cls, using in self.TCS_CLS.items():
            tc_cls.SKIP = not using
            # tc_cls.clear__cls()   # let them use last states
            tc_cls.devices__apply(self.DEVICES__BREEDER_CLS)

    def tcs_clear(self) -> None:
        for tc_cls in self.TCS_CLS:
            tc_cls.clear__cls()

    # =================================================================================================================
    def tp__startup(self) -> bool:
        """
        Overwrite with super! super first!
        """
        self.progress = 1
        self.DEVICES__BREEDER_CLS.group_call__("connect__only_if_address_resolved")  #, group="DUT")   # dont connect all here! only in exact TC!!!!????
        return True

    def tp__teardown(self, progress: int = 100) -> None:
        """
        Overwrite with super! super last!
        """
        if self.tc_active and not self.tc_active.finished:
            self.tc_active.terminate__cls()
        if not self._TC_RUN_SINGLE:
            self.tc_active = None

        if progress is None:
            progress = 100
        self.progress = progress

        self.DEVICES__BREEDER_CLS.disconnect__cls()

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
        self.tp__teardown(0)
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
                tcs_to_execute = list(filter(lambda x: not x.SKIP, self.TCS_CLS))

                if self._TC_RUN_SINGLE:
                    if not self.tc_active:
                        if tcs_to_execute:
                            self.tc_active = tcs_to_execute[0]
                        else:
                            self.tc_active = self.TCS_CLS[0]

                    self.tc_active.run__cls()

                else:
                    # MULTY
                    for index, self.tc_active in enumerate(tcs_to_execute):     # TODO: place cls_prev into TcBaseCls!!! and clear on finish???
                        if index == 0:
                            tc_prev = None
                        else:
                            tc_prev = tcs_to_execute[index - 1]

                        if index == len(tcs_to_execute) - 1:
                            tc_next = None
                        else:
                            tc_next = tcs_to_execute[index + 1]

                        tc_executed__result = self.tc_active.run__cls(cls_prev=tc_prev, cls_next=tc_next)
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
    def get__info__stand(self) -> dict[str, Any]:
        # TODO: add into file! to separate real ARM/Stand!!!
        result = {
            "STAND.NAME": self.STAND.NAME,
            "STAND.DESCRIPTION": self.STAND.DESCRIPTION,
            "STAND.SN": self.STAND.SN,
        }
        return result

    def get__info__tp(self) -> dict[str, Any]:
        """
        get info/structure about stand/TP
        """
        TP_TCS = []
        for tc in self.TCS_CLS:
            TP_TCS.append(tc.get__info__tc())

        result = {
            **self.get__info__stand(),

            "TESTCASES": TP_TCS,
            # "TP_DUTS": [],      # TODO: decide how to use
            # [
            #     # [{DUT1}, {DUT2}, …]
            #     {
            #         DUT_ID: 1  # ??? 	# aux
            #         DUT_SKIP: False
            #     }
            # ]

            }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def get__results(self) -> dict[str, Any]:
        """
        get all results for stand/TP
        """
        TCS_RESULTS = {}
        for tc_cls in self.TCS_CLS:
            TCS_RESULTS.update({tc_cls: tc_cls.get__results__all()})

        result = {
            "STAND" : self.get__info__stand(),
            "TCS": TCS_RESULTS,
        }
        return result

    def save__results(self) -> None:
        name_prefix = str(DateTimeAux())
        for index in range(self.DEVICES__BREEDER_CLS.COUNT):
            result_i_short = {}
            result_i_full = {}
            for tc_cls in self.TCS_CLS:
                tc_inst = None
                try:
                    tc_inst: Base_TestCase = tc_cls.TCS__LIST[index]

                    tc_inst_result_full = tc_inst.get__results(add_info_dut=False, add_info_tc=False)
                    tc_inst_result_short = tc_inst_result_full["tc_result"]
                except:
                    tc_inst_result_short = None
                    tc_inst_result_full = None

                result_i_short.update({tc_cls.DESCRIPTION: tc_inst_result_short})
                result_i_full.update({tc_cls.DESCRIPTION: tc_inst_result_full})

            DUT = tc_inst.DEVICES__BREEDER_INST.DUT

            if not DUT.DEV_FOUND or not DUT.DUT_FW:
                continue

            dut_info = DUT.get__info__dev()
            result_dut = {
                "STAND": self.get__info__stand(),
                "DUT": dut_info,
                "RESULTS_SHORT": result_i_short,
                "RESULTS_FULL": result_i_full,
            }
            data_text = json.dumps(result_dut, indent=4, ensure_ascii=False)

            filename = f"{name_prefix}[{index}].json"
            filepath = pathlib.Path(self.DIRPATH_RESULTS, filename)
            filepath.write_text(data=data_text, encoding='utf-8')

    # -----------------------------------------------------------------------------------------------------------------
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
            **self.get__info__stand(),
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
