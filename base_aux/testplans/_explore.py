from base_aux.testplans.main import  *
from base_aux.servers.m1_client_requests import *

from base_aux.testplans.DEVICES.load__example import DevicesBreeder__Example


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
class Tp__Example(TpMultyDutBase):
    LOG_ENABLE = True
    api_client: Client_RequestsStack = Client_RequestsStack_Tp()  # FIXME: need fix post__results!!!!
    # api_client: Client_RequestsStack = None

    DEVICES__BREEDER_CLS = DevicesBreeder__Example
    API_SERVER__CLS = TpApi_FastApi

    GUI__START = True
    API_SERVER__START = True


# =====================================================================================================================
class TpInsideApi_Runner__example(TpInsideApi_Runner):
    TP_CLS = Tp__Example


# =====================================================================================================================
def run_direct():
    Tp__Example()


def run_over_api():
    TpInsideApi_Runner__example()


# =====================================================================================================================
if __name__ == "__main__":
    run_direct()
    # run_over_api()


# =====================================================================================================================
