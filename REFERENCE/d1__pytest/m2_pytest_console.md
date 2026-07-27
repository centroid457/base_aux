# ======================================================================================================================
# !. BEST 
# =============================================================================
# ОПТИМАЛЬНЫЙ ВЫВОД с ГЕНЕРАЦИЕЙ ОТЧЕТА
pytest -v --html=report_results.html








# ======================================================================================================================
# 1=ФИЛЬТРАЦИЯ ЗАПУСКА
# ======================================================================================================================
# 1.0 СБОР СПИСКА ТЕСТОВ БЕЗ ИСПОЛНЕНИЯ
# =============================================================================
# Только собрать тесты и показать их список, не выполняя
pytest --collect-only

# Показать дерево тестов (требуется плагин: pip install pytest-clarity)
pytest --collect-only --tree

# Собрать только список тестов, подходящих под ключевое слово, в файл
pytest -k "database" --collect-only -q > db_tests.txt

# =============================================================================
# 1.1 ФИЛЬТАЦИЯ по ФАЙЛАМ/ПАПКАМ
# =============================================================================
# Запустить все тесты в текущей директории и поддиректориях
pytest

# Запустить конкретный файл с тестами
pytest test_example.py

# Все тесты внутри папки tests/
pytest tests/
# Все тесты внутри нескольких папок
pytest tests/unit tests/integration

# Запустить тесты из нескольких файлов/папок
pytest test_a.py test_b.py tests/

# Игнорировать пути файлы
pytest --ignore=tests/legacy --ignore=tests/experimental

# ШАБЛОН МАСКА имён файлов (по умолчанию test_*.py)
pytest -k "test_*.py"

# =============================================================================
# 1.2 ФИЛЬТРАЦИЯ по МЕТОДАМ/КЛАССАМ
# =============================================================================
# Запустить конкретную тестовую функцию в файле
pytest test_example.py::test_passing

# Запустить конкретный метод класса
pytest test_classes.py::TestUserAuthentication::test_initial_state

# Запустить все тесты класса
pytest test_classes.py::TestUserAuthentication

# Запустить тесты по совпадению с ключевым словом в имени (подстрока)
pytest -k "authentication"

# Исключить тесты по ключевому слову
pytest -k "not slow"

# Комбинировать: запустить тесты, содержащие "login" или "logout"
pytest -k "login or logout"

# =============================================================================
# 1.3 ФИЛЬТРАЦИЯ по МАРКЕРАМ
# =============================================================================
# Запустить тесты, помеченные маркером @pytest.mark.slow
pytest -m slow

# Прогнать медленные тесты отдельно
pytest -m slow --durations=10

# marker_combination-1=NO = все что без указанного маркера 
pytest -m "not slow"
# marker_combination-2=AND
pytest -m "mvp and info and long"
# marker_combination-3=OR
pytest -m "mvp or info or long"

# Запустить тесты с маркером integration И с маркером database
pytest -m "integration and database"

# Показать все доступные маркеры (определённые в pytest.ini или в коде)
pytest --markers

# =============================================================================
# 1.4 ПЕРЕЗАПУСК УПАВШИХ ТЕСТОВ
# =============================================================================
# Запустить только те тесты, которые упали в последнем прогоне
pytest --lf

# Запустить сначала упавшие тесты, потом остальные
pytest --ff


# =============================================================================
# 1.5 ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ И ДИНАМИЧЕСКОЕ ПРОПУСКАНИЕ
# =============================================================================

# Установить переменную окружения прямо в команде (Linux/Mac)
ENV=production pytest

# В Windows cmd:
# set ENV=production && pytest

# В PowerShell:
# $env:ENV="production"; pytest

# Использовать значение переменной в тестах (os.environ.get('ENV'))











# ======================================================================================================================
# 2=ВЫВОД ДАННЫХ/RESULTS/REPORTS
# ======================================================================================================================
# 2.1 ВЫВОД ДАННЫХ - КОНСОЛЬ
# =============================================================================
# Подробный вывод (показывает имена тестов)
pytest -v

