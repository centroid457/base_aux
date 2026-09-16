# =============================================================================
# 49. ХРАНЕНИЕ ДАННЫХ МЕЖДУ ЗАПУСКАМИ PYTEST
# =============================================================================
# Задача: сохранять JSON-совместимые данные (последний адрес, настройки)
# так, чтобы они пережили перезапуск pytest, терминала и компьютера.
# Рассмотрим все варианты с их приоритетами и оговорками.

import os
import json
import tempfile
import pytest
from pathlib import Path


# ======================================================================================================================
# =============================================================================
# 49.1 CONFIG.CACHE — ВСТРОЕННЫЙ МЕХАНИЗМ (рекомендуемый по умолчанию)
# =============================================================================
# Куда пишет: <rootdir>/.pytest_cache/v/cache/
# Формат: JSON (сериализация через json.dumps).
# Переживает: перезапуск pytest, перезапуск терминала, перезапуск ОС (файл на диске).
# Минусы:
#   - привязан к конкретной папке проекта (rootdir);
#   - при очистке проекта (git clean -xfd, удаление .pytest_cache) данные теряются;
#   - при xdist запись из нескольких воркеров может конфликтовать;
#   - можно очистить командой pytest --cache-clear.

def test_cache_save(cache):
    cache.set("last_uart", "COM3")
    cache.set("last_baud", 115200)
    cache.set("last_settings", {"parity": "N", "stopbits": 1})

def test_cache_load(cache):
    last_uart = cache.get("last_uart", None)
    settings = cache.get("last_settings", {})
    assert isinstance(settings, dict)

# Путь к файлу:
def test_cache_location(cache):
    print(f"\nКеш: {cache._cachedir}")

# =============================================================================
# 49.2 ЯВНЫЙ ФАЙЛ В ДОМАШНЕЙ ДИРЕКТОРИИ (рекомендуемый для «последнего адреса»)
# =============================================================================
# Куда пишет: ~/.myproject_state.json (или $XDG_CONFIG_HOME).
# Переживает: всё, включая перезапуск ОС.
# Не теряется при очистке проекта.
# Работает при запуске из любой директории.
# Плюсы: явный контроль, переносимость между проектами.
# Минусы: нужно писать код чтения/записи вручную.

def get_state_path():
    home = Path.home()
    state_dir = home / ".pytest_state"
    state_dir.mkdir(exist_ok=True)
    return state_dir / "device_state.json"

def load_state():
    path = get_state_path()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_state(state: dict):
    path = get_state_path()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

@pytest.fixture(scope="session")
def persistent_state():
    state = load_state()
    yield state
    save_state(state)

def test_remember_address(persistent_state):
    persistent_state["last_address"] = "COM3"
    persistent_state["last_mode"] = "uart"

def test_use_last_address(persistent_state):
    addr = persistent_state.get("last_address", None)
    assert addr in ("COM3", None)

# =============================================================================
# 49.3 ФАЙЛ В ПАПКЕ ПРОЕКТА (например, .state.json в rootdir)
# =============================================================================
# Переживает: pytest, терминал, ОС.
# Минусы: файл может попасть в git (добавьте в .gitignore!),
#         может теряться при клонировании/очистке проекта.
# Плюс: удобно для проектных настроек, где данные логически принадлежат проекту.

def project_state_path():
    # config.rootdir доступен внутри фикстур через request.config
    return Path(".state.json")

def test_project_state_save():
    path = project_state_path()
    data = {"last_uart": "ttyUSB0"}
    path.write_text(json.dumps(data), encoding="utf-8")

# НЕ ЗАБУДЬТЕ в .gitignore: .state.json, .pytest_cache/

# =============================================================================
# 49.4 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ (os.environ) — НЕ РАБОТАЕТ между запусками
# =============================================================================
# ВАЖНО: os.environ живёт только в рамках текущего процесса и его потомков.
# При завершении терминала/сессии — теряется.
# При перезапуске ОС — тем более.
# НЕ подходит для хранения между запусками.
# Подходит только для:
#   - передачи значений от родительского процесса к дочернему;
#   - временной настройки в CI (set VAR=... && pytest);
#   - внутри одной сессии pytest (все воркеры xdist наследуют env родителя).

# Пример: установка переменной в текущей сессии (не сохраняется между запусками)
def test_env_not_persistent():
    os.environ["MY_TEMP"] = "value"
    # После завершения pytest переменная исчезнет

# Если хочется эмулировать «постоянную» переменную в Windows:
#   setx MY_VAR value       (Windows, сохраняется в реестре, но требует перезапуска процесса)
#   export в ~/.bashrc       (Linux, влияет на все новые терминалы, но не «между pytest»)
# Это внешние механизмы ОС, а не pytest.

