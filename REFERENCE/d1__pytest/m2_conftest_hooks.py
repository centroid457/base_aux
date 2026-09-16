# ======================================================================================================================
# 1 PYTEST ХУКИ: СПРАВОЧНИК ПО conftest.py
# =============================================================================
# Хуки — это точки расширения pytest. Они позволяют вмешиваться в процесс
# тестирования на разных этапах: инициализация, сбор тестов, выполнение,
# формирование отчётов и завершение сессии.
# Хуки определяются в файлах conftest.py (действуют на все тесты ниже по дереву)
# или в плагинах. Ниже — наиболее полезные хуки с примерами.

import pytest
import datetime


# ======================================================================================================================
# 1=ПОРЯДОК по уровню запуска
# ---------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    html_path = session.config.getoption('--html', default=None)
    pass


def pytest_unconfigure(config):      # реально после pytest-html запускается!
    """ПОСЛЕ ВСЕХ pytest_sessionfinish"""
    html_path = config.getoption('--html', default=None)


# ======================================================================================================================
# 2=НАСТРОЙКА порядка на одном уровне
@pytest.hookimpl(trylast=True)   # попытка запуска после хука pytest-html - не помогло!!!!
def pytest_sessionfinish(session, exitstatus):
    pass


# =============================================================================
# 31. ПОРЯДОК СРАБАТЫВАНИЯ ХУКОВ PYTEST (структура conftest.py)
# =============================================================================
# ---------------------------------------------------------------------------
# 1. ИНИЦИАЛИЗАЦИЯ И КОНФИГУРИРОВАНИЕ (до старта сессии)
# ---------------------------------------------------------------------------

def pytest_load_initial_conftests(early_config, parser, args):
    """Самый первый хук, вызывается для ранней загрузки conftest."""
    pass

def pytest_cmdline_preparse(config, args):
    """Анализ командной строки до добавления пользовательских опций."""
    pass

def pytest_addoption(parser, pluginmanager):
    """Добавление своих параметров командной строки."""
    pass

def pytest_configure(config):
    """Главный конфигурационный хук. Запускается после парсинга аргументов.
    Здесь можно регистрировать маркеры, добавлять свои on-действия."""
    pass

def pytest_sessionstart(session):
    """Начало сессии, до сбора тестов. Полезно для баннера."""
    pass

# ---------------------------------------------------------------------------
# 2. СБОР ТЕСТОВ (collection phase)
# ---------------------------------------------------------------------------

def pytest_ignore_collect(collection_path, path, config):
    """Можно запретить сбор файлов/папок (возвращает True)."""
    pass

def pytest_collect_file(file_path, parent, config):
    """Выбор файлов для сбора тестов (возвращает None, если не тестовый)."""
    pass

def pytest_pycollect_makeitem(collector, name, obj):
    """Решает, является ли объект тестом (функция/класс)."""
    pass

def pytest_generate_tests(metafunc):
    """Генерация параметризаций на лету."""
    pass

def pytest_make_parametrize_id(config, val, argname):
    """Формирование id для параметризованных тестов."""
    pass

def pytest_collection_modifyitems(session, config, items):
    """Модификация списка собранных тестов (сортировка, добавление маркеров)."""
    pass

# ---------------------------------------------------------------------------
# 3. ФИКСТУРЫ — настройка и завершение
# ---------------------------------------------------------------------------

def pytest_fixture_setup(fixturedef, request):
    """Вызывается перед настройкой фикстуры."""
    pass

def pytest_fixture_post_finalizer(fixturedef, request):
    """После завершающего кода фикстуры (yield/teardown)."""
    pass

# ---------------------------------------------------------------------------
# 4. ВЫПОЛНЕНИЕ ОТДЕЛЬНОГО ТЕСТА (цикл runtest)
# ---------------------------------------------------------------------------

def pytest_runtestloop(session):
    """Основной цикл запуска тестов. Обычно не переопределяют."""
    pass

def pytest_runtest_protocol(item, nextitem):
    """Протокол выполнения одного теста: setup, call, teardown."""
    pass

def pytest_runtest_setup(item):
    """Перед фикстурами и телом теста."""
    pass

def pytest_runtest_call(item):
    """Непосредственно вызов тела теста."""
    pass

def pytest_runtest_teardown(item, nextitem):
    """После тела теста, перед завершением фикстур."""
    pass

def pytest_runtest_makereport(item, call):
    """Создание отчёта о каждой фазе (setup, call, teardown).
    Обёртка hookwrapper, поэтому обычно:
    @pytest.hookimpl(hookwrapper=True)
    """
    pass

def pytest_report_teststatus(report, config):
    """Влияет на односимвольное отображение результата (., F, E)."""
    pass

