import requests

from base_aux.base_types.m2_info import ObjectInfo
from base_aux.webs.d3_fastapi.d1_templates.m0_start2_py1_thread import ServerFastApi_Thread


# =====================================================================================================================
class Test__Server_FastApi:
    @classmethod
    def setup_class(cls):
        pass

        cls.server = ServerFastApi_Thread()
        cls.server.start()

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__types(self):
        # WORK ==============================================
        for url_i in ["return_types/int", "return_types/str", "return_types/dict"]:
            url = f"{self.server.ROOT}{url_i}"
            print(f"{url=}")
            response = requests.get(url=url, timeout=1)

        ObjectInfo(response).print()

    def test__post(self):
        # PREPARE ==============================================
        TEST_DATA = {'value': 1}

        # WORK ==============================================
        response = requests.post(url=f"{self.server.ROOT}post/dict", timeout=1, json=TEST_DATA)
        ObjectInfo(response).print()

        assert response.json() == TEST_DATA


# =====================================================================================================================
