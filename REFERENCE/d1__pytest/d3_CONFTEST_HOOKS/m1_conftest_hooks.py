# ======================================================================================================================
# 1 PYTEST ХУКИ: СПРАВОЧНИК ПО conftest.py
# =============================================================================
# ХУКИ — это точки расширения pytest.
# Они позволяют вмешиваться в процесс тестирования на разных этапах:
# инициализация, сбор тестов, выполнение, формирование отчётов и завершение сессии.
# Хуки определяются в файлах conftest.py (действуют на все тесты ниже по дереву)
# или в плагинах.

# КУДА КЛАСТЬ
# только в CONFTEST.PY
# ЕСЛИ ПОМЕСТИТЬ ПРОСТО В ТЕСТЫ - РАБОТАТЬ НЕ БУДЕТ!!!


import pytest
import datetime
import os


# ======================================================================================================================
# 1=ПОРЯДОК по уровню запуска
# ---------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    """Самый конец сессии, после всех отчётов. Можно выполнить очистку, отправить уведомление."""
    print(f"\nСессия завершена с кодом {exitstatus}")
    html_path = session.config.getoption('--html', default=None)
    pass


def pytest_unconfigure(config):      # реально после pytest-html запускается!
    """ПОСЛЕ ВСЕХ pytest_sessionfinish"""
    """Вызывается ПОСЛЕ pytest_sessionfinish, когда все плагины завершили работу.
    Здесь уже безопасно переименовывать/перемещать сгенерированные отчёты."""

    print(f"[pytest.STAGE.pytest_unconfigure]START")
    html_path = config.getoption('--html', default=None)
    print(f"[pytest.STAGE.pytest_unconfigure]FINISH")


# ======================================================================================================================
# 2=НАСТРОЙКА порядка на одном уровне
@pytest.hookimpl(trylast=True)   # попытка запуска после хука pytest-html - не помогло!!!!
def pytest_sessionfinish(session, exitstatus):
    """Конец сессии. Можно выполнить очистку, отправить уведомления.
    Выполняется ДО того, как плагины вроде pytest-html закроют свои файлы."""
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
    """Добавление своих параметров командной строки. для парсинга
    """
    parser.addoption("--my-env", action="store", default="dev", help="Окружение")

def pytest_configure(config):
    """Главный конфигурационный хук. Запускается после парсинга аргументов.
    Здесь можно регистрировать маркеры, добавлять свои on-действия.

    Вызывается после создания объекта конфигурации, до сбора тестов.
    Можно
    1. зарегистрировать кастомные маркеры,
    2. опции  - изменить значения, добавить новые,
    3. изменить настройки.
    """
    config.addinivalue_line("markers", "smoke: быстрые проверки")

    # CHANGE OPTIONS
    # Если пользователь не указал --html, ставим свой путь
    if not config.option.htmlpath:
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(reports_dir, "_report_results.html")


