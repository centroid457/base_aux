from base_aux.versions.m3_derivatives import *
from base_aux.testplans.tp_manager import *
from base_aux.servers.m1_client_requests import *

from TESTPLANS.stands import Stands


# =====================================================================================================================
Version_Python().raise_if_not__check_ge("3.11", COMMENT="need greater equal!")


# =====================================================================================================================
class Client_RequestItem_Tp(Client_RequestItem):
    LOG_ENABLE = True

    RETRY_LIMIT = 1
    RETRY_TIMEOUT = 1

    HOST: str = "192.168.74.20"
    PORT: int = 8080
    ROUTE: str = "results"

    SUCCESS_IF_FAIL_CODE = True


class Client_RequestsStack_Tp(Client_RequestsStack):
    LOG_ENABLE = True
    REQUEST_CLS = Client_RequestItem_Tp


# =====================================================================================================================
class TpManager__Example(TpManager):
    LOG_ENABLE = True

    STANDS = Stands
    STAND = Stands.TP_PSU800

    API_SERVER__CLS = TpApi_FastApi
    api_client: Client_RequestsStack = Client_RequestsStack_Tp()  # FIXME: need fix post__results!!!!
    # api_client: Client_RequestsStack = None

    GUI__START = True
    API_SERVER__START = True

    # def post__tc_results(self, tc_inst: Base_TestCase) -> None:
    #     # CHECK ------------------------------------------
    #     if not self.api_client or tc_inst.result is None:
    #         return
    #
    #     # WORK ------------------------------------------
    #     # TODO: need CREATE good Model + generate it + use pydantic in MW + validate + add correct in SQL
    #     body = {
    #         "sn": tc_inst.DEVICES__BREEDER_INST.DUT.SN,
    #         "timestamp": tc_inst.timestamp_last,
    #         "factory_record": {
    #             "name": "name_stand",
    #             "stand_number": 111,
    #             "shift_number": 222,
    #         },
    #         "test_result": "PASS" if tc_inst.result else "FAIL",
    #         "components": {
    #             "component1": "comp1",
    #             "component2": "comp2",
    #         },
    #         "versions": {
    #             "board_version": "ver_board",
    #             "firmware_version": "ver_fir",
    #         },
    #         "test_log": {
    #             "test_name": "test1",
    #             "test_result": "PASS" if tc_inst.result else "FAIL",
    #             "parameters": {
    #                 "param1": 111,
    #                 "param2": 222,
    #             },
    #             "log_file": "log_file.txt",
    #         },
    #         "history_record": {
    #             "status": "Shipped",
    #             "other_databases": {
    #                 "database1": "DB1",
    #                 "database2": "DB2",
    #             },
    #         },
    #
    #         # **tc_inst.get__results().dict(),
    #     }
    #     print(body)
    #     self.api_client.send(body=body)


# =====================================================================================================================
class TpInsideApi_Runner__example(TpInsideApi_Runner):
    TP_CLS = TpManager__Example


# =====================================================================================================================
def run_direct():
    TpManager__Example()


def run_over_api():
    TpInsideApi_Runner__example()


# =====================================================================================================================
if __name__ == "__main__":
    run_direct()
    # run_over_api()


# =====================================================================================================================
