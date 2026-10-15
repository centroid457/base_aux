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
from base_aux.base_types.m2_info import ObjectInfo


# ======================================================================================================================
print(f"[pytest.STAGE.pytest_unconfigure]START")
print(f"[pytest.STAGE.pytest_unconfigure]FINISH")


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Создание отчёта о каждой фазе (setup, call, teardown).
    Обёртка hookwrapper, поэтому обычно:
    @pytest.hookimpl(hookwrapper=True)

    ===================================================
    item
    ---------------------------------------------------
    item=<Function test__in_conftest>
----------self.HIDE_NAMES__TOUCHED=None-------------------------------------------------------------
self.NAMES_COUNT__ON_START=89
   1:_ALLOW_MARKERS
   2:__abstractmethods__
   3:__annotations__
   4:__class__
   5:__delattr__
   6:__dict__
   7:__dir__
   8:__doc__
   9:__eq__
  10:__format__
  11:__ge__
  12:__getattribute__
  13:__getstate__
  14:__gt__
  15:__hash__
  16:__init__
  17:__init_subclass__
  18:__le__
  19:__lt__
  20:__module__
  21:__ne__
  22:__new__
  23:__reduce__
  24:__reduce_ex__
  25:__repr__
  26:__setattr__
  27:__sizeof__
  28:__slots__
  29:__str__
  30:__subclasshook__
  31:__weakref__
  32:_abc_impl
  33:_check_item_and_collector_diamond_inheritance
  34:_fixtureinfo
  35:_getinstance
  36:_getobj
  37:_initrequest
  38:_instance
  39:_nodeid
  40:_obj
  41:_pyfuncitem
  42:_pytest_diamond_inheritance_warning_shown
  43:_report_sections
  44:_repr_failure_py
  45:_request
  46:_store
  47:_traceback_filter
  48:add_marker
  49:add_report_section
  50:addfinalizer
  51:cls
  52:config
  53:extra_keyword_matches
  54:fixturenames
  55:from_parent
  56:fspath
  57:funcargs
  58:function
  59:get_closest_marker
  60:getmodpath
  61:getparent
  62:ihook
  63:instance
  64:iter_markers
  65:iter_markers_with_node
  66:iter_parents
  67:keywords
  68:listchain
  69:listextrakeywords
  70:listnames
  71:location
  72:module
  73:name
  74:nextitem
  75:nodeid
  76:obj
  77:originalname
  78:own_markers
  79:parent
  80:path
  81:reportinfo
  82:repr_failure
  83:runtest
  84:session
  85:setup
  86:stash
  87:teardown
  88:user_properties
  89:warn
