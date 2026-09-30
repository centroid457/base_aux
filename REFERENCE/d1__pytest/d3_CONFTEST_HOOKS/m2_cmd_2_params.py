# =============================================================================
# 47. ПЕРЕДАЧА ПАРАМЕТРОВ В PYTEST ИЗ КОМАНДНОЙ СТРОКИ
# =============================================================================
import pytest
import os

# =============================================================================
# 47.1 ПОЛЬЗОВАТЕЛЬСКИЕ ОПЦИИ ЧЕРЕЗ pytest_addoption (рекомендуемый способ)
# =============================================================================
# Определяем свои опции в conftest.py: parser.addoption(...)

# 1=DEFINE =============================================================================================================
# ИМЕНА
# 1. Не используйте короткие имена --h, --v и т.п. — конфликт с встроенными.

# ЗНАЧЕНИЯ
# 2. Значения с пробелами требуют кавычек в командной строке.
# 3. При задании опции по умолчанию None в addoption и последующем
#    getoption("--uart") всегда проверяйте на None.
# 6. Для сложных структур (например, JSON) используйте --config-json='{...}'
#    и распарсите через json.loads.

# --- conftest.py + pytest_addoption(parser) ---
def pytest_addoption(parser):
    # *arg=УКАЗАНИЕ ИМЕНИ!!! без имени параметра в функции!!!
    parser.addoption(
        "--ssh-host",
        action="store",
        default=None,
        help="SSH-хост: имя или IP"
    )

    # 0=ОБЯЗАТЕЛЬНОЕ УКАЗАНИЕ параметра при запуске=тоесть если нет дефолтного???
    parser.addoption(
        "--pass_always",
        action="store_true",
        # default=False,
        help="обязательное указание"
    )

    # ACTION=
    # 1=FLAG=BOOL
    parser.addoption(
        "--debug-mode",
        action="store_true",
        default=False,
        help="Режим отладки"
    )

    # 2=ПРОИЗВОЛЬНОЕ ЗНАЧЕНИЕ
    # pytest --uart=com3
    parser.addoption(
        "--uart",
        action="store",
        default=None,
        help="UART-порт, например: com3 или ttyUSB0"
    )
    parser.addoption(
        "--ssh-host",
        action="store",
        default=None,
        help="SSH-хост: имя или IP"
    )

    # 3=APPEND=НЕСКОЛЬКО ЗНАЧЕНИЙ
    # pytest --debug-mode --tag=smoke --tag=fast
    # 5. Для передачи нескольких значений (например, нескольких портов)
    #    используйте action="append" и получайте список.
    parser.addoption(
        "--tag",
        action="append",
        default=[],
        help="Тег (можно указать несколько раз)"
    )

    # CHOICES=ВАРИАНТЫ ЗНАЧЕНИЙ
    # если указаны то сверяется пир получении!
    # если не совпадает - ошибка
    # pytest --channel=ssh
    parser.addoption(
        "--channel",
        action="store",
        default="uart",
        choices=["uart", "ssh", "usb"],
        help="Канал соединения"
    )

    # TYPE=преобразование типа
    # по умолчанию дает всегда STR!!!
    # Параметр type= может быть int, float, str или функцией.
    # Внутри: request.config.getoption("--timeout") вернёт указанный тип int.
    parser.addoption(
        "--timeout",
        action="store",
        type=int,
        default=5
    )


# 2=PASS/WRITE =========================================================================================================
# Запуск из консоли:
# pytest --uart=ttyUSB0 --channel=uart
# pytest --ssh-host=harvest05 --channel=ssh
# pytest --ssh-host=192.168.1.64 --channel=ssh

# 3=READING ============================================================================================================
# 1=из тестов - config.getoption(...). - лучше всегда использовать его!
def test__1(config):
    assert config.getoption("--opt1")


# 2=из фикстур - request.config.getoption(...) + config.getoption(...)
@pytest.fixture(scope="session")
def uart_port(request):
    return request.config.getoption("--uart")

@pytest.fixture(scope="session")
def ssh_host(request):
    return request.config.getoption("--ssh-host")

@pytest.fixture(scope="session")
def channel(request):
    return request.config.getoption("--channel")

def test__2(uart_port, ssh_host, channel):
    if channel == "uart":
        assert uart_port is not None, "Не задан --uart"
        print(f"\nРаботаем с UART: {uart_port}")
    elif channel == "ssh":
        assert ssh_host is not None, "Не задан --ssh-host"
        print(f"\nРаботаем по SSH: {ssh_host}")















# =============================================================================
# 47.2 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ (быстро, но неявно) чтение через фикстуры
# =============================================================================
# Подходит для значений, которые часто меняются в CI/CD.
# ЧТЕНИЕ ЧЕРЕЗ ФИКСТУРЫ

# Плюс: не требует правки pytest_addoption.
# Минус: не видно в pytest --help, легко забыть.

# Запуск:
# Linux/Mac:      TEST_CHANNEL=ssh TEST_UART=ttyUSB0 pytest
# Windows cmd:    set TEST_CHANNEL=ssh && set TEST_UART=ttyUSB0 && pytest
# PowerShell:     $env:TEST_CHANNEL="ssh"; $env:TEST_UART="ttyUSB0"; pytest

