"""
Вспомогательные функции не подходящие под принцип Универсальные!
тоесть все что не должно быть в func_universal но почемуто там оказалось!!!!
"""
# =====================================================================================================================
# STARICHENKO UNIVERSAL IMPORT
import sys
sys.path.append("..")  # Adds higher directory to python modules path.
import CONSTANTS

import time
import pathlib
import typing as tp

import utilities.func_universal as UFU
from gui.pyqt_import_all_by_star import *

# from users.user_profile import UserProfile_Singleton
# from stands.stand import Stand_Singleton
# from results.results_testplan import ResultsTestplan_Singleton
# =====================================================================================================================

import os
import re
from shutil import copyfile
from utilities.processor_file_excel import _ExcelProcessor
from utilities.processor_file_json import ProcessorJsonDict
import win32com.client


# import connection import volga_connection
# pid_short__get = volga_connection.pid_short__get


# =====================================================================================================================
# 1=FILE -------------------------------------------------------------------------------------------------------------
def get_settings_file_for_pid(pid, _dirpath=None):  # STARICHENKO
    pid_short = pid_short__get(pid)
    if _dirpath is None:
        _dirpath = CONSTANTS.DIRPATH_TESTPLANS_SETTINGS
    else:
        _dirpath = pathlib.Path(_dirpath)

    for filepath in _dirpath.glob("*_settings.json"):
        jd = ProcessorJsonDict().json_read(filepath)
        jdPid = jd.get(pid_short)
        if jdPid:
            return filepath

    UFU.logging_and_print_warning(f"НЕ найден нужный файл для [{pid_short=}/{pid=}/{_dirpath=}]")


# 2=JSON_DATA --------------------------------------------------------------------------------------------------------
def get_settings_jd(pid, user_path=None):  # STARICHENKO
    pid = pid_short__get(pid)

    file_settings_abs = get_settings_file_for_pid(pid, user_path)

    if file_settings_abs is None or not os.path.exists(file_settings_abs):
        UFU.logging_and_print_warning(f"файл отсутствует или недоступен [{file_settings_abs}]")
        return

    jd = ProcessorJsonDict().json_read(file_settings_abs)
    UFU.logging_and_print_debug(f"jd={jd}")
    return jd


def get_settings_jdDef(pid, user_path=None, jd=None):  # STARICHENKO
    if jd is None:
        jd = get_settings_jd(pid, user_path)
    if jd:
        return jd.get("default_settings")


def get_settings_jdDef_DevList(pid, user_path=None, jd=None):  # STARICHENKO
    jdDef = get_settings_jdDef(pid, user_path, jd)
    if jdDef:
        return list(jdDef)
    else:
        return []


def get_settings_jdDefDev_MeasList(pid, devDef, user_path=None, jd=None):  # STARICHENKO
    # todo: split to separate funcs!
    jdDef = get_settings_jdDef(pid, user_path, jd)
    if jdDef:
        jdDefDev = jdDef.get(devDef)
        if jdDefDev:
            jdDefDevMeas = jdDef.get("measurement_settings")
            if jdDefDevMeas:
                return list(jdDefDevMeas)
    else:
        return []


def get_settings_jdPid(pid, user_path=None, jd=None):  # STARICHENKO
    if jd is None:
        jd = get_settings_jd(pid, user_path)
    if jd:
        return jd.get(pid_short__get(pid))


def get_settings_jdPid_DefList(pid, user_path=None, jd=None):  # STARICHENKO
    jdPid = get_settings_jdPid(pid, user_path, jd)
    if jdPid:
        jdPid_DefList = jd.get("default_settings")
        if jdPid_DefList:
            return jdPid_DefList
        else:
            return []


