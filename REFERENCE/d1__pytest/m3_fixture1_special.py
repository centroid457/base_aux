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













# ---------------------------------------------------------------------------
# 6. request — доступ к данным запроса фикстуры/теста
# (используется ТОЛЬКО в фикстурах, НЕ в тестах!)
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

# ---------------------------------------------------------------------------
# 7. config (или pytestconfig) — конфиг pytest (session scope)
# ---------------------------------------------------------------------------
def test_check_config(config):
    # config.getoption("--verbose") и т.д.
    assert config.getoption("verbose") >= 0

# Можно безопасно использовать и в тестах, и в session-фикстурах.

# ---------------------------------------------------------------------------
# 8. cache — хранилище между сессиями (session scope)
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

