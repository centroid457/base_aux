import pytest


# ======================================================================================================================
# ПРОПУСК ВСЕГО КЛАССА
# с использованием фикстур
# ----------------------------------------------------------------------------------------------------------------------
# 1=setup_class=НЕЛЬЗЯ!!! потому что фикстуры на его уровне НЕПРИМЕНИМЫ!!!
# 2=setup_method=МОЖНО но это не чисто!!! проверка будет запускаться на каждом методе!
# 3=autouse method=такое же! - запуск на каждом тесте! даже session не помогает!
class TestCls_skipping():
    @pytest.fixture(scope="class", autouse=True)    # session тоже не помогает!!!!
    def skip_whole_class(self, request, pytestconfig):
        pytest.skip("класс пропущен целиком/но не совсем!")
    def test__1(self): pass
    def test__2(self): pass

# 4=---SKIPIF нельзя фикстуры НО имеет свой обьект pytestconfig внутри!!! - НИХРЕНА НЕ ИМЕЕТ!!!
# @pytest.mark.skipif(
#     pytestconfig.getoption("--skip-slow"), # EXCEPTION!
#     reason="--skip-slow указан",
# )
class TestCls_skipping2():
    @pytest.fixture(scope="session", autouse=True)
    def skip_whole_class(self, request, pytestconfig):
        pytest.skip("класс пропущен целиком")
    def test__1(self): pass
    def test__2(self): pass


# 5=ХУК=CONFIG=pytest_collection_modifyitems=ЧИСТЕЙШЕЕ РЕШЕНИЕ! но не совсем
def pytest_collection_modifyitems(config, items):
    some_condition = True
    for item in items:
        if "TestCls_skipping" in item.nodeid:
            item.add_marker(pytest.mark.skip(reason="TestCls_skipping"))


# ======================================================================================================================