# 3=EXACT SETTINGS ---------------------------------------------------------------------------------------------------
def get_settings_all_from_jdDef(pid, jd=None, devDefList_use=[], measDefList_use=[]):  # STARICHENKO
    result = dict()

    if jd is None:
        jd = get_settings_jd(pid)

    if jd is None:
        UFU.logging_and_print_warning(f"не нашлось файла настроек для PID=[{pid}]")
        return

    jdDef = get_settings_jdDef(pid, jd=jd)
    UFU.logging_and_print_debug(f"jdDef=[{jdDef}]")
    if jdDef is None or len(jdDef) == 0:
        UFU.logging_and_print_warning(f"не нашлось значений в корневой секции default_settings=[{jdDef}]")
        return

    # 0=доступные настройки
    jdDef_DevList = get_settings_jdDef_DevList(pid, jd=jd)
    UFU.logging_and_print_debug(f"jdDef_DevList=[{jdDef_DevList}]")

    # 1=берем настройки одного устройства
    for devDef in jdDef_DevList:
        if (devDefList_use != []) and (devDef not in devDefList_use):
            UFU.logging_and_print_warning(f"не будет учитывыаться настройки для всего устройствв=[{devDef}]")
            continue
        else:
            jdDefDev = jdDef.get(devDef)
            jdDefDevMeas = jdDefDev.get("measurement_settings")
            measDefList = list(jdDefDevMeas)
            UFU.logging_and_print_debug(f"measDefList=[{measDefList}]")

            # 2=берем настройки одного класса
            for meas_class in measDefList:
                meas_class_settings = jdDefDevMeas.get(meas_class).get('settings')
                if meas_class_settings is None:
                    continue
                if (measDefList_use == []) or (meas_class in measDefList_use):
                    UFU.logging_and_print_debug(f"добавляем настройки=[{devDef, meas_class}]={result}")
                    result.update(meas_class_settings)
                else:
                    UFU.logging_and_print_warning(f"НЕ добавляем настройки=[{devDef, meas_class}]")

    UFU.logging_and_print_debug(f"настройки из функции=[{result}]")
    return result


