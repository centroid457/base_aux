import pytest


class TestDetect:
    @pytest.fixture(scope="session", autouse=True)
    def test_detect(self):
        print(123)
        print(123)
        print(123)
        print(123)
        print(123)
        print(123)


def test__1():
    assert True