self.NAMES_COUNT__ON_FINISH=89
[INFO]self.SOURCE_NAMES_COUNT_WAS_CHANGED=False//89/89
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<Function test__in_conftest>
repr(SOURCE)=<Function test__in_conftest>
type(SOURCE)=<class '_pytest.python.Function'>
mro(SOURCE)=['Function', 'PyobjMixin', 'Item', 'Node', 'ABC', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.SKIP__BUILD_IN=True
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=[]
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'abort', 'commit', 'checkout', 'attach', 'detach', 'connect', 'disconnect', 'exec', 'exec_', 'pyqtConfigure', 'run', 'start', 'wait', 'pause', 'continue', 'join', 'terminate', 'quit', 'stop', 'communicate', 'pop', 'popleft', 'put', 'input', 'extend', 'extendleft', 'append', 'appendleft', 'update', 'add', 'insert', 'reverse', 'rotate', 'sort', 'load', 'reload', 'dump', 'move', 'remove', 'rename', 'remove', 'resize', 'restart', 'reload', 'unpausebreakpointhook', 'hook']
self.MAX_LINE_LEN=100
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
_instance           	NoneType    :None
_nodeid             	str         :REFERENCE/d1__pytest/0_EXPLORE/conftest.py::test__in_conftest
_pytest_diamond_inheritance_warning_shown	bool        :True
cls                 	NoneType    :None
instance            	NoneType    :None
name                	str         :test__in_conftest
nodeid              	str         :REFERENCE/d1__pytest/0_EXPLORE/conftest.py::test__in_conftest
originalname        	str         :test__in_conftest
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
_report_sections    	list        :[]
extra_keyword_matches	set         :set()
funcargs            	dict        :{'event_loop_policy': <asyncio.windows_events.WindowsProacto...
                    	event_loop_policy:<asyncio.windows_events.WindowsProactorEventLoopPolicy ...
                    	pytestconfig:<_pytest.config.Config object at 0x000001CE4E946DB0>:	ItemKe...
                    	request:<FixtureRequest for <Function test__in_conftest>>:	ItemKeyValue(K...
location            	tuple       :('REFERENCE\\d1__pytest\\0_EXPLORE\\conftest.py', 24, 'test_...
own_markers         	list        :[]
user_properties     	list        :[]
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
_abc_impl           	_abc_data   :<_abc._abc_data object at 0x000001CE4E70A980>
_fixtureinfo        	FuncFixtureInfo:FuncFixtureInfo(argnames=('pytestconfig',), initialnames=...
_pyfuncitem         	Function    :<Function test__in_conftest>
_request            	TopRequest  :<FixtureRequest for <Function test__in_conftest>>
_store              	Stash       :<_pytest.stash.Stash object at 0x000001CE533FA590>
config              	Config      :<_pytest.config.Config object at 0x000001CE4E946DB0>
fspath              	LocalPath   :C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1_...
keywords            	NodeKeywords:<NodeKeywords for node <Function test__in_conftest>>
module              	module      :<module 'conftest' from 'C:\\__STARICHENKO_Element\\PROJECTS...
parent              	Module      :<Module conftest.py>
path                	WindowsPath :C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1_...
session             	Session     :<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testscol...
stash               	Stash       :<_pytest.stash.Stash object at 0x000001CE533FA590>
----------PROPERTIES__EXC---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
_check_item_and_collector_diamond_inheritance	NoneType    :None
_getinstance        	NoneType    :None
getmodpath          	str         :test__in_conftest
teardown            	NoneType    :None
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
listchain           	list        :[<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testsco...
                    	Session     :	<Session  exitstatus=<ExitCode.OK: 0> testsfailed=0 testsco...
                    	Dir         :	<Dir abc=base_aux>
                    	Dir         :	<Dir REFERENCE>
                    	Dir         :	<Dir d1__pytest>
                    	Dir         :	<Dir 0_EXPLORE>
                    	            :	...
listextrakeywords   	set         :set()
listnames           	list        :['', 'abc=base_aux', 'REFERENCE', 'd1__pytest', '0_EXPLORE',...
reportinfo          	tuple       :(WindowsPath('C:/__STARICHENKO_Element/PROJECTS/abc=base_aux...
                    	WindowsPath :	C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\REFERENCE\d1...
                    	int         :	24
                    	str         :	test__in_conftest
----------METHODS__OBJECTS--------------------------------------------------------------------------
_getobj             	function    :<function test__in_conftest at 0x000001CE52F6B420>
iter_markers        	generator   :<generator object Node.iter_markers.<locals>.<genexpr> at 0x...
iter_markers_with_node	generator   :<generator object Node.iter_markers_with_node at 0x000001C...
iter_parents        	generator   :<generator object Node.iter_parents at 0x000001CE52F0DE40>
----------METHODS__EXC------------------------------------------------------------------------------
_obj                	TypeError   :TypeError("test__in_conftest() missing 1 required positional...
_repr_failure_py    	TypeError   :TypeError("Node._repr_failure_py() missing 1 required positi...
_traceback_filter   	TypeError   :TypeError("Function._traceback_filter() missing 1 required p...
from_parent         	TypeError   :TypeError("Function.from_parent() missing 1 required positio...
function            	TypeError   :TypeError("test__in_conftest() missing 1 required positional...
getparent           	TypeError   :TypeError("Node.getparent() missing 1 required positional ar...
obj                 	TypeError   :TypeError("test__in_conftest() missing 1 required positional...
repr_failure        	TypeError   :TypeError("Function.repr_failure() missing 1 required positi...
warn                	TypeError   :TypeError("Node.warn() missing 1 required positional argumen...
==========================================================================================




==========================================================================================
call=<CallInfo when='setup' result: None>
----------self.HIDE_NAMES__TOUCHED=None-------------------------------------------------------------
self.NAMES_COUNT__ON_START=43
   1:__annotations__
   2:__class__
   3:__class_getitem__
   4:__dataclass_fields__
   5:__dataclass_params__
   6:__delattr__
   7:__dict__
   8:__dir__
   9:__doc__
  10:__eq__
  11:__final__
  12:__format__
  13:__ge__
  14:__getattribute__
  15:__getstate__
  16:__gt__
  17:__hash__
  18:__init__
  19:__init_subclass__
  20:__le__
  21:__lt__
  22:__match_args__
  23:__module__
  24:__ne__
  25:__new__
  26:__orig_bases__
  27:__parameters__
  28:__reduce__
  29:__reduce_ex__
  30:__repr__
  31:__setattr__
  32:__sizeof__
  33:__str__
  34:__subclasshook__
  35:__weakref__
  36:_result
  37:duration
  38:excinfo
  39:from_call
  40:result
  41:start
  42:stop
  43:when
self.NAMES_COUNT__ON_FINISH=43
[INFO]self.SOURCE_NAMES_COUNT_WAS_CHANGED=False//43/43
==========================================================================================
----------OBJECTINFO.PRINT--------------------------------------------------------------------------
str(SOURCE)=<CallInfo when='setup' result: None>
repr(SOURCE)=<CallInfo when='setup' result: None>
type(SOURCE)=<class '_pytest.runner.CallInfo'>
mro(SOURCE)=['CallInfo', 'Generic', 'object']
----------SETTINGS----------------------------------------------------------------------------------
self.SKIP__BUILD_IN=True
self.NAMES__USE_ONLY_PARTS=[]
self.NAMES__SKIP_FULL=[]
self.NAMES__SKIP_PARTS=['init', 'new', 'create', 'enter', 'install', 'set', 'clone', 'copy', 'move', 'next', 'clear', 'reduce', 'close', 'del', 'exit', 'kill', 'abort', 'commit', 'checkout', 'attach', 'detach', 'connect', 'disconnect', 'exec', 'exec_', 'pyqtConfigure', 'run', 'start', 'wait', 'pause', 'continue', 'join', 'terminate', 'quit', 'stop', 'communicate', 'pop', 'popleft', 'put', 'input', 'extend', 'extendleft', 'append', 'appendleft', 'update', 'add', 'insert', 'reverse', 'rotate', 'sort', 'load', 'reload', 'dump', 'move', 'remove', 'rename', 'remove', 'resize', 'restart', 'reload', 'unpausebreakpointhook', 'hook']
self.MAX_LINE_LEN=100
self.MAX_ITER_ITEMS=5
----------SKIPPED_BUILDIN---------------------------------------------------------------------------
   1:__annotations__
   2:__class__
   3:__class_getitem__
   4:__dataclass_fields__
   5:__dataclass_params__
   6:__delattr__
   7:__dict__
   8:__dir__
   9:__doc__
  10:__eq__
  11:__final__
  12:__format__
  13:__ge__
  14:__getattribute__
  15:__getstate__
  16:__gt__
  17:__hash__
  18:__init__
  19:__init_subclass__
  20:__le__
  21:__lt__
  22:__match_args__
  23:__module__
  24:__ne__
  25:__new__
  26:__orig_bases__
  27:__parameters__
  28:__reduce__
  29:__reduce_ex__
  30:__repr__
  31:__setattr__
  32:__sizeof__
  33:__str__
  34:__subclasshook__
  35:__weakref__
----------SKIPPED_FULLNAMES-------------------------------------------------------------------------
----------SKIPPED_PARTNAMES-------------------------------------------------------------------------
   1:start
   2:stop
----------PROPERTIES__ELEMENTARY_SINGLE-------------------------------------------------------------
_result             	NoneType    :None
duration            	float       :0.00031749997287988663
excinfo             	NoneType    :None
result              	NoneType    :None
when                	str         :setup
----------PROPERTIES__ELEMENTARY_COLLECTION---------------------------------------------------------
----------PROPERTIES__OBJECTS-----------------------------------------------------------------------
----------PROPERTIES__EXC---------------------------------------------------------------------------
----------METHODS__ELEMENTARY_SINGLE----------------------------------------------------------------
----------METHODS__ELEMENTARY_COLLECTION------------------------------------------------------------
----------METHODS__OBJECTS--------------------------------------------------------------------------
----------METHODS__EXC------------------------------------------------------------------------------
from_call           	TypeError   :TypeError("CallInfo.from_call() missing 2 required positiona...
==========================================================================================


# [test.py]
def test__in_conftest__1_ok(pytestconfig):
    pass

def test__in_conftest__2_fail(pytestconfig):
    raise Exception("raised")

def test__in_conftest__3_skip(pytestconfig):
    pytest.skip("skip")

def test__in_conftest__4_exit(pytestconfig):
    pytest.exit(f"exit")
    """
    print(f"[pytest.STAGE.pytest_runtest_makereport]START")

    # -----------------------------------------------------------
    # 1=попытка поймать PYTEST.EXIT!!! - не ловит!!! потому что это не Exception для теста а сигнал выхода для сессии!!!
    from _pytest.outcomes import Exit

    # print(f"{item=}")
    # ObjectInfo(item).print()
    # print(f"{call=}")
    # ObjectInfo(call).print()

    # ПОМЕТКА выхода из тестирования pytest.exit как FAILED! если так не сделать то будет похоже на SKIPPED
    outcome = yield
    report = outcome.get_result()
    if call.excinfo and isinstance(call.excinfo.value, Exit):
        # pytest.exit() внутри теста — принудительно делаем failed
        report.outcome = "failed"
        report.longrepr = f"Фатальная остановка: {call.excinfo.value}"

    print(f"[pytest.STAGE.pytest_runtest_makereport]FINISH")


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