def get_stand_testcases_list_and_settings_from_json_by_pid(
        settings_dict,
        pid,
        dict_params_enum=None):
    """
    Task:
    1. Read "*_settings.json" files from DIRPATH_TESTPLANS_SETTINGS by short_pid
    2. update settings_dict with stand_testcases_list, measurement_settings, protocol_creators and testcases_for_protocol
    """
    result = dict()
    pattern = re.compile("'''([^']+?)'''")

    # variable_parameters = testplan_settings_file_data.get('variable_parameters')
    testplan__default_name_list = []

    # 2=USE-1=exact DEFAULT SETTINGS
    if "default_settings" in UFU.testplan_settings__by_short_pid:
        testplan__default_name_list = UFU.testplan_settings__by_short_pid.pop("default_settings")   # ["CU_TESTPLAN", ]

        if isinstance(testplan__default_name_list, str):
            testplan__default_name_list = [testplan__default_name_list, ]
        if isinstance(testplan__default_name_list, list):
            for testplan__default_name in testplan__default_name_list:
                result = UFU.dicts_merge([result, UFU.testplans_settings__all_default_dict.get(testplan__default_name, {})])
        else:
            msg = f"incorrect type {testplan__default_name_list=}"
            UFU.logging_and_print_warning(msg)

    # 2=USE-2=exact testplan
    result = UFU.dicts_merge([result, UFU.testplan_settings__by_short_pid])

    if UFU.testplan_settings__by_short_pid.get('measurement_settings'):
        stand_testcases_list = list(UFU.testplan_settings__by_short_pid.get('measurement_settings').keys())
    else:
        UFU.logging_and_print_warning(f'ERROR! no testplan for {pid=}')
        return

    settings_dict['default_settings_root'] = UFU.testplans_settings__all_default_dict
    settings_dict['default_settings_from_pid'] = testplan__default_name_list
    # settings_dict['variable_parameters'] = variable_parameters
    settings_dict['stand_testcases_list'] = stand_testcases_list
    settings_dict['protocol_creators'] = UFU.testplan_settings__by_short_pid.get('protocol_creators')
    settings_dict['testcases_for_protocol'] = UFU.testplan_settings__by_short_pid.get('testcases_for_protocol')
    settings_dict['measurement_settings'] = UFU.testplan_settings__by_short_pid.get('measurement_settings')

    if settings_dict['measurement_settings']:
        for measurement in settings_dict['measurement_settings']:
            settings = settings_dict['measurement_settings'][measurement].get('settings')
            if settings:
                for (k, v) in settings.items():
                    # начало спец. обработки
                    current_match = pattern.search(k)
                    if dict_params_enum and current_match:
                        """
                        Для параметров, описанных (в .JSON-файле с настройками) в виде:

                                    "'''command_from_ATLAS'''"
                                            либо
                        "любой_текст '''command_from_ATLAS'''"

                        используется особая обработка, где
                        command_from_ATLAS – это точное название параметра из слотового уст-ва.

                        Подразумевается, что данный метод используется только для параметров
                        с именованными значениями (т.е. с выбором значений из списка в "АТЛАСе")
                        и позволяет автоматически подгружать доступные значения
                        для текущего уст-ва.
                        """
                        command = current_match.group(1)
                        if command in dict_params_enum and dict_params_enum[command]:
                            dict_with_empty_values = UFU.dict_make_from_keys_list_with_none_values(
                                    tuple(dict_params_enum[command]))
                            try:
                                first_key = tuple(v.items())[0][0]
                            except:
                                first_key = None
                            v = UFU.dict_ensure_first_key(dict_with_empty_values, first_key=first_key)
                        else:
                            msg = f"Параметр '{command}' не имеет именованных значений в слотовом устройстве; использую данные из .JSON-файла настроек"
                            UFU.logging_and_print_info(msg)
                    # конец спец. обработки
                    if isinstance(v, dict):
                        """
                        Для параметров, описанных в .JSON-файле в виде
                        словарей с пустыми значениями (null) используется
                        упорядоченная обработка (необходимо для формирования
                        раскрывающегося "списка с выбором" в настройках измерений).
                        """
                        if UFU.dict_values_check_all_none(v):
                            try:
                                settings[k] = UFU.SettingsInt(v)
                                continue
                            except:
                                pass

                            try:
                                settings[k] = UFU.SettingsFloat(v)
                                continue
                            except:
                                pass

                            try:
                                settings[k] = UFU.SettingsString(v)
                                continue
                            except:
                                """ Convert OrderedDict to standard dict
                                (for MeasurementEditSettings class)
                                """
                                settings[k] = dict(v)
                        else:
                            """ Convert OrderedDict to standard dict
                                (for MeasurementEditSettings class)
                            """
                            settings[k] = dict(v)
            else:
                settings_dict['measurement_settings'][measurement] = {'settings': {}}

    if UFU.parse_channels_from_pid(pid):
        for each_measurement in settings_dict['measurement_settings']:
            if settings_dict['measurement_settings'][each_measurement]['settings']:
                for each_setting in settings_dict['measurement_settings'][each_measurement]['settings']:
                    if each_setting == 'Измеряемые каналы':
                        settings_dict['measurement_settings'][each_measurement]['settings'][
                            'Измеряемые каналы'] = UFU.parse_channels_from_pid(pid)
    return


