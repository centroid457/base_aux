import pytest


# ======================================================================================================================
# ТЕСТЫ В КЛАССАХ: организация, setup/teardown, фикстуры
# ----------------------------------------------------------------------------------------------------------------------
class Test__ResourceLevel1_Class:
    """Класс с setup_class/teardown_class (scope='class')."""
    # ----------------------------------------------------------
    # Эти методы вызываются один раз для всего класса
    @classmethod
    def setup_class(cls):
        print("\n\t[setup_class] Подключение к общему ресурсу")
        """
        напрямую передать фикстуру в метод setup_class нельзя, 
        потому что это @classmethod, а pytest внедряет фикстуры только в обычные методы тестовых классов 
        (и в методы с self). 
        Аргументы, кроме cls, в setup_class не принимаются.
        """
        cls.shared_resource = ["resource"]

    @classmethod
    def teardown_class(cls):
        print("\t[teardown_class] Освобождение ресурса")
        cls.shared_resource = None

    # ----------------------------------------------------------
    def test__shared_resource_exists(self):
        assert self.shared_resource == ["resource"]
        self.shared_resource.append("modified")
        assert len(self.shared_resource) == 2

    def test__append_to_shared_resource(self):
        assert len(self.shared_resource) == 2


# ----------------------------------------------------------------------------------------------------------------------
class Test__ResourceLevel2_Method:
    # Методы setup/teardown выполняются для каждого теста (аналогично фикстурам function scope)
    # ----------------------------------------------------------
    def setup_method(self, method):
        print(f"\n\t[setup] {method.__name__}")
        self.user_data = {"name": "guest", "authenticated": False}

    def teardown_method(self, method):
        print(f"\t[teardown] {method.__name__}")
        self.user_data.clear()

    # ----------------------------------------------------------
    def test__initial_state(self):
        """Пользователь не аутентифицирован по умолчанию."""
        assert self.user_data["authenticated"] is False

    # Можно использовать фикстуры: они вставляются после self
    def test__login_with_fixture(self, simple_data):
        """simple_data определена в этом же модуле (см. раздел 3)."""
        self.user_data["name"] = simple_data["name"]
        self.user_data["authenticated"] = True
        assert self.user_data["name"] == "Alice"
        assert self.user_data["authenticated"] is True



# ======================================================================================================================
# ПРОПУСК ВСЕГО КЛАССА
# с использованием фикстур
# ----------------------------------------------------------------------------------------------------------------------
# 1=setup_class=НЕЛЬЗЯ!!! потому что фикстуры на его уровне НЕПРИМЕНИМЫ!!!
# 2=setup_method=МОЖНО но это не чисто!!! проверка будет запускаться на каждом методе!
# 3=autouse method=такое же! - запуск на каждом тесте! даже session не помогает!
class TestCls_skipping():
    @pytest.fixture(scope="class", autouse=True) # session тоже не помогает!!!!
    def skip_whole_class(self, request, pytestconfig):
        pytest.skip("класс пропущен целиком/но не совсем!")

    def test__1(self):
        pass

    def test__2(self):
        pass

# 4=---SKIPIF нельзя фикстуры НО имеет свой обьект pytestconfig внутри!!! - НИХРЕНА НЕ ИМЕЕТ!!!
import pytest


# @pytest.mark.skipif(
#     pytestconfig.getoption("--skip-slow"), # EXCEPTION!
#     reason="--skip-slow указан",
# )
class TestCls_skipping2():
    @pytest.fixture(scope="session", autouse=True)
    def skip_whole_class(self, request, pytestconfig):
        pytest.skip("класс пропущен целиком")

    def test__1(self):
        pass

    def test__2(self):
        pass


# 5=ХУК=CONFIG=pytest_collection_modifyitems=ЧИСТЕЙШЕЕ РЕШЕНИЕ!
def pytest_collection_modifyitems(config, items):
    some_condition = True
    for item in items:
        if "TestCls_skipping" == item.nodeid:
            item.add_marker(pytest.mark.skip(reason="..."))


# ======================================================================================================================
# ВАЖНО: использование @pytest.mark.usefixtures для автоматического внедрения
# фикстур в класс без явного указания в аргументах каждого метода.
# ----------------------------------------------------------------------------------------------------------------------
@pytest.fixture
def resource_autouse():
    print("\n\t[Фикстура resource_autouse] открываем ресурс")
    res = {"state": True}
    yield res  # тест выполняется здесь
    print("\n\t[Фикстура resource_autouse] закрываем ресурс")
    res["state"] = False


# ----------------------------------------------------------------------------------------------------------------------
class Test__Inject0_DirectPass_IntoMethods:
    def test__correct(self, resource_autouse):
        assert "state" in resource_autouse


# ----------------------------------------------------------------------------------------------------------------------
# использовать обычный метод setup_method для запроса фикстур.
class Test__Inject1_ManualFixture:
    def setup_method(self, method, resource_autouse):
        self.resource = resource_autouse

    def test__check_resource(self):
        assert self.resource["state"] is True


# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.usefixtures("resource_autouse")
class Test__Inject2_AutoFixture:
    """Фикстура 'resource_autouse' будет доступна во всех тестах как self.resource."""

    # Чтобы фикстура стала атрибутом self, нужно объявить её в методе
    # или использовать хитрый приём – объявить фикстуру и сохранить её в self.
    # Просто @usefixtures не делает фикстуру атрибутом, но можно запросить её.
    # Покажем правильный паттерн: ручной запрос через request fixture.

    # ----------------------------------------------------------
    @pytest.fixture(autouse=True)
    def _inject_resource(self, resource_autouse):
        """Фикстура, которая внедрит 'resource_autouse' в self."""
        self.resource = resource_autouse

    # ----------------------------------------------------------
    def test__check_resource(self):
        assert self.resource["state"] is True
        self.resource["state"] = False

    def test__resource_can_be_used(self):
        assert "state" in self.resource


# ======================================================================================================================
