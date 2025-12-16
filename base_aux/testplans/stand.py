from pathlib import Path

from base_aux.path2_file.m4_fileattrs import *
from base_aux.aux_datetime.m2_datetime import *
from base_aux.testplans.devices_kit import DeviceKit
from base_aux.breeders.m3_table_inst import *


# =====================================================================================================================
class Base_Stand:
    NAME: str = "[DEF] STAND NAME"
    DESCRIPTION: str = "[DEF] STAND DESCRIPTION"
    SN: str = "[DEF] STAND SN"

    DIRPATH_RESULTS: Union[str, Path] = "RESULTS"

    DEV_LINES: DeviceKit

    # TCSc_LINE: dict[type, bool]   # TODO: use TableLine??? - NO! KEEP DICT! with value like USING! so we can use one
    TCSc_LINE: TableLine = TableLine()

    TIMESTAMP_START: DateTimeAux | None = None
    TIMESTAMP_STOP: DateTimeAux | None = None

    # =================================================================================================================
    def __init__(self) -> None:
        # PREPARE CLSs ========================================
        for tc_cls in self.TCSc_LINE:
            # init STAND -----------------------------------
            tc_cls.STAND = self

            # gen INSTS -----------------------------------
            tcs_insts = []
            for index in range(self.DEV_LINES.COUNT_COLUMNS):
                tc_i = tc_cls(index=index)
                tcs_insts.append(tc_i)
            tc_cls.TCSi_LINE = TableLine(*tcs_insts)    # TODO: move into TC_CLS

    # =================================================================================================================
    def stand__get_info__general(self) -> dict[str, Any]:
        result = {
            "STAND.NAME": self.NAME,
            "STAND.DESCRIPTION": self.DESCRIPTION,
            "STAND.SN": self.SN,

            "STAND.TIMESTAMP_START": str(self.TIMESTAMP_START),
            "STAND.TIMESTAMP_STOP": str(self.TIMESTAMP_STOP),
        }
        return result

    def stand__get_info__tcs(self) -> dict[str, Any]:
        """
        get info/structure about stand/TP
        """
        TP_TCS = []
        for tc_cls in self.TCSc_LINE:
            TP_TCS.append(tc_cls.tcc__get_info())

        result = {
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

    def stand__get_info__general_tcsc(self) -> dict[str, Any]:
        """
        get info/structure about stand/TP
===================================
some example
===================================
{
  "STAND.NAME": "[ОТК] БП800",
  "STAND.DESCRIPTION": "[DEF] STAND DESCRIPTION",
  "STAND.SN": "[DEF] STAND SN",
  "STAND.TIMESTAMP_START": "None",
  "STAND.TIMESTAMP_STOP": "None",
  "TESTCASES": [
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOff,HvOff,PsOff]присутствие БП",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOff,HvOff,PsOff]тест Заземления",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOff,HvOff,PsOff]проверка значений параметров ВЫКЛ",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOff,HvOff,PsOn]проверка значений параметров ВКЛ",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOn,HvOff,PsOff]тест PmBus",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOn,HvOff,PsOff]\nпроверка значений параметров ВЫКЛ",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc0,ExtOn,HvOff,PsOn]\nпроверка значений параметров ВКЛ",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOff]\nпроверка значений параметров в ВЫКЛ состоянии",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOn]\nпроверка значений параметров во ВКЛ состоянии",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOn]тест КЗ\nшины ожидания (STANDBY)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOn]тест КЗ\nшины главного питания (MAIN)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOn]тест нагрузочный\nшины ожидания (STANDBY)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc220,ExtOff,HvOn,PsOn]тест нагрузочный\nшины главного питания (MAIN)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc150,ExtOff,HvOn,PsOn]\nграница включения - нижняя (OFF)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc160,ExtOff,HvOn,PsOn]\nграница включения - нижняя (ON)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc250,ExtOff,HvOn,PsOn]\nграница включения - верхняя (ON)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    },
    {
      "TC_NAME": "",
      "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
      "TC_ASYNC": true,
      "TC_SKIP": null
    }
  ]
}
        """
        result = {
            **self.stand__get_info__general(),
            **self.stand__get_info__tcs(),
        }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def stand__get_results(self) -> dict[str, Any]:
        """
        get all results for stand/TP
===================================
some example
===================================
{
  "STAND": {
    "STAND.NAME": "[ОТК] БП800",
    "STAND.DESCRIPTION": "[DEF] STAND DESCRIPTION",
    "STAND.SN": "[DEF] STAND SN",
    "STAND.TIMESTAMP_START": "None",
    "STAND.TIMESTAMP_STOP": "None"
  },
  "TCS": {
    "": {       # NOTE: here is wrong! all TCS have no name! so all get balnk"" value and all are rewrite each other! need # FIXME
      "0": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 0,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=0\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "1": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 1,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=1\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "2": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 2,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=2\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "3": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 3,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=3\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "4": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 4,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=4\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "5": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 5,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=5\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "6": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 6,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=6\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "7": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 7,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=7\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "8": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 8,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=8\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      },
      "9": {
        "TC_NAME": "",
        "TC_DESCRIPTION": "[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)",
        "TC_ASYNC": true,
        "TC_SKIP": null,
        "DEV_FOUND": false,
        "INDEX": 9,
        "SKIP": null,
        "NAME": "PTB",
        "DESCRIPTION": "PTB for PSU",
        "SN": "",
        "FW": "",
        "MODEL": "",
        "DUT_SN": "",
        "DUT_FW": "",
        "DUT_MODEL": "",
        "timestamp_start": null,
        "tc_active": false,
        "tc_result_startup": false,
        "tc_result": null,
        "tc_details": {},
        "result__teardown": false,
        "timestamp_stop": null,
        "log": "INDEX=9\nDUT_SN=None\nDUT_ADDRESS=Enum__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID\ntc_skip_dut=None\nTC_NAME=\nTC_GROUP=Atc260\nTC_DESCRIPTION=[Atc260,ExtOff,HvOn,PsOn]\nграница включения - верхняя (OFF)\nTC_ASYNC=True\nTC_SKIP=None\nSETTINGS=====================\nINFO_STR__ADD_ATTRS===========\nATC_VOUT:260\nPTB_SET_EXTON:False\nPTB_SET_HVON:True\nPTB_SET_PSON:True\nPROGRESS=====================\nSTATE_ACTIVE__CLS=EnumAdj_ProcessStateActive.NONE\ntimestamp_start=None\ntimestamp_stop=None\nexc=None\n------------------------------------------------------------\nresult__startup=None\nresult=None\nresult__teardown=None\n------------------------------------------------------------\nDETAILS=====================\n"
      }
    }
  }
}
        """
        TCS_RESULTS = {}
        for tc_cls in self.TCSc_LINE:
            TCS_RESULTS.update({tc_cls.NAME: tc_cls.tcsi__get_results()})

        result = {
            "STAND" : self.stand__get_info__general(),
            "TCS": TCS_RESULTS,
        }
        return result

    def stand__save_results(self) -> None:
        for index in range(self.DEV_LINES.COUNT_COLUMNS):
            result_i_short = {}
            result_i_full = {}
            for tc_cls in self.TCSc_LINE:
                tc_inst = None
                try:
                    tc_inst: 'Base_TestCase' = tc_cls.TCSi_LINE[index]

                    tc_inst_result_full = tc_inst.tci__get_result(add_info_dut=False, add_info_tc=False)
                    tc_inst_result_short = tc_inst_result_full["tc_result"]
                except:
                    tc_inst_result_short = None
                    tc_inst_result_full = None

                result_i_short.update({tc_cls.DESCRIPTION: tc_inst_result_short})
                result_i_full.update({tc_cls.DESCRIPTION: tc_inst_result_full})

            DUT = tc_inst.DEV_COLUMN.DUT

            if not DUT.DEV_FOUND or not DUT.DUT_FW:
                continue

            dut_info = DUT.dev__get_info()
            result_dut = {
                "STAND": self.stand__get_info__general(),
                "DUT": dut_info,
                "RESULTS_SHORT": result_i_short,
                "RESULTS_FULL": result_i_full,
            }

            # data_text = json.dumps(result_dut, indent=4, ensure_ascii=False)

            filename = f"{self.TIMESTAMP_STOP}[{index}].json"
            filepath = pathlib.Path(self.DIRPATH_RESULTS, filename)

            tfile = TextFile(text=str(result_dut), filepath=filepath)
            tfile.pretty__json()
            tfile.write__text()


# =====================================================================================================================
# if __name__ == "__main__":
#     print(load__tcs())


# =====================================================================================================================