def get_stand_testcases_list_and_settings_from_server_by_pid(settings_dict, pid):
    """ Reads .json-file from server by short_pid and
        replaces settings_dict from it if file exists.
    """
    short_pid = pid_short__get(pid)
    filepath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(short_pid, f'{short_pid}.json')

    if not filepath.exists():
        return

    try:
        testplan_settings__by_short_pid = ProcessorJsonDict().json_read(filepath).get(short_pid)
    except:
        return
    if testplan_settings__by_short_pid:

        if testplan_settings__by_short_pid.get('measurement_settings'):
            stand_testcases_list = list(testplan_settings__by_short_pid.get('measurement_settings').keys())
        else:
            UFU.logging_and_print_warning(f'Ошибка: для [{pid=}] нет доступных тесткейсов!')
            return

        settings_dict['stand_testcases_list'] = stand_testcases_list
        settings_dict['protocol_creators'] = testplan_settings__by_short_pid.get('protocol_creators')
        settings_dict['testcases_for_protocol'] = testplan_settings__by_short_pid.get('testcases_for_protocol')
        settings_dict['measurement_settings'] = testplan_settings__by_short_pid.get('measurement_settings')
        if settings_dict['measurement_settings']:
            for measurement in settings_dict['measurement_settings']:
                settings = settings_dict['measurement_settings'][measurement].get('settings')
                if settings:
                    for (k, v) in settings.items():
                        if isinstance(v, dict):
                            if UFU.dict_values_check_all_none(v):
                                try:
                                    settings[k] = UFU.SettingsInt(v)
                                    continue
                                except:
                                    pass

                                try:
                                    settings[k] = UFU.SettingsFloat(v)
                                    continue
                                except:
                                    pass

                                try:
                                    settings[k] = UFU.SettingsString(v)
                                    continue
                                except:
                                    """ Convert OrderedDict to standard dict
                                    (for MeasurementEditSettings class)
                                    """
                                    settings[k] = dict(v)
                            else:
                                """ Convert OrderedDict to standard dict
                                    (for MeasurementEditSettings class)
                                """
                                settings[k] = dict(v)

        if UFU.parse_channels_from_pid(pid):
            for each_measurement in settings_dict['measurement_settings']:
                if settings_dict['measurement_settings'][each_measurement]['settings']:
                    for each_setting in settings_dict['measurement_settings'][each_measurement]['settings']:
                        if each_setting == 'Измеряемые каналы':
                            settings_dict['measurement_settings'][each_measurement]['settings']['Измеряемые каналы'] = \
                                UFU.parse_channels_from_pid(pid)


def update_measurement_settings_in_json_by_pid(measurement_class,
                                               measurement_settings_dict,
                                               pid,
                                               testcases_for_protocol,
                                               protocol_creators,
                                               user_path=None):
    """ Updates measurement settings in "*_settings.json" files from DIRPATH_TESTPLANS_SETTINGS
        with given measurement_settings_dict by pid and measurement_class.

        :param user_path: If not `None` than updates measurement settings
        in "*_settings.json" files from ./user_path/data/settings/. For
        example, ["users", "Инженер"].
        :type user_path: list
    """
    pid = pid_short__get(pid)
    settings_dir = os.path.abspath(os.path.join(*user_path, 'data', 'settings')) if user_path else CONSTANTS.DIRPATH_TESTPLANS_SETTINGS

    for file in os.listdir(settings_dir):
        if str(file).lower().endswith("_settings.json"):
            file_path = os.path.join(settings_dir, file)
            json_file_data = ProcessorJsonDict().json_read(file_path)
            testplan_settings__by_short_pid = json_file_data.get(pid)

            if testplan_settings__by_short_pid:
                if protocol_creators:
                    testplan_settings__by_short_pid['protocol_creators'] = protocol_creators

                if testcases_for_protocol:
                    testplan_settings__by_short_pid['testcases_for_protocol'] = testcases_for_protocol
                if measurement_settings_dict:
                    if 'measurement_settings' not in testplan_settings__by_short_pid:
                        testplan_settings__by_short_pid['measurement_settings'] = dict()
                    testplan_settings__by_short_pid['measurement_settings'][measurement_class] = {
                        'settings': measurement_settings_dict
                    }
                    settings_dict = testplan_settings__by_short_pid['measurement_settings'][measurement_class].get('settings')
                    if settings_dict:
                        for key, value in settings_dict.items():
                            if isinstance(value, UFU.SettingsInt) or \
                                    isinstance(value, UFU.SettingsFloat) or \
                                    isinstance(value, UFU.SettingsString):
                                temp_dict = dict()
                                temp_dict[str(value)] = None
                                for k in value.keys:
                                    temp_dict[str(k)] = None
                                settings_dict[key] = temp_dict
                                del temp_dict

                ProcessorJsonDict().json_dump(file_path, json_file_data)

                if measurement_settings_dict:
                    """ Restore SettingsString in 'MeasurementEditSettings' widget """
                    settings_dict = testplan_settings__by_short_pid['measurement_settings'][measurement_class].get('settings')
                    if settings_dict:
                        for key, value in settings_dict.items():
                            if isinstance(value, dict):
                                if UFU.dict_values_check_all_none(value):
                                    try:
                                        settings_dict[key] = UFU.SettingsInt(value)
                                        continue
                                    except:
                                        pass

                                    try:
                                        settings_dict[key] = UFU.SettingsFloat(value)
                                        continue
                                    except:
                                        pass

                                    try:
                                        settings_dict[key] = UFU.SettingsString(value)
                                        continue
                                    except:
                                        """ Convert OrderedDict to standard dict
                                        (for MeasurementEditSettings class)
                                        """
                                        settings_dict[key] = dict(value)
                                else:
                                    """ Convert OrderedDict to standard dict
                                        (for MeasurementEditSettings class)
                                    """
                                    settings_dict[key] = dict(value)
                return


