import pytest


class TestCls_skipping():
    @pytest.fixture(scope="session", autouse=True)
    def skip_whole_class(self, request, pytestconfig):
        pytest.skip("класс пропущен целиком")

    def test__1(self):
        pass

    @pytest.mark.skip
    @pytest.mark.USER
    def test__2(self):
        pass