# =============================================================================
# 49.5 ФАЙЛ В TEMP (tempfile.gettempdir())
# =============================================================================
# Переживает: pytest, терминал, перезапуск ОС — НЕТ.
# При перезагрузке системы /tmp (или %TEMP%) обычно очищается.
# Подходит: для сессионных данных, не требующих сохранения после ребута.

def temp_state_path():
    return Path(tempfile.gettempdir()) / "pytest_state.json"

def test_temp_state():
    path = temp_state_path()
    path.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")

# =============================================================================
# 49.6 ЛОКАЛЬНАЯ БАЗА ДАННЫХ (SQLite) — если данных много
# =============================================================================
# Переживает: всё (файл на диске).
# Плюсы: атомарность, конкурентный доступ, запросы.
# Минусы: избыточно для пары ключей.
# Хорошо подходит, если храните историю запусков устройств, телеметрию и т.п.

import sqlite3

def db_path():
    return Path.home() / ".pytest_state" / "state.db"

def init_db():
    path = db_path()
    path.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()
    return conn

# =============================================================================
# 49.7 СИСТЕМНЫЕ РЕЕСТРЫ / ПЛАНИРОВЩИКИ (экзотика)
# =============================================================================
# Windows Registry: reg add HKCU\Software\MyProject /v LastUart /d COM3
# Linux: dconf, gsettings
# Не рекомендуется — сложно переносимо, тяжело тестировать.

# =============================================================================
# 49.8 СВОДНАЯ ТАБЛИЦА
# =============================================================================
# Способ                    | Переживает ОС | Автоочистка | Формат | Приоритет
# --------------------------|---------------|-------------|--------|-----------
# config.cache              | ДА            | git clean   | JSON   | средний
# Файл в $HOME              | ДА            | редко       | JSON   | высокий
# Файл в rootdir            | ДА            | git clean   | JSON   | средний
# os.environ                | НЕТ           | всегда      | str    | низкий
# tempfile                  | НЕТ           | ОС ребут    | любой  | низкий
# SQLite в $HOME            | ДА            | редко       | BLOB   | высокий (много данных)
# Реестр/dconf              | ДА            | вручную     | свой   | очень низкий

# =============================================================================
# 49.9 РЕКОМЕНДАЦИИ ДЛЯ ВАШЕЙ ЗАДАЧИ (последний адрес, настройки)
# =============================================================================
# Оптимальное решение — комбинированное, с приоритетами источников:
#   1. Явные параметры командной строки (--host, --channel) — высший приоритет.
#   2. Переменные окружения (TEST_HOST) — для CI.
#   3. Значения по умолчанию из ini-файла.
#   4. Последнее сохранённое значение из файла в $HOME — самый низкий приоритет
#      (fallback).
#
# Это даёт: пользователь может каждый раз задавать параметры явно,
# но если забыл — подставится «последнее известное» значение.

# Пример реализации:

def get_state_file():
    return Path.home() / ".myproject" / "state.json"

def read_saved_state():
    path = get_state_file()
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def write_saved_state(state):
    path = get_state_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default=None,
                     help="Адрес устройства (перебивает сохранённое)")
    parser.addoption("--channel", action="store", default=None,
                     choices=["uart", "ssh"])

@pytest.fixture(scope="session")
def connection(request):
    saved = read_saved_state()
    host = (request.config.getoption("--host")
            or os.environ.get("TEST_HOST")
            or saved.get("last_host"))
    channel = (request.config.getoption("--channel")
               or os.environ.get("TEST_CHANNEL")
               or saved.get("last_channel", "uart"))
    if not host:
        pytest.skip("Нет адреса: задайте --host, TEST_HOST или сохраните ранее")
    return {"host": host, "channel": channel}

@pytest.fixture(scope="session", autouse=True)
def remember_connection(connection):
    yield
    # после успешного прогона сохраняем использованные значения
    saved = read_saved_state()
    saved["last_host"] = connection["host"]
    saved["last_channel"] = connection["channel"]
    write_saved_state(saved)

# Запуск:
#   pytest --host=COM3 --channel=uart          # явно
#   TEST_HOST=192.168.1.64 pytest --channel=ssh # через env
#   pytest                                       # возьмёт последнее сохранённое

# =============================================================================
# ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ
# =============================================================================
# - os.environ НЕ ХРАНИТ данные между запусками. Это временное значение
#   в текущем процессе.
# - config.cache стирается при git clean / удалении .pytest_cache.
# - Файл в $HOME — самый надёжный для «последнего адреса».
# - Всегда добавляйте файлы состояния в .gitignore, чтобы не коммитить
#   пользовательские настройки.
# - Для JSON используйте ensure_ascii=False, чтобы кириллица сохранялась читаемо.


# ======================================================================================================================
