# =====================================================================================================================
"""
THIS IS THE REAL TESTPLAN!!!
"""
import json
import pathlib

# =====================================================================================================================
from .tc import TestCaseBase
from .devices import DutBase, DeviceBase, DevicesBreeder_WithDut, DevicesBreeder_Example
from .gui import TpGuiBase
from .api import TpApi_FastApi

import time
from typing import *
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal
from importlib import import_module

from base_aux.testplans import *
from base_aux.pyqt import *
from base_aux.classes import *
from base_aux.funcs import *
from base_aux.loggers import *
from base_aux.servers import *
from base_aux.privates import *
from base_aux.datetimes import *


# =====================================================================================================================
class Exx__TcsPathNotExists(Exception):
    pass


class Exx__TcItemNotFound(Exception):
    pass


class Exx__TcItemType(Exception):
    pass


class Exx__TcSettingsIncorrect(Exception):
    pass


# =====================================================================================================================
class TpMultyDutBase(Logger, QThread):
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

    STAND_NAME: Optional[str] = "stand_id__1"
    STAND_DESCRIPTION: Optional[str] = "stand_description"
    STAND_SN: Optional[str] = "StandSn"

    API_SERVER__START: bool = True
    API_SERVER__CLS: type[TpApi_FastApi] = TpApi_FastApi
    api_server: TpApi_FastApi

    GUI__START: bool = True
    GUI__CLS: type[TpGuiBase] = TpGuiBase

    api_client: Client_RequestsStack = Client_RequestsStack()   # todo: USE CLS!!! + add start

    # DIRPATH_TPS: Union[str, Path] = "TESTPLANS"
    DIRPATH_TCS: Union[str, Path] = "TESTCASES"
    DIRPATH_RESULTS: Union[str, Path] = "RESULTS"
    # DIRPATH_DEVS: Union[str, Path] = "DEVICES__BREEDER_INST"
    SETTINGS_BASE_NAME: Union[str, Path] = "SETTINGS_BASE.json"
    SETTINGS_BASE_FILEPATH: Path

    DEVICES__BREEDER_CLS: type[DevicesBreeder_WithDut] = DevicesBreeder_Example

    # AUX -----------------------------------------------------------
    TCS__CLS: dict[Union[str, type[TestCaseBase]], Optional[bool]] = {}     # todo: RENAME TO clss!!!
    # {
    #     Tc1: True,
    #     Tc2: True
    # }

    # DEVICES__BREEDER_INST: list[Union[str, type[DeviceBase]]]    # settings
    # [
    #     Dev1,
    #     Dev2
    # ]

    __tc_active: Optional[type[TestCaseBase]] = None
    tc_prev: Optional[type[TestCaseBase]] = None
    progress: int = 0   # todo: use as property? by getting from TCS???

    # =================================================================================================================
    @property
    def tc_active(self) -> type[TestCaseBase] | None:
        return self.__tc_active

    @tc_active.setter
    def tc_active(self, value: type[TestCaseBase] | None) -> None:
        if self.__tc_active and not self.__tc_active.SKIP:
            self.tc_prev = self.__tc_active
        self.__tc_active = value

    def tp__check_active(self) -> bool:
        result = self.tc_active is not None and self.progress not in [0, 100]
        return result

    # =================================================================================================================
    def __init__(self):
        super().__init__()
        # self.DIRPATH_TPS: Path = Path(self.DIRPATH_TPS)
        self.DIRPATH_TCS: Path = Path(self.DIRPATH_TCS)
        # self.DIRPATH_DEVS: Path = Path(self.DIRPATH_DEVS)
        self.SETTINGS_BASE_FILEPATH = self.DIRPATH_TCS.joinpath(self.SETTINGS_BASE_NAME)

        self.DIRPATH_RESULTS = pathlib.Path(self.DIRPATH_RESULTS)
        if not self.DIRPATH_RESULTS.exists():
            self.DIRPATH_RESULTS.mkdir(parents=True, exist_ok=True)

        if not self.DIRPATH_TCS.exists():
            msg = f"[ERROR] not found path {self.DIRPATH_TCS.name=}"
            print(msg)
            raise Exx__TcsPathNotExists(msg)

        self.DEVICES__BREEDER_CLS.generate__objects()

        self.tcs__reinit()
        self.slots_connect()

        if self.START__GUI_AND_API:
            self.start__gui_and_api()

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

        TestCaseBase.signals.signal__tc_state_changed.connect(self.post__tc_results)

    # =================================================================================================================
    def tcs__reinit(self) -> None:
        if not self.TCS__CLS:
            self._tcs__load()
        self._tcs__apply_classes()
        self._tcs__apply_settings()
        self._tcs__apply_devices()

    def _tcs__load(self) -> None:
        """
        for tests just overwrite
        :return:
        """
        self._tcs__load_from_files()

    def _tcs__load_from_files(self) -> None:
        self.TCS__CLS = {}
        for file in self.DIRPATH_TCS.glob("*.py"):
            if not file.stem.startswith("__"):
                self.TCS__CLS.update({file.stem: True})

    def _tcs__apply_classes(self) -> None:
        result = {}
        for item, using in self.TCS__CLS.items():
            # print(dir(TESTCASES))
            print(f"touch {self.DIRPATH_TCS} {item=}")
            if isinstance(item, str):   # filename
                # tc_cls = import_module(item, "TESTCASES").TestCase    # not working!
                # tc_cls = getattr(TESTCASES, item).TestCase      # not working
                tc_cls = None
                try:
                    tc_cls = import_module(f"{self.DIRPATH_TCS.name}.{item}").TestCase
                except Exception as exx:
                    msg = f"[WARN] no 'TestCase' class in file [{self.DIRPATH_TCS}/{item}] {exx=}"
                    print(msg)
                    continue
                if not tc_cls:
                    msg = f"[ERROR] file not found[{item=}] in /{self.DIRPATH_TCS}/"
                    raise Exx__TcItemNotFound(msg)
                tc_cls.NAME = item
            elif isinstance(type(item), type) and issubclass(item, TestCaseBase):
                tc_cls = item
                # msg = f"[ERROR] DONT USE IT!"
                # raise Exception(msg)
            else:
                msg = f"[ERROR] type is inconvenient [{item=}]"
                raise Exx__TcItemType(msg)

            tc_cls.SKIP = not using
            result.update({tc_cls: using})

        self.TCS__CLS = result

    def _tcs__apply_settings(self) -> None:
        for tc_cls in self.TCS__CLS:
            tc_cls.SETTINGS_FILES = [self.SETTINGS_BASE_FILEPATH, ]

            settings_tc_filepath = self.DIRPATH_TCS.joinpath(f"{tc_cls.NAME}.json")
            if settings_tc_filepath.exists():
                tc_cls.SETTINGS_FILES.append(settings_tc_filepath)
            else:
                print(f"{settings_tc_filepath=} NOT_EXISTS")
                pass

        # print(f"{tc_cls.SETTINGS=}")

    def _tcs__apply_devices(self) -> None:
        for tc in self.TCS__CLS:
            tc.devices__apply(self.DEVICES__BREEDER_CLS)

    def tcs_clear(self) -> None:
        for tc_cls in self.TCS__CLS:
            tc_cls.clear__cls()

    # =================================================================================================================
    def tp__startup(self) -> bool:
        """
        Overwrite with super! super first!
        """
        self.tc_prev = None
        self.progress = 1
        self.DEVICES__BREEDER_CLS.group_call__("connect__only_if_address_resolved")  #, group="DUT")   # dont connect all here! only in exact TC!!!!????
        return True

    def tp__teardown(self, progress: int = 100) -> None:
        """
        Overwrite with super! super last!
        """
        if self.tc_active and not self.tc_active.finished:
            self.tc_active.terminate__cls()
        if self.tc_prev and not self.tc_prev.finished:
            self.tc_prev.teardown__cls()
            self.tc_prev = None
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
                if self._TC_RUN_SINGLE:
                    if self.tc_active:
                        self.tc_active.run__cls(single=True)
                else:
                    for self.tc_active in filter(lambda x: not x.SKIP, self.TCS__CLS):  # TODO: place cls_prev into TcBaseCls!!! and clear on finish???
                        tc_executed__result = self.tc_active.run__cls(cls_prev=self.tc_prev)
                        if tc_executed__result is False:
                            break
            # if self.tc_prev:
            #     self.tc_prev.teardown__cls()
            if self.tc_active and self.tc_active.finished__cls is not None:
                self.tc_active.teardown__cls()
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
        result = {
            "STAND_NAME": self.STAND_NAME,
            "STAND_DESCRIPTION": self.STAND_DESCRIPTION,
            "STAND_SN": self.STAND_SN,
            "STAND_SETTINGS": TestCaseBase.settings_read(files=self.SETTINGS_BASE_FILEPATH),
        }
        return result

    def get__info__tp(self) -> dict[str, Any]:
        """
        get info/structure about stand/TP
        """
        TP_TCS = []
        for tc in self.TCS__CLS:
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
        for tc_cls in self.TCS__CLS:
            TCS_RESULTS.update({tc_cls: tc_cls.get__results__all()})

        result = {
            "STAND" : self.get__info__stand(),
            "TCS": TCS_RESULTS,
        }
        return result

    def save__results(self) -> None:
        name_prefix = DateTime().get_str()
        for index in range(self.DEVICES__BREEDER_CLS.COUNT):
            result_i = {}
            for tc_cls in self.TCS__CLS:
                tc_inst = None
                try:
                    tc_inst: TestCaseBase = tc_cls.TCS__LIST[index]
                    tc_inst_result = tc_inst.get__results(add_info_dut=False, add_info_tc=False)["tc_result"]
                except:
                    tc_inst_result = None

                result_i.update({tc_cls.DESCRIPTION: tc_inst_result})

            dut_info = tc_inst.DEVICES__BREEDER_INST.DUT.get__info__dev()
            result_dut = {
                "STAND": self.get__info__stand(),
                "DUT": dut_info,
                "RESULTS": result_i,
            }
            data_text = json.dumps(result_dut, indent=4, ensure_ascii=False)

            filename = f"{name_prefix}[{index}].json"
            filepath = pathlib.Path(self.DIRPATH_RESULTS, filename)
            filepath.write_text(data=data_text, encoding='utf-8')

    # -----------------------------------------------------------------------------------------------------------------
    def post__tc_results(self, tc_inst: TestCaseBase) -> None:
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
    in windows TestCaseBase works fine by any variance GUI__START/API_SERVER__START
    in Linux it is not good maybe cause of nesting theme=Thread+Async+Threads

    so this is the attempt to execute correctly TP in Linux by deactivating GUI and using theme=Async+Threads

    UNFORTUNATELY: ITS NOT WORKING WAY for linux!!!
    """
    TP_CLS: type[TpMultyDutBase] = TpMultyDutBase

    def __init__(self, *args, **kwargs):

        self.TP_CLS.START__GUI_AND_API = False
        self.data = self.TP_CLS()

        super().__init__(*args, **kwargs)
        self.run()


# =====================================================================================================================
