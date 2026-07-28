# =============================================================================
# 41. PYTEST-HTML: ГЕНЕРАЦИЯ HTML-ОТЧЁТОВ
# =============================================================================
# Плагин pytest-html создаёт красивые отчёты в формате HTML.
# Установка: pip install pytest-html

import pytest

# ---------------------------------------------------------------------------
# 41.1 Базовое использование
# ---------------------------------------------------------------------------
# Генерация отчёта одной командой:
# pytest --html=report.html

# Чтобы не подключать внешние CSS/JS и сделать отчёт переносимым:
# pytest --html=report.html --self-contained-html

# ---------------------------------------------------------------------------
# 41.2 Настройка заголовка и окружения
# ---------------------------------------------------------------------------
# Изменить заголовок отчёта можно через хук pytest_html_report_title
# в файле conftest.py (или в текущем файле при запуске с -p no:cacheprovider)
def pytest_html_report_title(report):
    report.title = "Отчёт тестов устройств v2.0"

# Добавить информацию об окружении (версия ОС, ветка git, переменные):
def pytest_configure(config):
    # Создаём словарь метаданных, если его ещё нет
    if not hasattr(config, '_metadata'):
        config._metadata = {}
    config._metadata["Версия ОС"] = "Ubuntu 22.04"
    config._metadata["Версия Python"] = "3.11.5"

# ---------------------------------------------------------------------------
# 41.3 Добавление дополнительной информации в таблицу результатов
# ---------------------------------------------------------------------------
# Можно добавить колонки в таблицу тестов через хуки:
#   pytest_html_results_table_header – для заголовков колонок
#   pytest_html_results_table_row – для данных в строках

def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Устройство</th>")  # добавляем третью колонку

def pytest_html_results_table_row(report, cells):
    device = getattr(report, 'device_name', '—')
    cells.insert(2, f"<td>{device}</td>")

# Чтобы записать имя устройства в объект report, используем record_property в тесте:
def test_device1(record_property):
    record_property("device_name", "BT-001")
    assert True

# Или напрямую в хуке pytest_runtest_makereport:
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     report.device_name = getattr(item, "device_name", "—")

# ---------------------------------------------------------------------------
# 41.4 Вставка скриншотов, файлов, произвольного HTML
# ---------------------------------------------------------------------------
# Для добавления картинок, ссылок или произвольного HTML в ячейку отчёта
# используется список "extra" у объекта report.

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        # Добавляем скриншот, если тест упал
        if report.failed:
            # Путь к файлу (например, скриншот ошибки)
            screenshot_path = "failure.png"
            # HTML-строка для вставки в отчёт
            extra_html = f'<img src="{screenshot_path}" width="200" />'
            report.extra = getattr(report, 'extra', []) + [
                pytest_html.extras.html(extra_html)
            ]
        # Можно добавить ссылку на внешний лог
        report.extra = getattr(report, 'extra', []) + [
            pytest_html.extras.url("http://example.com/logs/test.log")
        ]
        # Или простой текст
        report.extra = getattr(report, 'extra', []) + [
            pytest_html.extras.text("Дополнительная информация")
        ]

# ---------------------------------------------------------------------------
# 41.5 Динамическое имя файла отчёта (см. раздел 21)
# ---------------------------------------------------------------------------
# В разделе 21 мы уже рассматривали, как задать имя отчёта с меткой времени
# или другими данными. Кратко: в pytest_configure можно установить
# config.option.htmlpath или переименовать файл в pytest_sessionfinish.

# ---------------------------------------------------------------------------
# 41.6 Совместимость с pytest-xdist
# ---------------------------------------------------------------------------
# При параллельном запуске (pytest -n auto --html=report.html) каждый воркер
# генерирует свою часть отчёта, затем в конце сессии они объединяются.
# Чтобы избежать конфликтов, не изменяйте один и тот же файл из нескольких
# процессов через внешние скрипты — используйте встроенный механизм объединения.

# ---------------------------------------------------------------------------
# 41.7 Важные замечания
# ---------------------------------------------------------------------------
# - Отчёт формируется в конце сессии, поэтому при аварийном завершении (kill -9)
#   он может остаться пустым. Решение — дублирование логов и аварийная генерация
#   (раздел 32).
# - Не записывайте слишком много громоздких данных в extra — отчёт может стать
#   очень большим. Для больших файлов давайте ссылки, а не встраивайте содержимое.
# - Если нужен отчёт без потери данных при множественных запусках, используйте
#   уникальные имена (timestamp).
# - Плагин поддерживает кастомные CSS через --css=style.css.



# ======================================================================================================================
# =============================================================================
# 21. ДИНАМИЧЕСКОЕ ИМЯ ДЛЯ ОТЧЁТА HTML (pytest-html)
# =============================================================================
# pytest-html записывает отчёт по пути, указанному в --html.
# Чтобы имя файла зависело от результатов тестов или от данных, полученных
# во время прогона, нужно переименовать готовый отчёт после завершения сессии.
# Ниже показаны способы: от простого (времени прогона) до сложного
# (использование значения, сохранённого тестом).

import os
import datetime
import pytest