def load_measurement_settings_from_json_by_pid(measurement_class, pid, dictionaries_list, user_file=None):
    """ Loads measurement settings from DIRPATH_TESTPLANS_SETTINGS/*_settings.json" files
        to given measurement_settings_dict by pid and measurement_class.

        :param user_file: абсолютный путь к файлу с пользовательскими настройками измерений.
        :type user_file: str
    """
    pid = pid_short__get(pid)
    if user_file is None:
        settings_dir = CONSTANTS.DIRPATH_TESTPLANS_SETTINGS
    else:
        settings_dir = os.path.dirname(user_file)

    for file in os.listdir(settings_dir):
        if str(file).lower().endswith("_settings.json"):
            file_path = os.path.join(settings_dir, file)
            json_file_data = ProcessorJsonDict().json_read(file_path)
            testplan_settings__by_short_pid = json_file_data.get(pid)

            if testplan_settings__by_short_pid:
                # STARICHENKO - заполнил эти строки комментариев
                # load_measurement_settings_from_json_by_pid("TC_PS__Requirements", "default_settings", ["default_settings",])
                # print(type(testplan_settings__by_short_pid))     # <class 'collections.OrderedDict'>
                # print(testplan_settings__by_short_pid)
                # print(testplan_settings__by_short_pid['cu_psu'])
                # print(testplan_settings__by_short_pid['cu_psu']["measurement_settings"])
                # print(testplan_settings__by_short_pid['cu_psu']["measurement_settings"]["TC_PS__Requirements"]["settings"])

                if testplan_settings__by_short_pid['measurement_settings'].get(measurement_class):
                    settings = testplan_settings__by_short_pid['measurement_settings'][measurement_class].get('settings')
                    if settings:
                        for key, value in settings.items():
                            if isinstance(value, dict):
                                if UFU.dict_values_check_all_none(value):
                                    try:
                                        settings[key] = UFU.SettingsInt(value)
                                        continue
                                    except:
                                        pass

                                    try:
                                        settings[key] = UFU.SettingsFloat(value)
                                        continue
                                    except:
                                        pass

                                    try:
                                        settings[key] = UFU.SettingsString(value)
                                        continue
                                    except:
                                        """ Convert OrderedDict to standart dict
                                        (for MeasurementEditSettings class)
                                        """
                                        settings[key] = dict(value)

                                else:
                                    """ Convert OrderedDict to standart dict
                                        (for MeasurementEditSettings class)
                                    """
                                    settings[key] = dict(value)

                        for settings_dict in dictionaries_list:
                            settings_dict.update(settings)