# ---------------------------------------------------------------------------
# 5. ЗАВЕРШЕНИЕ СЕССИИ И ОТЧЁТЫ
# ---------------------------------------------------------------------------

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Дополнительная сводка после всех тестов."""
    pass

def pytest_sessionfinish(session, exitstatus):
    """Конец сессии. Можно выполнить очистку, отправить уведомления.
    Выполняется ДО того, как плагины вроде pytest-html закроют свои файлы."""
    pass

def pytest_unconfigure(config):
    """Вызывается ПОСЛЕ pytest_sessionfinish, когда все плагины завершили работу.
    Здесь уже безопасно переименовывать/перемещать сгенерированные отчёты."""
    pass

# ---------------------------------------------------------------------------
# ДОПОЛНИТЕЛЬНЫЕ ХУКИ (реагирование на события)
# ---------------------------------------------------------------------------

def pytest_exception_interact(node, call, report):
    """При падении теста с включённым --pdb."""
    pass

def pytest_keyboard_interrupt(excinfo):
    """При прерывании с клавиатуры."""
    pass

def pytest_internalerror(excinfo):
    """При внутренней ошибке pytest."""
    pass

# =============================================================================
# ВАЖНО:
# - Порядок, показанный выше, актуален для большинства ситуаций.
# - Если conftest.py есть на разных уровнях (корень, подпапка), то:
#   * Хуки с префиксом «pytest_» вызываются в порядке от ближайшего к файлу
#     до самого верхнего уровня (LIFO для хуков одного типа).
#   * Фикстуры, наоборот, ищутся от ближайшего conftest к самому дальнему.
# - Для точной последовательности можно вставить в каждый хук print и запустить
#   `pytest --co`.
# =============================================================================

























































# ======================================================================================================================
# ---------------------------------------------------------------------------
# 30.1 Инициализация и конфигурация
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Вызывается после создания объекта конфигурации, до сбора тестов.
    Можно зарегистрировать кастомные маркеры, добавить опции, изменить настройки."""
    config.addinivalue_line("markers", "smoke: быстрые проверки")

def pytest_addoption(parser):
    """Добавление своих опций командной строки."""
    parser.addoption("--my-env", action="store", default="dev", help="Окружение")

@pytest.fixture(scope="session")
def environment(request):
    return request.config.getoption("--my-env")

def pytest_sessionstart(session):
    """Перед началом выполнения тестов (после сбора). Можно вывести баннер."""
    print(f"\n=== Запуск тестов в окружении: {session.config.getoption('--my-env', 'dev')} ===")

# ---------------------------------------------------------------------------
# 30.2 Сбор тестов (collection)
# ---------------------------------------------------------------------------

def pytest_collection_modifyitems(session, config, items):
    """Позволяет изменить список собранных тестов: переупорядочить, отфильтровать,
    динамически добавить маркеры на основе имён/путей."""
    for item in items:
        if "slow" in item.name:
            item.add_marker(pytest.mark.slow)

# ---------------------------------------------------------------------------
# 30.3 Выполнение тестов (run test)
# ---------------------------------------------------------------------------

def pytest_runtest_setup(item):
    """Перед каждым тестом (после фикстур). Можно проверить условия и вызвать skip."""
    if item.get_closest_marker("skip_on_monday"):
        if datetime.datetime.now().weekday() == 0:
            pytest.skip("По понедельникам тест не запускается")

def pytest_runtest_call(item):
    """Вместо самого вызова теста. Можно обернуть в try/except.
    Не рекомендуется без крайней необходимости, лучше использовать фикстуры."""
    pass

def pytest_runtest_teardown(item, nextitem):
    """После выполнения теста (до фикстур teardown). Можно подчистить состояние."""
    pass

# ---------------------------------------------------------------------------
# 30.4 Отчёты и логирование
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Обёртка вокруг создания отчёта о каждом этапе (setup, call, teardown).
    Позволяет добавить дополнительную информацию в отчёт."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        # Сохранить скриншот или доп. данные для упавшего теста
        pass

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """После всех тестов, перед закрытием терминала. Можно вывести свою статистику."""
    terminalreporter.write_line(f"\nСводка: {terminalreporter.stats.get('passed', [])}")

def pytest_sessionfinish(session, exitstatus):
    """Самый конец сессии, после всех отчётов. Можно выполнить очистку, отправить уведомление."""
    print(f"\nСессия завершена с кодом {exitstatus}")

# ---------------------------------------------------------------------------
# 30.5 Взаимодействие с фикстурами
# ---------------------------------------------------------------------------

@pytest.hookimpl(trylast=True)
def pytest_fixture_setup(fixturedef, request):
    """Вызывается при настройке каждой фикстуры. Можно изменить поведение."""
    pass

# ---------------------------------------------------------------------------
# 30.6 Полный список хуков и их сигнатуры (основные категории)
# ---------------------------------------------------------------------------
# Bootstrapping hooks:
#   pytest_load_initial_conftests, pytest_cmdline_preparse, pytest_addoption,
#   pytest_configure, pytest_unconfigure, pytest_sessionstart
# Collection hooks:
#   pytest_collect_file, pytest_pycollect_makeitem, pytest_generate_tests,
#   pytest_make_parametrize_id, pytest_collection_modifyitems
# Test running hooks:
#   pytest_runtestloop, pytest_runtest_protocol, pytest_runtest_setup,
#   pytest_runtest_call, pytest_runtest_teardown
# Reporting hooks:
#   pytest_runtest_makereport, pytest_report_teststatus, pytest_terminal_summary
# Debugging/Interaction hooks:
#   pytest_exception_interact, pytest_internalerror, pytest_keyboard_interrupt

# Важно:
# - Хуки в conftest.py работают только для директории и поддиректорий,
#   где находится conftest.py. Можно иметь несколько conftest.py на разных уровнях.
# - Подробнее в официальной документации:
#   https://docs.pytest.org/en/stable/reference/reference.html#hooks


# ======================================================================================================================