@pytest.fixture(scope="session")
def channel_from_env():
    return os.environ.get("TEST_CHANNEL", "uart")

@pytest.fixture(scope="session")
def uart_from_env():
    return os.environ.get("TEST_UART", None)



# =============================================================================
# 47.3 INI-ФАЙЛ (pytest.ini / pyproject.toml) — для значений по умолчанию
# =============================================================================
# [pytest]
# uart = com3
# ssh_host = harvest05
# channel = uart

def pytest_addoption(parser):
    parser.addini("uart", "UART-порт по умолчанию", default=None)
    parser.addini("ssh_host", "SSH-хост по умолчанию", default=None)
    parser.addini("channel", "Канал по умолчанию", default="uart")

@pytest.fixture(scope="session")
def uart_from_ini(request):
    # getini возвращает значение из ini или default
    return request.config.getini("uart")

@pytest.fixture(scope="session")
def channel_from_ini(request):
    return request.config.getini("channel")

# Запуск без параметров использует значения из ini.
# Переопределение через --uart=... имеет приоритет (если getvalue).
# Для комбинирования ini + option используйте config.getvalue():
def pytest_addoption(parser):
    parser.addini("uart", "UART-порт", default="com3")
    parser.addoption("--uart", action="store", default=None)

@pytest.fixture(scope="session")
def uart(request):
    # getvalue проверяет: command line option → ini → env → default
    return request.config.getvalue("uart")









# =============================================================================
# 47.4 ARGS=ПОЗИЦИОННЫЕ АРГУМЕНТЫ (свободные строки после опций) - НЕ ИСПОЛЬЗОВАТЬ
# =============================================================================
# Всё, что не распознано как опция, попадает в config.args (список строк).
# Подходит для простых случаев вида: pytest uart=com3 ssh=harvest05
# 4. Позиционные аргументы (config.args) могут конфликтовать с путями
#    к тестам — используйте префиксы --key=val.

def pytest_configure(config):
    # config.args — список строк, оставшихся после парсинга
    # Например, при запуске: pytest uart=com3 ssh=harvest05
    # config.args = ["uart=com3", "ssh=harvest05", "tests/"]
    pass

@pytest.fixture(scope="session")
def positional_params(request):
    params = {}
    for arg in request.config.args:
        if "=" in arg and not arg.startswith("/"):
            key, val = arg.split("=", 1)
            params[key] = val
    return params

def test_positional(positional_params):
    # Работает при запуске: pytest uart=com3 ssh=harvest05
    assert positional_params.get("uart") in ("com3", "ttyUSB0", None)

# ВАЖНО: позиционные аргументы также используются для указания путей
# к тестовым файлам. Поэтому лучше использовать префикс, например:
#   pytest --uart=com3 --ssh=harvest05
# Так надёжнее — не путается с путями к тестам.
















# =============================================================================
# 47.5 KWARGS=ИМЕНОВАННЫЕ АРГУМЕНТЫ В СТИЛЕ key=value (собственный парсер)
# =============================================================================
# Если хочется синтаксис --uart=com3 или --uart com3 — это встроено в
# addoption (action="store"). При желании можно принять стиль uart:com3
# и распарсить вручную.

def pytest_addoption(parser):
    parser.addoption("--pair", action="append", default=[],
                     help="Пары key:value (можно несколько)")

@pytest.fixture(scope="session")
def pairs(request):
    result = {}
    for p in request.config.getoption("--pair"):
        if ":" in p:
            k, v = p.split(":", 1)
            result[k] = v
    return result

def test_pairs(pairs):
    # Запуск: pytest --pair uart:com3 --pair ssh:harvest05
    assert "uart" in pairs

# =============================================================================
# 47.6 КОМБИНИРОВАННЫЙ ПОДХОД (рекомендуемый для вашей задачи)
# =============================================================================
# Один параметр --channel задаёт тип соединения, а --host принимает адрес.
# Для UART и SSH используется один и тот же --host.

def pytest_addoption(parser):
    parser.addoption("--channel", action="store", default=None,
                     choices=["uart", "ssh", "usb"],
                     help="Канал: uart, ssh, usb")
    parser.addoption("--host", action="store", default=None,
                     help="Адрес: com3, ttyUSB0, 192.168.1.64, harvest05")
    parser.addoption("--baud", action="store", default=115200, type=int,
                     help="Скорость UART (по умолчанию 115200)")

@pytest.fixture(scope="session")
def connection(request):
    channel = request.config.getoption("--channel")
    host = request.config.getoption("--host")
    baud = request.config.getoption("--baud")
    if not channel or not host:
        pytest.skip("Не заданы --channel и --host")
    return {"channel": channel, "host": host, "baud": baud}

def test_conn(connection):
    # Запуск: pytest --channel=uart --host=com3
    #         pytest --channel=ssh --host=harvest05
    #         pytest --channel=ssh --host=192.168.1.64
    assert connection["channel"] in ("uart", "ssh", "usb")


# =============================================================================
# 47.8 ЧАСТЫЕ ОШИБКИ И ВАЖНЫЕ ЗАМЕЧАНИЯ
# =============================================================================
# 7. Лучше всего комбинировать: значения по умолчанию в ini + override
#    через командную строку + fallback на переменные окружения.
#    Это даёт максимальную гибкость без потери прозрачности.


# =============================================================================