def export_pids_to_pmi_excel(payload: dict, file_excel_path="", page="", start_cell=(2, 2)):    # NOBODY USE IT!
    """Экспорт данных в файл ПМИ Excel через win32com.client.Dispatch - COM-объект.

    :param payload: Данные для записи в файл. Ключи словаря - заголовки будущей таблицы, значения словаря - данные для
    построчной записи под соответствующий заголовок.
    :type payload: dict

    :param file_excel_path: Путь к файлу Excel. Должен в себе содержать путь и имя файла. Если не указан, то
    используется стандартный файл "\\dfs2\\14_OTK\\Автоматизация тестирования\\Актуальный TEST_SYSTEM\\ПМИ.xlsx".
    :type file_excel_path: str | Path

    :param page: Лист книги Excel для записи в него полученных данных. Лист по умолчанию: "Список устройств в TS".
    :type page: str

    :param start_cell: Адрес ячейки Excel, с которой начнется запись данных на лист. Соответствует формату
    (cow, column).
    :type start_cell: tuple(int, int)

    Экспорт сделан "в лоб" без использования библиотеки MeasurementProtocolHandler из модуля
    measurement_protocol.measurement_protocol_handler.
    """

    if not payload or not isinstance(payload, dict):
        print("Нет данных для записи в Excel.")
        return
    file_path = pathlib.Path(file_excel_path) if file_excel_path else CONSTANTS.FILEPATH_SERVER_PMI
    sheet_name = page if page else 'Список устройств в TS'
    if not file_path.exists():
        print(f"Не найден указанный файл Excel: {file_path}.")
        return
    if not file_path.is_file():
        print("Указанный путь не является файлом.")
        return
    if not isinstance(start_cell, tuple) or len(start_cell) != 2 or not isinstance(start_cell[0], int) or \
            not isinstance(start_cell[1], int):
        print(f"Не корректный формат стартовой ячейки для записи данных. Ожидается (int, int). Получен {start_cell}")
        return

    print(f"Будем читать файл Excel: '{file_path}'. Лист для записи '{sheet_name}'.")

    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel_default_flags = {
            "Visible": excel.Visible,
            "DisplayAlerts": excel.DisplayAlerts
        }
        excel.Visible = False  # True - Интерактивный режим работы с приложением.
        excel.DisplayAlerts = True  # True - Отключение предупредительных окон.
        wb_opened = [i for i in excel.Workbooks if i.Name == file_path.name]  # Проверяем, что книга есть в открытых.
        work_book = wb_opened[0] if wb_opened else excel.Workbooks.Open(file_path)  # Выбираем открытую или открываем.
        try:
            sheet = [i for i in work_book.Sheets if i.Name == sheet_name]  # Выбираем лист
            if not sheet:
                print(f"Не найден лист '{sheet_name}'.")
                return
            else:
                sheet = sheet[0]

            work_sheet = work_book.Worksheets(sheet.index)
            # Внимание! Excel заполняет диапазон данными как массив массивов строк с значениями по колонкам через
            #  запятую.
            # Примеры заполнения диапазона excel данными.
            # work_sheet.Range("D2:F3").Value = [["zЯч.D2", "zЯч.E2", "zЯч.F2"], ["zЯч.D3", "zЯч.E3", "zЯч.F3"]]
            # work_sheet.Range("D4:D6").Value = [["zЯч.D4"], ["zЯч.D5"], ["zЯч.D6"]]
            # print(f"Контроль чтения ячейки Cell({start_cell[0]},{start_cell[1]}) = "
            #       f"{work_sheet.Cells(start_cell[0], start_cell[1]).Value}")

            head_row = start_cell[0]
            current_row = start_cell[0] + 1
            current_column = start_cell[1]
            for k, v in payload.items():
                # print(f"=== {k}, {len(v)}, {head_row}, {current_row}, {current_column}")
                work_sheet.Cells(head_row, current_column).Value = k  # Заголовок колонки
                column_name = _ExcelProcessor.column_get_name_by_number(current_column)
                range_as_str = f"{column_name}{current_row}:{column_name}{len(v) - 1 + current_row}"
                # print(f"\t{column_name}, {range_as_str}")
                work_sheet.Range(range_as_str).Value = [[i] for i in v]  # Запись данных в одну колонку
                current_column += 1

        except Exception as data_err:
            print(f"Ошибка обработки данных при работе с Excel. {data_err!r}")

        try:
            print("Сохраняем книгу")
            work_book.Save()
        except Exception as save_err:
            print(f"{save_err!r}")
        try:
            print("Закрываем книгу")
            work_book.Close()
        except Exception as wb_err:
            print(f"{wb_err!r}")
        try:
            print("Восстанавливаем флаги Excel к состоянию до запуска")
            excel.Visible = excel_default_flags.get("Visible", False)
            excel.DisplayAlerts = excel_default_flags.get("DisplayAlerts", False)

            # Закрытие приложения не обязательно, т.к. реализация выше позволяет работать с уже открытыми книгами.
            # Поэтому можете смело для отладки закомментировать строку с excel.Quit().
            print("Закрываем приложение Excel")
            excel.Quit()
        except Exception as excel_err:
            print(f"{excel_err!r}")

    except Exception as excel_err:
        print(f"ОШИБКА работы с Excel. {excel_err!r}")
        return
    return True


