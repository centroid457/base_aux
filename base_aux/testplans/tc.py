import datetime

from PyQt5.QtCore import QThread, pyqtSignal

from base_aux.aux_dict.m3_dict_attr1_simple import *
from base_aux.valid.m2_valid_base import *
from base_aux.pyqt.m0_signals import *
from base_aux.loggers.m1_logger import *

from base_aux.breeders.m3_table_inst import *
from base_aux.base_nest_dunders.m6_eq2_cls import *
from base_aux.base_statics.m4_enums import NestEq_Enum

from base_aux.testplans.tc_types import TYPING__RESULT_BASE, TYPING__RESULT_W_NORETURN, TYPING__RESULT_W_EXX
from base_aux.testplans.models import *
from base_aux.testplans.tp_item import *


# =====================================================================================================================
class _Base0_TestCase(Logger):
    """
    GOAL (SEPARATING)
    ----
    just to use in Signals before defining exact
    """
    pass


# =====================================================================================================================
class Enum_TcGroup_Base(NestEq_Enum):
    NONE = None


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_state_changed = pyqtSignal(_Base0_TestCase)


# =====================================================================================================================
class _Base1_TestCase(Nest_EqCls, _Base0_TestCase, QThread):
    LOG_ENABLE = False
    LOG_USE_FILE = False
    signals: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?

    # SETTINGS ------------------------------------
    NAME: str = ""      # set auto!
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    skip_tc_dut: Optional[bool] = None
    ASYNC: Optional[bool] = True
    # STOP_IF_FALSE_RESULT: Optional[bool] = None     # NOT USED NOW! MAYBE NOT IMPORTANT!!!

    # AUXILIARY -----------------------------------
    STATE_ACTIVE__CLS: Enum_ProcessStateActive = Enum_ProcessStateActive.NONE

    result__startup_cls: TYPING__RESULT_BASE | Enum_ProcessStateActive = None
    result__teardown_cls: TYPING__RESULT_BASE | Enum_ProcessStateActive = None

    TP_ITEM: Base_TpItem
    TCSi_LINE: TableLine = TableLine()

    # INSTANCE ------------------------------------
    INDEX: int
    SETTINGS: DictAttr = {}

    result__startup: TYPING__RESULT_W_EXX = None
    result__teardown: TYPING__RESULT_W_EXX = None

    _result: TYPING__RESULT_W_EXX = None
    _timestamp_last: Optional[datetime.datetime]
    timestamp_start: Optional[datetime.datetime]
    details: dict[str, Any]
    exx: Optional[Exception]

    # =================================================================================================================
    @property
    def DEV_COLUMN(self) -> TableColumn:
        return TableColumn(index=self.INDEX, lines=self.TP_ITEM.DEV_LINES)    # FIXME: use multiton!???

    # =================================================================================================================
    @classmethod
    @property
    def _EQ_CLS__VALUE(cls) -> Enum:
        """
        GOAL
        ----
        REDEFINE TO USE AS CMP VALUE
        """
        return Enum_TcGroup_Base.NONE

    # =================================================================================================================
    def __init__(self, index: int):
        self.INDEX = index
        self.clear()
        super().__init__()

    # =================================================================================================================
    @property
    def timestamp_last(self) -> datetime.datetime | None:
        """
        None - not even started
        float - was started!
            stable - finished
            UnStable - in active thread
        """
        if self._timestamp_last:
            return self._timestamp_last

        if self.isRunning():
            return datetime.datetime.now()

    @timestamp_last.setter
    def timestamp_last(self, value: datetime.datetime | None) -> None:
        self._timestamp_last = value

    # =================================================================================================================
    @classmethod
    def clear__cls(cls):
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.NONE
        cls.result__startup_cls = None
        cls.result__teardown_cls = None
        for tc in cls.TCSi_LINE:
            tc.clear()

    def clear(self) -> None:
        self.result__startup = None
        self.result__teardown = None
        self.result = None

        self.timestamp_last = None
        self.timestamp_start = None

        self.details = {}
        self.exx = None

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> TYPING__RESULT_W_EXX:
        return self._result

    @result.setter
    def result(self, value: TYPING__RESULT_W_EXX) -> None:
        self._result = value
        self.signals.signal__tc_state_changed.emit(self)
        if isinstance(value, Exception):
            self.DEV_COLUMN.DUT.final_result: bool = False

        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!
        # FIXME: FINISH!!!

    # # ---------------------------------------------------------
    # @classmethod
    # @property
    # def result__startup_cls(cls) -> Optional[bool]:
    #     return cls.__result__cls_startup
    #
    # @classmethod
    # @result__startup_cls.setter
    # def result__startup_cls(cls, value: Optional[bool]) -> None:
    #     cls.__result__cls_startup = value
    #     # cls.signals.signal__tc_state_changed.emit(cls)

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: dict[str, Any]) -> None:
        self.LOGGER.debug("")
        self.details.update(details)
        # self.signals.signal__tc_state_changed.emit(self)

    # =================================================================================================================
    @classmethod
    def run__cls(cls, cls_prev: type[Self] | None = None) -> None | bool:
        """run TC on batch duts(??? may be INDEXES???)
        preferred using in thread on upper level!

        :return:
            NONE - if SKIP for any reason
            True - need continue TP
            False - cant continue! need stop TP
        """
        # if not cls.TP_ITEM.DEV_LINES.DUT:
        #     return

        print(f"run__cls=START={cls.NAME=}/{cls.DESCRIPTION=}{'=' * 50}")

        # SKIP ---------------------------------------------------
        # if cls.SKIP:
        #     print(f"run__cls=SKIP={cls.NAME=}={'=' * 50}")
        #     return

        cls.clear__cls()
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.STARTED

        # FIXME: teardown not call!!!

        # TERDOWN PREV ----------------------------------------
        if cls_prev and not Nest_EqCls._eq_classes__check(cls, cls_prev):
            cls_prev.result__teardown_cls = cls_prev.teardown__cls()
            if cls_prev.result__startup_cls and cls_prev.result__teardown_cls is False:
                return False

        # STARTUP ----------------------------------------
        if cls_prev is not None and Nest_EqCls._eq_classes__check(cls, cls_prev):
            cls.result__startup_cls = cls_prev.result__startup_cls
        elif not Nest_EqCls._eq_classes__check(cls, cls_prev):
            cls.result__startup_cls = cls.startup__cls()

        # WORK ---------------------------------------------------
        if cls.result__startup_cls:
            # BATCH --------------------------
            for tc_inst in cls.TCSi_LINE:
                if tc_inst.skip_tc_dut:
                    continue

                print(f"run__cls=tc_inst.start({tc_inst.INDEX=})")
                tc_inst.start()
                if not cls.ASYNC:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inONEbyONE")
                    tc_inst.wait()

            # WAIT --------------------------
            if cls.ASYNC:
                for tc_inst in cls.TCSi_LINE:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inPARALLEL")
                    tc_inst.wait()

        # FINISH -------------------------------------------------
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.FINISHED
        print(f"[TC]FINISH={cls.NAME=}={'=' * 50}")
        return True

    def run(self) -> None:
        """
        GOAL
        ----
        start execution INSTANCE (in thread)
        """
        self.LOGGER.debug("run")

        # PREPARE --------
        self.clear()
        self.timestamp_start = datetime.datetime.now()
        if (
                not hasattr(self.DEV_COLUMN, "DUT")
                or
                self.DEV_COLUMN.DUT.SKIP
                or
                not self.DEV_COLUMN.DUT.DEV_FOUND
                or
                not self.DEV_COLUMN.DUT.connect()
        ):
            return

        # WORK --------
        self.LOGGER.debug("run-startup")
        if self.startup():
            try:
                self.LOGGER.debug("run-run_wrapped START")
                self.result = self.run__wrapped()
                if isinstance(self.result, Valid):
                    self.result.run__if_not_finished()

                self.LOGGER.debug(f"run-run_wrapped FINISHED WITH {self.result=}")
            except Exception as exx:
                self.result = False
                self.exx = exx
        self.LOGGER.debug("run-teardown")
        self.teardown()

    # =================================================================================================================
    @classmethod
    def startup__cls(cls) -> TYPING__RESULT_W_EXX:
        """before batch work
        """
        print(f"startup__cls")
        cls.result__startup_cls = Enum_ProcessStateActive.STARTED
        # cls.clear__cls()

        result = cls.startup__cls__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()
        print(f"{cls.result__startup_cls=}")
        cls.result__startup_cls = result
        return result

    def startup(self) -> TYPING__RESULT_W_EXX:
        self.LOGGER.debug("")

        result = self.startup__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()
        self.result__startup = result
        return result

    def teardown(self) -> TYPING__RESULT_W_EXX:
        self.LOGGER.debug("")
        self.timestamp_last = datetime.datetime.now()

        result = self.teardown__wrapped
        result = CallableAux(result).resolve_exx()
        if isinstance(result, Valid):
            result.run__if_not_finished()

        self.result__teardown = result
        return result

    @classmethod
    def teardown__cls(cls) -> TYPING__RESULT_W_EXX:
        print(f"run__cls=teardown__cls")

        if cls.STATE_ACTIVE__CLS == Enum_ProcessStateActive.STARTED:
            print(f"run__cls=teardown__cls=1")
            cls.result__teardown_cls = CallableAux(cls.teardown__cls__wrapped).resolve_exx()
            if isinstance(cls.result__teardown_cls, Valid):
                cls.result__teardown_cls.run__if_not_finished()

            if not bool(cls.result__teardown_cls):
                print(f"[FAIL]{cls.result__teardown_cls=}//{cls.NAME}")

        else:
            print(f"run__cls=teardown__cls=2")
            pass

        print(f"run__cls=teardown__cls=3")
        cls.STATE_ACTIVE__CLS = Enum_ProcessStateActive.FINISHED
        return cls.result__teardown_cls

    # =================================================================================================================
    @classmethod
    def terminate__cls(cls) -> None:
        for tc_inst in cls.TCSi_LINE:
            try:
                if tc_inst.isRunning() and not tc_inst.isFinished():
                    tc_inst.terminate()
            except:
                pass

        cls.teardown__cls()

    # -----------------------------------------------------------------------------------------------------------------
    def terminate(self) -> None:
        self.LOGGER.debug("")
        super().terminate()
        self.teardown()     # TODO: check order!!! place upper!

    # REDEFINE ========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass

    @classmethod
    def startup__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        return True

    def startup__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    def run__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    def teardown__wrapped(self) -> TYPING__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPING__RESULT_W_NORETURN:
        return True