```
C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\prj_1_harvest_tests>pytest -v
=============================================== test session starts ================================================
platform win32 -- Python 3.12.7, pytest-9.0.2, pluggy-1.5.0 -- C:\Python3127x64\python.exe
cachedir: .pytest_cache
rootdir: C:\__STARICHENKO_Element\PROJECTS\abc=base_aux
configfile: .pytest.ini
plugins: anyio-4.6.2.post1, dash-4.4.0, asyncio-1.3.0, cov-6.2.1, dependency-0.6.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 27 items

test__harvest.py::Test_01__Detection::test_1__exist_ports PASSED                                              [  3%]
test__harvest.py::Test_01__Detection::test_2__exist_can_open PASSED                                           [  7%]
test__harvest.py::Test_01__Detection::test_3__harvest_detection PASSED                                        [ 11%]
test__harvest.py::Test_02__PreInstall::test_pre_0__internet PASSED                                            [ 14%]
test__harvest.py::Test_02__PreInstall::test_pre_1__coreutils_timeout PASSED                                   [ 18%]
test__harvest.py::Test_02__PreInstall::test_pre_2__picocom PASSED                                             [ 22%]
test__harvest.py::Test_02__PreInstall::test_pre_3__python PASSED                                              [ 25%]
test__harvest.py::Test_02__PreInstall::test_pre_4__python_serial PASSED                                       [ 29%]
test__harvest.py::Test_02__PreInstall::test_pre_5__wifi_1__iw PASSED                                          [ 33%]
test__harvest.py::Test_02__PreInstall::test_pre_5__wifi_2__bluez PASSED                                       [ 37%]
test__harvest.py::Test_02__PreInstall::test_pre_5__wifi_3__usbutils PASSED                                    [ 40%]
test__harvest.py::Test_1__GNSS::test_gnss_1__gnss_exists PASSED                                               [ 44%]
test__harvest.py::Test_1__GNSS::test_gnss_2__nmea_output_exists PASSED                                        [ 48%]
test__harvest.py::Test_1__GNSS::test_gnss_3__nmea_output_correct SKIPPED (Not realised yet)                   [ 51%]
test__harvest.py::Test_21__WiFi::test_wf_1__interface_exists PASSED                                           [ 55%]
test__harvest.py::Test_21__WiFi::test_wf_2__link_connected FAILED                                             [ 59%]
test__harvest.py::Test_21__WiFi::test_wf_3__signal_quality FAILED                                             [ 62%]
test__harvest.py::Test_22__Bluetooth::test_bt_1__interface_exists PASSED                                      [ 66%]
test__harvest.py::Test_22__Bluetooth::test_bt_2__scan_devices PASSED                                          [ 70%]
test__harvest.py::Test_22__Bluetooth::test_bt_3__scan_devices_count PASSED                                    [ 74%]
test__harvest.py::Test_3__GSM::test_gsm_1__interface_exists PASSED                                            [ 77%]
test__harvest.py::Test_3__GSM::test_gsm_2__sim_detected FAILED                                                [ 81%]
test__harvest.py::Test_3__GSM::test_gsm_3__network_registration FAILED                                        [ 85%]
test__harvest.py::Test_3__GSM::test_gsm_4__signal_quality FAILED                                              [ 88%]
test__harvest.py::Test_4__RFID::test_rfid_1__script_exists PASSED                                             [ 92%]
test__harvest.py::Test_4__RFID::test_rfid_2__execution_no_error PASSED                                        [ 96%]
test__harvest.py::Test_4__RFID::test_rfid_3__valid_response_present PASSED                                    [100%]

===================================================== FAILURES =====================================================
_____________________________________ Test_21__WiFi.test_wf_2__link_connected ______________________________________

self = <prj_1_harvest_tests.test__harvest.Test_21__WiFi object at 0x0000023C176A8D40>
harvest = <prj_1_harvest_tests.utils.HarvestDevice object at 0x0000023C176A9190>, present__wifi = True

    def test_wf_2__link_connected(self, harvest, present__wifi):
        """Получение данных о текущем подключении."""
        if not present__wifi:
            pytest.skip("Wi-Fi отсутствует")

        # assert harvest.cmd__check_success("iw dev wlan0 link"), "Команда iw dev wlan0 link вернула ошибку"
        stdout_connected = harvest.conn.write_read_lines("iw dev wlan0 link")
>       assert "Not connected." not in stdout_connected, "нет соединения по WiFi"
E       AssertionError: нет соединения по WiFi
E       assert 'Not connected.' not in ['iw dev wlan0 link', 'Not connected.', 'root@harvest05:~# ', 'root@harvest05:~# ']

test__harvest.py:225: AssertionError
----------------------------------------------- Captured stdout call -----------------------------------------------
SerialClient2(COM16.115200,occupied=harvest05){'write': b'iw dev wlan0 link\r\n'}
SerialClient2(COM16.115200,occupied=harvest05bytes=b'iw dev wlan0 link\r\n\x1b[?2004l\rNot connected.\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# printable=iw dev wlan0 link
Not connected.
root@harvest05:~#
root@harvest05:~#
______________________________________ Test_3__GSM.test_gsm_4__signal_quality ______________________________________

self = <prj_1_harvest_tests.test__harvest.Test_3__GSM object at 0x0000023C1766F5F0>
harvest = <prj_1_harvest_tests.utils.HarvestDevice object at 0x0000023C176A9190>, present__gsm = True

    def test_gsm_4__signal_quality(self, harvest, present__gsm):
        """Валидация уровня сигнала (RSSI > 5)."""
        if not present__gsm:
            pytest.skip("GSM отсутствует")

        harvest.conn.write_bytes('echo -e "AT+CSQ\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1')
        output = harvest.conn.read_lines(timeout_continue=1.5)
        for line in output:
            if "+CSQ:" in line:
                try:
                    # формат +CSQ: <rssi>,<ber>
                    parts = line.replace("+CSQ:", "").strip().split(",")
                    rssi = int(parts[0])
                    assert rssi >= 5, f"Низкий уровень сигнала GSM: {rssi} (из 31)"
                    return
                except Exception:
                    pass
>       pytest.fail("Не удалось извлечь уровень сигнала GSM")
E       Failed: Не удалось извлечь уровень сигнала GSM

test__harvest.py:385: Failed
----------------------------------------------- Captured stdout call -----------------------------------------------
SerialClient2(COM16.115200,occupied=harvest05){'write': b'echo -e "AT+CSQ\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1\r\n'}
SerialClient2(COM16.115200,occupied=harvest05bytes=b'echo -e "AT+CSQ\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1\r\n\x1b[?2004l\r[1] 1187\r\nAT+CSQ\r\r\n\r\n[1]+  Done                    echo -e "AT+CSQ\\r\\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2\r\n-bash: kill: %1: no such job\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# printable=echo -e "AT+CSQ\r\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2 & sleep 0.5; kill %1
[1] 1187
AT+CSQ

[1]+  Done                    echo -e "AT+CSQ\r\n" > /dev/ttyUSB2 && cat /dev/ttyUSB2
-bash: kill: %1: no such job
root@harvest05:~#
root@harvest05:~#
============================================= short test summary info ==============================================
FAILED test__harvest.py::Test_21__WiFi::test_wf_2__link_connected - AssertionError: нет соединения по WiFi
FAILED test__harvest.py::Test_21__WiFi::test_wf_3__signal_quality - Failed: Не найдена строка signal
FAILED test__harvest.py::Test_3__GSM::test_gsm_2__sim_detected - AssertionError: SIM-карта не готова или модем не отвечает
FAILED test__harvest.py::Test_3__GSM::test_gsm_3__network_registration - AssertionError: Модем не зарегистрирован в сотовой сети
FAILED test__harvest.py::Test_3__GSM::test_gsm_4__signal_quality - Failed: Не удалось извлечь уровень сигнала GSM
===================================== 5 failed, 21 passed, 1 skipped in 50.49s =====================================

C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\prj_1_harvest_tests>
```