# =====================================================================================================================
def return_last_SrNumber_from_server_by_pid(pid):
    """ Returns last serial number (by protocol file names)
        from pid-folder on server.
    """
    dirpath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(pid_short__get(pid))

    if not dirpath.exists():
        return None

    result_list = []
    for filepath in dirpath.glob("T8*"):
        result_list.append(filepath.name)

    return sorted(result_list)[-1]


def return_last_SrNumber_increased_by_one_from_server_by_pid(pid):
    """ Returns last serial number (by protocol file names), increased by one,
        from pid-folder on server. Otherwise returns None.
    """
    SrNumber = return_last_SrNumber_from_server_by_pid(pid)
    if not SrNumber:
        return None

    pattern = r'(.+[.])(\d+)'
    current_match = re.match(pattern, SrNumber)
    if current_match:
        length_of_last_group = len(str(current_match.group(2)))
        return current_match.group(1) + str(int(current_match.group(2)) + 1).zfill(length_of_last_group)

    return None


def check_SrNumber_else_get_last_from_server_and_write_to_device(SrNumber=None, DUT=None, pid=None):
    """ Checks if serial number is in device or tries
        to write last serial number from server (increased by one) to device.
        Returns serial number.
    """
    try:
        sn = DUT.conn.CACHE.SN
    except:
        sn = None

    if not sn:
        if not SrNumber:
            SrNumber = return_last_SrNumber_increased_by_one_from_server_by_pid(pid)

        if not SrNumber:
            UFU.logging_and_print_warning('Ошибка сохранения протокола: невозможно получить последний серийный номер с сервера')
            return None

        else:
            try:
                super(type(DUT.conn), DUT.conn). \
                    write_param(DUT.conn.slot_uid, 'SrNumber', SrNumber)
                time.sleep(1)
            except:
                UFU.logging_and_print_warning('Ошибка сохранения протокола: невозможно записать в устройство серийный номер')

    elif not SrNumber:
        return sn

    return SrNumber


def export_protocol_to_server(source, pid=None):
    """ Exports protocol to CPl.DIRPATH_SERVER_PROTOCOLS by short_pid-folder.
    """
    if pid:
        short_pid = pid_short__get(pid)
        dirpath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(short_pid)
        filepath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(short_pid, os.path.basename(source))
    else:
        dirpath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS
        filepath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(os.path.basename(source))

    if not dirpath.exists():
        UFU.logging_and_print_warning('Ошибка: на сервере нет папки с таким pid')
        return

    if filepath.exists():
        UFU.logging_and_print_warning('Ошибка: файл с таким же именем уже существует на сервере')
        return

    try:
        copyfile(source, filepath)
    except:
        UFU.logging_and_print_warning('Ошибка: невозможно экспортировать протокол на сервер')
        return

    try:
        os.remove(os.path.realpath(source))
    except:
        UFU.logging_and_print_warning('Ошибка: невозможно удалить локальный протокол')

    return True


def copy_protocol_template_from_server_by_pid(copy_path, pid):
    """ Copies protocol template from CONSTANTS.DIRPATH_SERVER_PROTOCOLS by short_pid-folder
        to copy_path.
    """
    short_pid = pid_short__get(pid)
    filepath = CONSTANTS.DIRPATH_SERVER_PROTOCOLS.joinpath(short_pid, short_pid + '.xlsx')

    if not filepath.exists():
        UFU.logging_and_print_warning('Ошибка: на сервере нет шаблона протокола с таким pid')
        return

    try:
        copyfile(filepath, copy_path)
        return True
    except:
        UFU.logging_and_print_warning('Ошибка: невозможно скопировать шаблон протокола')


# =====================================================================================================================
