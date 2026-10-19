# [conftest.py]
import pytest
from base_aux.base_types.m2_info import ObjectInfo

class Fixtures:
    @pytest.fixture(scope="session")
    def harvest(self):
        return None

    @pytest.fixture(scope="session")
    def transport(self, harvest):
        return "ssh"

    @pytest.fixture(scope="session")
    def device(self):
        return "harvest"



# [test.py]
import pytest
def test__1(harvest):
    assert harvest is None
