import pytest

@pytest.fixture
def fixt1():
    print("[FIXT1]")
    return 111

@pytest.fixture(scope="session")
def fixt2():
    print("[FIXT2]")
    return 222

@pytest.mark.usefixtures("fixt1", "fixt2")
class TestSimple:
    def test_a(self):
        # FIXT1 И FIXT2 выполнятся автоматически,
        # но их значения здесь НЕ доступны.
        assert True

    def test_b(self, fixt2):
        # FIXT1 - выполнится еще раз!!!
        # FIXT2 - получит значение из раннего запуска
        assert fixt2 == 222