# Сокращённый вывод (минимальная информация) - ТИХАЯ ПРОВЕРКА
pytest -q

# Очень подробный вывод (включает docstring тестов)
pytest -vv

# Показать локальные переменные в трейсбэке при падении
pytest -l

# Показать print() даже для успешных тестов (обычно скрывается)
pytest -s

# =============================================================================
# 2.2 УПРАВЛЕНИЕ ВЫВОДОМ ПРЕДУПРЕЖДЕНИЙ
# =============================================================================     # FIXME: ЭТО ПЕРЕХВАТ вывода???????????????????
# Показать все предупреждения
pytest -W all

# Скрыть все предупреждения
pytest -W ignore

# Трактовать предупреждения как ошибки
pytest -W error

# =============================================================================
# 2.3 ГЕНЕРАЦИЯ ОТЧЁТОВ
# =============================================================================
# Вывод результатов в формате JUnit XML (для CI/CD, Jenkins)
pytest --junitxml=test_results.xml

# Сохранить список всех пройденных тестов в текстовый файл
pytest --collect-only -q > all_tests.txt

# Генерация HTML-отчёта (требуется плагин: pip install pytest-html)
pytest --html=report.html

# =============================================================================
# 2.4 ТРЕЙСБЭК
# =============================================================================
# Показать трейсбэк полностью (не обрезая) при падении
pytest --tb=long