def pytest_sessionstart(session):
    """Начало сессии, до сбора тестов. Полезно для баннера.

    Перед началом выполнения тестов (после сбора). Можно вывести баннер.
    """
    print(f"\n=== Запуск тестов в окружении: {session.config.getoption('--my-env', 'dev')} ===")

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
    """Модификация списка собранных тестов (сортировка, добавление маркеров).

    "Позволяет изменить список собранных тестов: переупорядочить, отфильтровать,
    динамически добавить маркеры на основе имён/путей.

    item.own_markers - маркеры непосредственные на конечном тесте!!!
    """
    skip_marker = pytest.mark.skip(reason="reason")

    for item in items:
        # ITEMS - показывает только конечные тесты! обобщенные Классы - не в счет!!!

        # 1=MARKERS practice -----------------------------------------------------
        if (
            # 1=маркеры непосредственно на конечном тесте! сработает только если маркер собственный - прямо на методе!
            (pytest.mark.PRE_SKIP__CHECK in item.own_markers)
            or
            # 2=маркеры по всей иерархии = директория+файл+класс+непосредственныйТест!
            item.get_closest_marker("PRE_SKIP__CHECK")      # ЛУЧШЕЕ!!!
            or
            any(m.name == "PRE_SKIP__CHECK" for m in item.iter_markers())      # сложноватое!!!
        ):
            if config.getoption("--pre_skip", default=None):
                item.add_marker(skip_marker)


            if config.getoption("--pre_skip", default=None):
                item.add_marker(skip_marker)

        # 2=NAMES checks
        if "slow" in item.name:
            item.add_marker(pytest.mark.slow)

        if "TestCls_skipping" in item.nodeid:
            item.add_marker(skip_marker)

    """
    ITEM
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<Function test__2>
repr(SOURCE)=<Function test__2>
type(SOURCE)=<class '_pytest.python.Function'>
mro(SOURCE)=['Function', 'PyobjMixin', 'Item', 'Node', 'ABC', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.SKIP__BUILD_IN=True
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=[]
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'abort', 'commit', 'checkout', 'attach', 'detach', 'connect', 'disconnect', 'exec', 'exec_', 'pyqtConfigure', 'run', 'start', 'wait', 'pause', 'continue', 'join', 'terminate', 'quit', 'stop', 'communicate', 'pop', 'popleft', 'put', 'input', 'extend', 'extendleft', 'append', 'appendleft', 'update', 'add', 'insert', 'reverse', 'rotate', 'sort', 'load', 'reload', 'dump', 'move', 'remove', 'rename', 'remove', 'resize', 'restart', 'reload', 'unpausebreakpointhook', 'hook']
self.MAX_LINE_LEN=200
self.MAX_ITER_ITEMS=5
----------SKIPPED_BUILDIN---------------------------------------------------------------------------
   1:__abstractmethods__
   2:__annotations__
   3:__class__
   4:__delattr__
   5:__dict__
   6:__dir__
   7:__doc__
   8:__eq__
   9:__format__
  10:__ge__
  11:__getattribute__
  12:__getstate__
  13:__gt__
  14:__hash__
  15:__init__
  16:__init_subclass__
  17:__le__
  18:__lt__
  19:__module__
  20:__ne__
  21:__new__
  22:__reduce__
  23:__reduce_ex__
  24:__repr__
  25:__setattr__
  26:__sizeof__
  27:__slots__
  28:__str__
  29:__subclasshook__
  30:__weakref__
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
   1:_initrequest
   2:add_marker
   3:add_report_section
   4:addfinalizer
   5:fixturenames
   6:get_closest_marker
   7:ihook
   8:nextitem
   9:runtest
  10:setup
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
_ALLOW_MARKERS      	bool        :False
_nodeid             	str         :REFERENCE/d1__pytest/0_EXPLORE/test__explore.py::TestCls_skipping::test__2
_pytest_diamond_inheritance_warning_shown	bool        :True
name                	str         :test__2
nodeid              	str         :REFERENCE/d1__pytest/0_EXPLORE/test__explore.py::TestCls_skipping::test__2
originalname        	str         :test__2
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
_report_sections    	list        :[]
extra_keyword_matches	set         :set()
funcargs            	dict        :{}
location            	tuple       :('REFERENCE\\d1__pytest\\0_EXPLORE\\test__explore.py', 11, 'TestCls_skipping.test__2')
own_markers         	list        :[Mark(name='USER', args=(), kwargs={}), Mark(name='skip', args=(), kwargs={})]
user_properties     	list        :[]
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
_abc_impl           	_abc_data   :<_abc._abc_data object at 0x000001BD7D03A6C0>
_fixtureinfo        	FuncFixtureInfo:FuncFixtureInfo(argnames=(), initialnames=('event_loop_policy', 'skip_whole_class'), names_closure=['event_loop_policy', 'skip_whole_class', 'pytestconfig', ...
_instance           	TestCls_skipping:<test__explore.TestCls_skipping object at 0x000001BD01BBEE10>
_pyfuncitem         	Function    :<Function test__2>
_request            	TopRequest  :<FixtureRequest for <Function test__2>>
_store              	Stash       :<_pytest.stash.Stash object at 0x000001BD01BBEE90>
config              	Config      :<_pytest.config.Config object at 0x000001BD7D27B200>
fspath              	LocalPath   :C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1__pytest\0_EXPLORE\test__explore.py
instance            	TestCls_skipping:<test__explore.TestCls_skipping object at 0x000001BD01BBEE10>
keywords            	NodeKeywords:<NodeKeywords for node <Function test__2>>
module              	module      :<module 'test__explore' from 'C:\\__STARICHENKO_Element\\PROJECTS\\abc=base_aux\\REFERENCE\\d1__pytest\\0_EXPLORE\\test__explore.py'>
parent              	Class       :<Class TestCls_skipping>
path                	WindowsPath :C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1__pytest\0_EXPLORE\test__explore.py
session             	Session     :<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>
stash               	Stash       :<_pytest.stash.Stash object at 0x000001BD01BBEE90>
----------PROPERTIES__EXC---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
_check_item_and_collector_diamond_inheritance	NoneType    :None
_obj                	NoneType    :None
getmodpath          	str         :TestCls_skipping.test__2
obj                 	NoneType    :None
teardown            	NoneType    :None
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
listchain           	list        :[<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>, <Dir abc=base_aux>, <Dir REFERENCE>, <Dir d1__pytest>, <Dir 0_EXPLORE>, <Module test__ex...
                    	Session     :	<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=0>
                    	Dir         :	<Dir abc=base_aux>
                    	Dir         :	<Dir REFERENCE>
                    	Dir         :	<Dir d1__pytest>
                    	Dir         :	<Dir 0_EXPLORE>
                    	            :	...
listextrakeywords   	set         :set()
listnames           	list        :['', 'abc=base_aux', 'REFERENCE', 'd1__pytest', '0_EXPLORE', 'test__explore.py', 'TestCls_skipping', 'test__2']
reportinfo          	tuple       :(WindowsPath('C:/__STARICHENKO_Element/PROJECTS/abc=base_aux/REFERENCE/d1__pytest/0_EXPLORE/test__explore.py'), 11, 'TestCls_skipping.test__2')
----------METHODS__OBJECTS--------------------------------------------------------------------------
_getinstance        	TestCls_skipping:<test__explore.TestCls_skipping object at 0x000001BD01BBEE70>
_getobj             	method      :<bound method TestCls_skipping.test__2 of <test__explore.TestCls_skipping object at 0x000001BD01BBEE10>>
cls                 	TestCls_skipping:<test__explore.TestCls_skipping object at 0x000001BD01BBF020>
iter_markers        	generator   :<generator object Node.iter_markers.<locals>.<genexpr> at 0x000001BD018DFB90>
iter_markers_with_node	generator   :<generator object Node.iter_markers_with_node at 0x000001BD01BE4040>
iter_parents        	generator   :<generator object Node.iter_parents at 0x000001BD0183D9C0>
----------METHODS__EXC------------------------------------------------------------------------------
_repr_failure_py    	TypeError   :TypeError("Node._repr_failure_py() missing 1 required positional argument: 'excinfo'")
_traceback_filter   	TypeError   :TypeError("Function._traceback_filter() missing 1 required positional argument: 'excinfo'")
from_parent         	TypeError   :TypeError("Function.from_parent() missing 1 required positional argument: 'parent'")
function            	TypeError   :TypeError("TestCls_skipping.test__2() missing 1 required positional argument: 'self'")
getparent           	TypeError   :TypeError("Node.getparent() missing 1 required positional argument: 'cls'")
repr_failure        	TypeError   :TypeError("Function.repr_failure() missing 1 required positional argument: 'excinfo'")
warn                	TypeError   :TypeError("Node.warn() missing 1 required positional argument: 'warning'")
==========================================================================================
    """

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
    """Перед фикстурами и телом теста.

    Перед каждым тестом (после фикстур). Можно проверить условия и вызвать skip.
    """
    if item.get_closest_marker("skip_on_monday"):
        if datetime.datetime.now().weekday() == 0:
            pytest.skip("По понедельникам тест не запускается")

def pytest_runtest_call(item):
    """Непосредственно вызов тела теста."""
    """Вместо самого вызова теста. Можно обернуть в try/except.
    Не рекомендуется без крайней необходимости, лучше использовать фикстуры."""
    pass

def pytest_runtest_teardown(item, nextitem):
    """После тела теста, перед завершением фикстур."""
    """После выполнения теста (до фикстур teardown). Можно подчистить состояние."""
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
    """После всех тестов, перед закрытием терминала. Можно вывести свою статистику."""
    terminalreporter.write_line(f"\nСводка: {terminalreporter.stats.get('passed', [])}")


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
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ---------------------------------------------------------------------------
# 30.1 Инициализация и конфигурация
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def environment(request):
    return request.config.getoption("--my-env")

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