# =====================================================================================================================
class _Info(_Base1_TestCase):
    """
    separated class for gen results/info by models!
    """
    INFO_STR__ADD_ATTRS: Iterable[str] = []

    @classmethod
    def get__info__tc(cls) -> dict[str, Any]:
        """
        get info/structure about TcCls
        """
        result = {
            "TC_NAME": cls.NAME,
            "TC_DESCRIPTION": cls.DESCRIPTION,
            "TC_ASYNC": cls.ASYNC,
            "TC_SKIP": cls.SKIP,
        }
        return result

    # =================================================================================================================
    def get__results_pretty(self) -> str:
        # FIXME: GET FROM INFO_GET????
        result = ""

        result += f"INDEX={self.INDEX}\n"
        result += f"DUT_SN={self.DEV_COLUMN.DUT.SN}\n"
        result += f"DUT_ADDRESS={self.DEV_COLUMN.DUT.ADDRESS}\n"
        result += f"tc_skip_dut={self.skip_tc_dut}\n"

        result += f"TC_NAME={self.NAME}\n"
        result += f"TC_GROUP={self._EQ_CLS__VALUE}\n"
        result += f"TC_DESCRIPTION={self.DESCRIPTION}\n"
        result += f"TC_ASYNC={self.ASYNC}\n"
        result += f"TC_SKIP={self.SKIP}\n"

        result += f"SETTINGS=====================\n"
        if self.SETTINGS:
            for name, value in self.SETTINGS.items():
                result += f"{name}:{value}\n"

        result += f"INFO_STR__ADD_ATTRS===========\n"
        if self.INFO_STR__ADD_ATTRS:
            for name in self.INFO_STR__ADD_ATTRS:
                if hasattr(self, name):
                    result += f"{name}:{getattr(self, name)}\n"

        result += f"PROGRESS=====================\n"
        result += f"STATE_ACTIVE__CLS={self.__class__.STATE_ACTIVE__CLS}\n"
        result += f"timestamp_start={self.timestamp_start}\n"
        result += f"timestamp_last={self.timestamp_last}\n"
        result += f"exx={self.exx}\n"

        result += "-"*60 + "\n"
        result += f"result__startup={self.result__startup}\n"
        result += f"result={self.result}\n"
        result += f"result__teardown={self.result__teardown}\n"
        result += "-"*60 + "\n"

        result += f"DETAILS=====================\n"
        for name, value in self.details.items():
            result += f"{name}={value}\n"
        return result

    # =================================================================================================================
    @classmethod
    def get__results__all(cls) -> dict[int, dict[str, Any]]:
        results = {}
        for tc_inst in cls.TCSi_LINE:
            results.update({tc_inst.INDEX: tc_inst.get__results()})
        return results

    # -----------------------------------------------------------------------------------------------------------------
    def get__results(self, add_info_dut: bool = True, add_info_tc: bool = True) -> dict[str, Any]:
        self.LOGGER.debug("")

        info_dut = {}
        try:
            if add_info_dut:
                info_dut = self.DEV_COLUMN.DUT.get__info__dev()
        except:
            pass

        info_tc = {}
        if add_info_tc:
            info_tc = self.get__info__tc()

        result = {
            **info_tc,
            **info_dut,

            # RESULTS
            "timestamp_start": self.timestamp_start and str(self.timestamp_start),
            "tc_active": self.isRunning(),
            "tc_result_startup": bool(self.result__startup),
            "tc_result": None if self.result is None else bool(self.result),
            "tc_details": self.details,
            "result__teardown": bool(self.result__teardown),
            "timestamp_last": self.timestamp_last and str(self.timestamp_last),
            "log": self.get__results_pretty().replace("\"", "").replace("\'", ""),
        }
        return result


# =====================================================================================================================
class Base_TestCase(_Info):
    """
    """


# =====================================================================================================================