# Показать только самую короткую информацию об ошибке
pytest --tb=line

# Не показывать трейсбэк вообще (только точки и результат)
pytest --tb=no

# =============================================================================
# 2.5 ВРЕМЯ ВЫПОЛНЕНИЯ
# =============================================================================
# Замер времени выполнения медленных тестов (встроено)
pytest --durations=10       # показать 10 самых медленных тестов
pytest --durations=0        # показать все тесты с временем выполнения

# =============================================================================
# 2.6 ПРОВЕРКА ПОКРЫТИЯ ЮНИТТЕСТОВ
# =============================================================================
# Покрытие кода (требуется плагин: pip install pytest-cov) --- это только для юнит-тестов!!! не для тестирования устройств!!
pytest --cov=my_package --cov-report=term --cov-report=html












# ======================================================================================================================
# 3=CONF
# ======================================================================================================================
# 3.1 КОНФИГУРАЦИЯ PYTEST (pytest.ini / pyproject.toml)
# =============================================================================

# Создать файл pytest.ini в корне проекта с примерным содержимым:
# [pytest]
# markers =
#     slow: медленные тесты
#     integration: интеграционные тесты
# testpaths = tests
# python_files = test_*.py
# addopts = -v --tb=short
# Тогда запуск просто: pytest

# Указать другой конфигурационный файл
pytest -c my_custom.ini

# Показать текущую конфигурацию (помогает понять, откуда берутся настройки)
pytest --collect-only -q   # показывает только список тестов с настройками

# =============================================================================
# 3.2 плагины
# =============================================================================
# Показать плагины, которые загружены
pytest --trace-config

# =============================================================================
# 3.3 кеш/плагины
# =============================================================================
# Чтобы ускорить запуск, можно отключить плагины:
pytest -p no:cacheprovider

# Запустить с новой базой кэша (игнорировать старые .pytest_cache)
pytest --cache-clear

# =============================================================================
# 3.4 ПАРАЛЛЕЛЬНЫЙ ЗАПУСК (pytest-xdist)
# =============================================================================
# Установить: pip install pytest-xdist
# Запустить на нескольких ядрах (авто-определение количества CPU)       # НЕ ПОНЯТНО ЧТО ИМЕННО ЗАПУСКАЕТ?????? ПРЕИМУЩЕСТВО????
pytest -n auto

# Запустить в 4 параллельных процесса
pytest -n 4

# Параллельно и с распределением по файлам тестов
pytest -n 4 --dist=loadfile













# ======================================================================================================================
# 4=DEBUG
# ======================================================================================================================
# 4.1 ОТЛАДЧИК
# =============================================================================

# Открыть отладчик pdb при падении теста
pytest --pdb

# Остановиться в начале сессии (для отладки кода тестов)
pytest --trace

# =============================================================================
# 4.2 ОСТАНОВКА ПОСЛЕ ПАДЕНИЙ
# =============================================================================
# Прервать выполнение при первом же упавшем тесте
pytest -x

# Прервать после двух падений - два любых теста упали! не перезапускает!
pytest --maxfail=2









# ======================================================================================================================
# разное
# ======================================================================================================================
# 17. ДЛЯ WINDOWS (CMD/POWERSHELL) — особенности
# =============================================================================
# В cmd многие символы работают так же, но лучше избегать сложных выражений в -k.
# Для передачи выражений с пробелами используйте кавычки:
pytest -k "login or logout"   # работает

# В PowerShell аналогично, но если нужно передать переменную окружения:
# $env:MY_VAR="value"; pytest





# ======================================================================================================================