# ---------------------------------------------------------------------------
# 21.1 Простейший вариант: временная метка в имени
# ---------------------------------------------------------------------------
# Создаём в conftest.py хук, который вычисляет имя до прогона
# или переименовывает после. Но проще всего генерировать имя на лету
# в командной строке через подстановку shell, например:
#
# pytest --html=report_$(date +%Y%m%d_%H%M%S).html
# (Linux/Mac)
#
# В Windows PowerShell:
# $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"; pytest --html="report_$timestamp.html"

# Если хочется автоматизации изнутри Python, используем pytest_configure.

# =============================================================================
# 21.2 Динамическое имя через pytest_configure (глобально для всех прогонов)
# =============================================================================
def pytest_configure(config):
    # Проверяем, что плагин pytest-html активирован
    if not hasattr(config.option, 'htmlpath'):
        return
    # Если пользователь не указал --html явно, можно задать его
    if not config.option.htmlpath:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Например, сохраним в папку reports/
        os.makedirs("reports", exist_ok=True)
        config.option.htmlpath = f"reports/report_{timestamp}.html"

# Теперь можно запускать pytest без --html – отчёт появится автоматически.

# ---------------------------------------------------------------------------
# 21.3 Переименование после прогона на основе тестовых данных
# ---------------------------------------------------------------------------
# Задача: получить значение из тестов (например, версию сборки, имя окружения)
# и вставить его в имя финального отчёта.
# Для этого в тесте сохраняем значение в глобальную переменную или в
# request.config.cache, а в хуке pytest_sessionfinish переименовываем файл.

# conftest.py (фрагмент):
# import os, pytest
# VERSION_FOR_REPORT = None
#
# @pytest.fixture(scope="session", autouse=True)
# def capture_version(request):
#     # Имитация: получаем версию из переменной окружения или вычисляем
#     version = os.environ.get("APP_VERSION", "unknown")
#     request.config._report_version = version  # кладём в конфиг на время сессии
#     yield
#
# def pytest_sessionfinish(session, exitstatus):
#     version = getattr(session.config, '_report_version', 'UNKNOWN')
#     htmlpath = session.config.option.htmlpath
#     if htmlpath:
#         dir_name = os.path.dirname(htmlpath)
#         base, ext = os.path.splitext(os.path.basename(htmlpath))
#         new_name = f"{base}_v{version}{ext}"
#         new_path = os.path.join(dir_name, new_name) if dir_name else new_name
#         try:
#             os.rename(htmlpath, new_path)
#         except OSError as e:
#             # Если файл не сгенерировался – не страшно
#             pass

# ---------------------------------------------------------------------------
# 21.4 Более гибкое решение: сохранение данных в файл и пост-обработка
# ---------------------------------------------------------------------------
# Можно из любого теста записывать нужные значения в специальный файл,
# а в sessionfinish читать этот файл и генерировать имя.
# Пример (добавить в conftest.py):

@pytest.fixture(scope="session", autouse=True)
def collect_report_metadata(request):
    # Создаём временный файл для метаданных
    meta_file = request.config.cache.get("report_meta", None)
    if not meta_file:
        import tempfile
        fd, meta_file = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        request.config.cache.set("report_meta", meta_file)
    # Сохраняем путь в конфиг
    request.config._meta_file = meta_file
    yield
    # Удалять не будем – sessionfinish понадобится

def pytest_sessionfinish(session, exitstatus):
    meta_file = getattr(session.config, '_meta_file', None)
    htmlpath = session.config.option.htmlpath
    if meta_file and os.path.exists(meta_file) and htmlpath:
        with open(meta_file, "r") as f:
            meta_value = f.read().strip()
        if meta_value:
            dir_name = os.path.dirname(htmlpath)
            base, ext = os.path.splitext(os.path.basename(htmlpath))
            new_name = f"{base}_{meta_value}{ext}"
            new_path = os.path.join(dir_name, new_name) if dir_name else new_name
            os.rename(htmlpath, new_path)
        os.remove(meta_file)

# Теперь в любом тесте можно записать нужную строку в файл, зная его путь:
def test_collect_build_number(request):
    meta_file = request.config._meta_file
    with open(meta_file, "w") as f:
        f.write("build123")

# ---------------------------------------------------------------------------
# 21.5 Альтернатива: кастомный отчёт прямо в тесте (без pytest-html)
# ---------------------------------------------------------------------------
# Если нужен полный контроль, можно вообще не использовать --html,
# а после всех тестов выполнить свой скрипт, который прочитает
# стандартный JUnit XML и сгенерирует HTML с нужным именем.
# Но это уже другой уровень сложности.

# =============================================================================
# ВАЖНЫЕ ЗАМЕЧАНИЯ
# =============================================================================
# - Плагин pytest-html требует явного указания --html. Без него sessionfinish
#   не имеет htmlpath, переименовывать нечего.
# - Переименование в sessionfinish отработает после завершения всех тестов,
#   даже если некоторые упали.
# - Если вы используете CI/CD, переименованный файл нужно будет найти и архивировать
#   по новому имени. Учтите это в сборочных скриптах.
# - Запись метаданных через фикстуру с scope='session' гарантирует, что файл
#   будет создан один раз и доступен всем тестам.





