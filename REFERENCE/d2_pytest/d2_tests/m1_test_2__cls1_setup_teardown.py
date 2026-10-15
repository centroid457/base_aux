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
