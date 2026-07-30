import pytest

# =====================================================================================================================
"""
ФАЙЛ
1. спокойно в тестовой файле!
2. conftest.py - просто по умолчанию - доступно на всех тестах!!!
"""


# =====================================================================================================================
# ГЛУБИНА
# 1. функция
# 2. МЕТОД класса тоже можно использовать как фикстуру
class Test_Example:
    @pytest.mark.dependency(depends=["gsm_responds"])
    def test_gsm_3__deep__dns(self, harvest):
        """Доступность ya.ru строго через GSM."""
        ping_ok = harvest.cmd_timeout__check_executed_success(
            f"ping -I {self.INTERFACE_NAME} -c 1 -W 2 ya.ru", timeout=5
        )
        assert ping_ok, f"ya.ru недоступен через {self.INTERFACE_NAME}"

    # ------------------------------------------------------------------
    # AT-команды (опционально, выполняются только при обнаружении порта)
    # ------------------------------------------------------------------
    @pytest.fixture(autouse=True)
    def _setup_at(self, harvest, request):
        """Определяет AT-порт перед AT-тестами, иначе пропускает их."""
        # Выполняется для каждого теста, но можно закешировать
        if request.node.get_closest_marker("skip_at"):
            return
        self.at_port = self._detect_at_port(harvest)
        if self.at_port is None:
            pytest.skip("AT-порт не обнаружен")

    @pytest.mark.dependency(depends=["gsm_responds"])
    def test_gsm_4__at__sim_ready(self, harvest):
        """AT+CPIN? -> READY."""
        out = harvest.send__at_command__raw("AT+CPIN?", port=self.at_port, timeout=2)
        assert "+CPIN: READY" in out, f"SIM не готова: {out}"


# =====================================================================================================================
