# ======================================================================================================================
# 34. ФИКСТУРЫ PYTEST: SYSTEM - САМЫЕ ПОЛЕЗНЫЕ
# =============================================================================
# Встроенные фикстуры доступны всегда, их не нужно объявлять.
# Их можно использовать в тестовых функциях и в пользовательских фикстурах.
# Важно: у каждой есть своя область видимости (scope), и нарушение scope
# — частая ошибка. Ниже список ключевых фикстур с примерами и ограничениями.

import pytest
import os
import sys










# ======================================================================================================================
# 1. ВРЕМЕННЫЕ ФАЙЛЫ И КАТАЛОГИ (tmp_path, tmpdir)
# =============================================================================
def test_create_temp_file(tmp_path):
    """tmp_path — pathlib.Path к уникальной временной папке."""
    file = tmp_path / "data.txt"
    file.write_text("pytest")
    assert file.read_text() == "pytest"
    # После теста папка удаляется автоматически

def test_temp_dir_structure(tmp_path):
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "f1.txt").write_text("content")
    assert len(list(sub_dir.iterdir())) == 1

# -----------------------------------------------------------------------------
# ВАЖНО: tmp_path уникален для каждого теста (scope="function").
# Не сохраняйте абсолютные пути на диск за пределами теста – папка будет удалена.
# -----------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 1. tmp_path — временная папка (function scope)
# ---------------------------------------------------------------------------
def test_tmp_path_example(tmp_path):
    # tmp_path — pathlib.Path, уникальная папка, удаляется после теста
    file = tmp_path / "data.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"

# Ошибка: нельзя использовать tmp_path в фикстуре со scope != "function"
# (например, scope="class", "module", "session").
# Для session-уровня используйте tmp_path_factory.

# ---------------------------------------------------------------------------
# 2. tmp_path_factory — фабрика временных папок (session scope)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def session_dir(tmp_path_factory):
    # Можно создать одну папку на всю сессию
    dir = tmp_path_factory.mktemp("my_session_data")
    (dir / "config.ini").write_text("[config]")
    return dir

def test_session_uses_factory(session_dir):
    assert (session_dir / "config.ini").read_text() == "[config]"






# ======================================================================================================================
# ХРАНЕНИЕ
# ---------------------------------------------------------------------------
# . cache — хранилище между сессиями (session scope)
# ---------------------------------------------------------------------------
def test_cache_example(cache):
    cache.set("my_key", 123)
    assert cache.get("my_key", 0) == 123

# ---------------------------------------------------------------------------
# 9. record_property / record_testsuite_property — для отчётов
# ---------------------------------------------------------------------------
def test_recording(record_property):
    record_property("severity", "critical")

# Эти фикстуры function-scoped. record_testsuite_property — для сессионного уровня.






# ======================================================================================================================
# 2. ПЕРЕХВАТ ВЫВОДА: stdout, stderr, логи (capsys, caplog)
# =============================================================================
def noisy_function():
    print("Важное сообщение в stdout")
    import logging
    logging.warning("Предупреждение в логах")

def test_capture_stdout_and_logs(capsys, caplog):
    noisy_function()
    captured = capsys.readouterr()
    assert "Важное сообщение" in captured.out

    # Проверка логов (caplog перехватывает логи уровня WARNING и выше по умолчанию)
    assert "Предупреждение" in caplog.text
    assert caplog.records[0].levelname == "WARNING"

# ---------------------------------------------------------------------------
# 3. capsys — захват stdout и stderr (function scope)
# ---------------------------------------------------------------------------
def test_print_something(capsys):
    print("важное сообщение")
    captured = capsys.readouterr()
    assert "важное" in captured.out
    # Нельзя в session-фикстурах: получите ошибку.

# ---------------------------------------------------------------------------
# 4. caplog — захват логов (function scope)
# ---------------------------------------------------------------------------
import logging

def test_log_output(caplog):
    logging.warning("test warning")
    assert "test warning" in caplog.text
    # caplog также function-scoped, не работает в session-фикстурах.








# ======================================================================================================================
# 3. МАНКИ-ПАТЧИНГ (monkeypatch)
# =============================================================================
import os

def get_db_url():
    return os.environ.get("DATABASE_URL", "postgres://prod")

def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    assert get_db_url() == "sqlite:///:memory:"

def test_monkeypatch_attr(monkeypatch):
    # Подмена атрибута класса или модуля
    import json
    fake_dumps = lambda obj, **kw: "mocked_json"
    monkeypatch.setattr(json, "dumps", fake_dumps)
    assert json.dumps({"a": 1}) == "mocked_json"

