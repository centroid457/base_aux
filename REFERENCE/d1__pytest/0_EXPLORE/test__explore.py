import pytest


@pytest.fixture(autouse=True)
def fixture__return():
    """каждый scope тестов оборачивается"""
    # При запуске с -s будет видно сообщения до и после теста.
    print("\n\t[autouse] вкл verbose лог")
    return 123

def test__1():
    assert True

