from typing import *
from pathlib import Path

from base_aux.testplans.devices import *
from base_aux.aux_attr.m4_kits import *
from base_aux.path2_file.m4_fileattrs import *
from base_aux.aux_datetime.m1_datetime import *


# =====================================================================================================================
class Base_Stand:
    NAME: str = "[DEF] STAND NAME"
    DESCRIPTION: str = "[DEF] STAND DESCRIPTION"
    SN: str = "[DEF] STAND SN"

    DIRPATH_RESULTS: Union[str, Path] = "RESULTS"

    DEV_LINES: DeviceKit

    # TCSc_LINE: dict[type, bool]   # TODO: use TableLine??? - NO! KEEP DICT! with value like USING! so we can use one
    TCSc_LINE: TableLine = TableLine()

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
    def stand__get_info__short(self) -> dict[str, Any]:
        result = {
            "STAND.NAME": self.NAME,
            "STAND.DESCRIPTION": self.DESCRIPTION,
            "STAND.SN": self.SN,
        }
        return result

    def stand__get_info__full(self) -> dict[str, Any]:
        """
        get info/structure about stand/TP
        """
        TP_TCS = []
        for tc_cls in self.TCSc_LINE:
            TP_TCS.append(tc_cls.tcc__get_info())

        result = {
            **self.stand__get_info__short(),

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
    def stand__get_results(self) -> dict[str, Any]:
        """
        get all results for stand/TP
        """
        TCS_RESULTS = {}
        for tc_cls in self.TCSc_LINE:
            TCS_RESULTS.update({tc_cls: tc_cls.tcsi__get_results()})

        result = {
            "STAND" : self.stand__get_info__short(),
            "TCS": TCS_RESULTS,
        }
        return result

    def stand__save_results(self) -> None:
        name_prefix = str(DateTimeAux())
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
                "STAND": self.stand__get_info__short(),
                "DUT": dut_info,
                "RESULTS_SHORT": result_i_short,
                "RESULTS_FULL": result_i_full,
            }

            # data_text = json.dumps(result_dut, indent=4, ensure_ascii=False)

            filename = f"{name_prefix}[{index}].json"
            filepath = pathlib.Path(self.DIRPATH_RESULTS, filename)

            tfile = TextFile(text=str(result_dut), filepath=filepath)
            tfile.pretty__json()
            tfile.write__text()


# =====================================================================================================================
# if __name__ == "__main__":
#     print(load__tcs())


# =====================================================================================================================