# -----------------------------------------------------------------------------
# Частая ошибка: забыть, что monkeypatch действует только в рамках теста.
# После выхода из тестовой функции оригинальное окружение восстанавливается.
# -----------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 5. monkeypatch — подмена атрибутов/окружения (function scope)
# ---------------------------------------------------------------------------
def test_env_var(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")
    assert os.environ["APP_MODE"] == "test"
    # Восстанавливается после выхода из теста.












# ======================================================================================================================
# ENV
# ======================================================================================================================
# ---------------------------------------------------------------------------
# 1. request — доступ к данным запроса фикстуры/теста
# (используется ТОЛЬКО в фикстурах, НЕ в тестах!)
# ---------------------------------------------------------------------------
# request доступен ТОЛЬКО внутри фикстур (не в тестах).
# Ключевые поля и методы:

@pytest.fixture
def test_fields__request(request):
    # request.node         - тест, для которого выполняется фикстура (Function/Item)
    # request.config       - объект Config (см. выше)
    # request.session      - объект Session
    # request.function     - сама тестовая функция (callable)
    # request.cls          - класс, если тест в классе, иначе None
    # request.module       - модуль, в котором определён тест
    # request.param        - параметр при параметризации фикстуры (indirect)
    # request.fixturename  - имя текущей фикстуры

    # --- Методы ---
    # request.getfixturevalue(name) - получить значение другой фикстуры
    #   (полезно, когда фикстура должна динамически запрашивать другие)
    # request.addfinalizer(func) - добавить завершающую функцию (teardown)
    # request.applymarker(marker) - применить маркер к тесту

    if request.cls:
        print(f"Фикстура вызвана из класса {request.cls.__name__}")
    return "ok"


# ---------------------------------------------------------------------------
@pytest.fixture
def my_fixture(request):
    # request.node — текущий тест
    # request.config — конфиг pytest
    # request.param — параметр для параметризованной фикстуры
    # request.session — объект сессии
    if "slow" in request.node.name:
        pytest.skip("skip slow in this fixture")
    return 42

def test_with_my_fixture(my_fixture):
    assert my_fixture == 42
    # Не пытайтесь объявить def test_x(request): — вызовет ошибку!






# ----------------------------------------------------------------------------------------------------------------------
# 2. session — объект текущей тестовой сессии (session scope)
# ---------------------------------------------------------------------------
# Фикстура с scope='session', возвращает объект _pytest.main.Session.
# Доступна в тестах и в фикстурах (любого scope, так как сессия шире).
# Ключевые поля и методы:
def test_fields__session(session):
    # --- Основные атрибуты ---
    # session.items        - список всех собранных тестов (Node/Item)
    #                        ВАЖНО: только для чтения, не модифицировать!
    # session.config       - объект Config (см. ниже)
    # session.testscollected - количество собранных тестов
    # session.testsfailed  - количество упавших тестов (может быть неактуально
    #                        во время выполнения, использовать в хуках)
    # session.startdir     - начальная директория запуска pytest
    # session.session_id   - уникальный идентификатор сессии

    print(f"Всего тестов: {session.testscollected}")
    print(f"Директория запуска: {session.startdir}")

    # --- Методы ---
    # session.perform_collect()  - перезапустить сбор тестов (редко нужно)

# Рекомендация: session лучше всего использовать в хуках и в фикстурах
# с scope='session' для доступа к списку тестов или к конфигурации.

# ---------------------------------------------------------------------------
# Это встроенная фикстура, возвращающая объект Session.
# Доступна в фикстурах с scope='session' и в тестах (можно запрашивать напрямую).
# Позволяет получить доступ к собранным тестам (items), конфигурации и др.

def test_using_session(session):
    # session.items — список всех собранных тестов (после collection)
    # Но в момент вызова теста этот список уже может быть неактуален.
    # Лучше использовать в сессионных фикстурах:
    print(f"Всего тестов в сессии: {len(session.items)}")

@pytest.fixture(scope="session")
def global_data(session):
    # Например, можно сохранить информацию о старте сессии
    start_time = session.config.option.start_time  # если задали
    return {"start_time": start_time, "test_count": len(session.items)}

# ВАЖНО: не изменяйте session.items во время выполнения тестов,
# иначе можно сломать сборщик. Используйте session только для чтения.
# Для модификации списка тестов используйте хуки (pytest_collection_modifyitems).








# ----------------------------------------------------------------------------------------------------------------------
# 3. config (==pytestconfig) — конфиг pytest (session scope)
# ---------------------------------------------------------------------------
# Фикстура с scope='session' (также доступна как pytestconfig).
# Возвращает объект _pytest.config.Config.
def test_fields__config(config):
    # --- Параметры командной строки ---
    # config.getoption(name)     - значение опции, например config.getoption("verbose")
    # config.getini(name)        - значение из конфигурационного файла (pytest.ini)
    # config.known_args_namespace - пространство имен всех аргументов (argparse)
    verbose = config.getoption("verbose")

    # --- Пути ---
    # config.rootpath   - корень проекта (где найден pytest.ini/pyproject.toml)
    # config.inipath    - путь к файлу конфигурации (pytest.ini)
    # config.invocation_params.dir - директория, из которой запущен pytest
    print(f"Root: {config.rootpath}")

    # --- Кэш и плагины ---
    # config.cache       - объект Cache (межсессионное хранилище)
    # config.pluginmanager - менеджер плагинов (можно искать плагины)
    # config.stash       - временное хранилище для данных между хуками (словарь)
    #   Используйте config.stash["key"] = value для передачи данных между
    #   pytest_configure и другими хуками.

    # --- Добавление опций и маркеров (в хуках) ---
    # config.addinivalue_line(type, line) - добавить строку в конфиг
    #   Например, регистрация маркера: config.addinivalue_line("markers", "slow: ...")

# ВАЖНО: config доступен в любых фикстурах (scope не ограничивает, т.к. session).
# ---------------------------------------------------------------------------
def test_check_config(config):
    # config.getoption("--verbose") и т.д.
    assert config.getoption("verbose") >= 0

# Можно безопасно использовать и в тестах, и в session-фикстурах.








# =============================================================================
# ПРАВИЛА И ОГРАНИЧЕНИЯ
# =============================================================================
# - Нельзя использовать фикстуру с более узким scope в фикстуре с более широким.
#   Например, tmp_path (function) нельзя запросить в фикстуре scope="session".
#   Решение: tmp_path_factory для session, или изменить scope на function.
# - request доступен только в телах фикстур, не в тестах.
# - Все встроенные фикстуры, кроме request, работают в тестах напрямую.
# - Псевдонимы: config == pytestconfig (оба одинаковы).


# ======================================================================================================================
