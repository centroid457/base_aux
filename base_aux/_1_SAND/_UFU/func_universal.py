# =====================================================================================================================
import time
import pathlib
import typing as tp

import csv
import json
import functools
import logging
import multiprocessing.pool
import os
import sys
import random
import re
import copy
import string
import inspect
import ipaddress
import socket
import winsound
import datetime
import numpy as np
from multiprocessing.context import TimeoutError
from platform import system
from subprocess import check_output
from importlib import import_module
from threading import Thread

# CONSTANTS ===========================================================================================================
# VALUES --------------------------------------------------------------------------------------------------------------
TYPE_DATA_ALL_DICT = {
    str: ["", " ", "123", " 123 ", "123.123"],
}

STR_NODATA_VALUE = "######"
STR_EXCEPTION_MARK = "***STR_EXCEPTION_MARK***"
STR_NOT_INPUTED_MARK = "***STR_NOT_INPUTED_MARK***"
STR_PATTERN_FOR_PYTEST_FAIL_MSG = "PYTEST_FAIL_MSG func_tested=[{}] params_dict={}::((( result=[{}] != expected=[{}] )))"  # starichenko

DICT_EXCEPTION_EXPLANATION = {     # starichenko
    # CUMULATIVE USER DICT for all errors!

    # todo: use like flattern/nested! OVER find_by_dict!!!
    # todo: maybe delete!
    # 1=SERIAL ================================================================
    # 1=OPEN errors -----------------------------------------------------------
    "OSError(22, 'Указано несуществующее устройство.', None, 433)":
        f"MAYBE YOU HAVE A PROBLEM WITH DRIVER!!! like PL2303",
    "FileNotFoundError(2, 'Не удается найти указанный файл.', None, 2)":
        f"MAYBE YOU TRY OPEN NOT EXISTS PORT???",
    "PermissionError(13, 'Отказано в доступе.', None, 5)":
        f"ALREADY WAS OPENED!!!!?????",
    "OSError(22, 'Недостаточно системных ресурсов для завершения операции.', None, 1450)":
        f"maybe you try to open VIRTUAL serial port (like Moxa nPort5150) wich was disconnected",

    # 2=READ errors -----------------------------------------------------------

    # 3=WRITE errors -----------------------------------------------------------

    # 1=SOCKET ================================================================
    "[WinError 10057] Запрос на отправку или получение данных  (when sending on a datagram socket using a sendto call) no address was supplied":
        f"PORT_ADDRESS WAS NOT SETTED!!!",
    # 1=OPEN errors -----------------------------------------------------------

    # 2=READ errors -----------------------------------------------------------
    "[WinError 10038] Сделана попытка выполнить операцию на объекте, не являющемся сокетом":
        f"ADDRESS WAS NOT SELECTED!!!",
    "timed out":
        f"TIMEOUT EXCEEDED!!! NO CONNECTION (POWEROFF) OR ALREADY BUSY BY ANOTHER CLIENT!"
    # 3=WRITE errors -----------------------------------------------------------

}   # starichenko

FUNC_LINK_LAMBDA_TRUE = lambda _=None: True     # starichenko # if you want co compare equality any func_link with LambdaTrue - use it constant link!!!
FUNC_LINK_LAMBDA_FALSE = lambda _=None: False
FUNC_LINK_LAMBDA_NONE = lambda _=None: None
FUNC_LINK_LAMBDA_REPEATER = lambda input=None: input

LIST_RUSSIAM_LETTERS_LOWERCASE = list("абвгдеёжзийклмнопрстуфхцчшщъыьэю")
LIST_RUSSIAM_LETTERS_UPPERCASE = list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮ")
LIST_RUSSIAM_LETTERS_ALLCASE = LIST_RUSSIAM_LETTERS_LOWERCASE + LIST_RUSSIAM_LETTERS_UPPERCASE

LIST_FILESYSTEM_WRONG_NAME_CHARS = list("\\/:*?\"<>|")


# SOUND ===============================================================================================================
def _sound(freq=1000, duration=500):
    winsound.Beep(freq, duration)


def sound_ask():
    for i in range(1):
        _sound(1500, 1000)


def sound_error():
    for i in range(2):
        _sound(1500, 200)
        time.sleep(0.2)


# 0=MSG ===============================================================================================================
def _msg_create_block_title(msg, start_char, finish_char, len_chars=100):
    msg = f"{start_char * len_chars}\n" \
          f"{msg}\n" \
          f"{finish_char * len_chars}\n"
    return msg


def msg_create_block_title_start(msg, start_char="#", finish_char="-", len_chars=100):
    return _msg_create_block_title(msg=msg, start_char=start_char, finish_char=finish_char, len_chars=len_chars)


def msg_create_block_title_finish(msg, start_char="-", finish_char="#", len_chars=100):
    return _msg_create_block_title(msg=msg, start_char=start_char, finish_char=finish_char, len_chars=len_chars)


# 0=LOGGERS ===========================================================================================================
def _log_and_print(msg="", type_0i_1d_2w_3e=1, _debug_mod=None):     # starichenko
    """ print msg to stdout and logging

    :param msg: exact message to logging - CAN BE ANY TYPE!!! inside it will be get STR()
    :param type_0i_1d_2w_3e: type of logging
    :poram _debug_mod:
        if True - msg wil be printing to stdout and in loggingType
        IF False - only logging except DebugType!
    """
    msg = f"[{debug_get_file_and_func_for_parent_frame_not_debug()[1]}]{msg}"

    # 1=additional stdout printing -------------
    if _debug_mod:
        print(msg)

    # 2=work -----------------------------------
    if type_0i_1d_2w_3e == 0:
        logging.info(msg)
    elif type_0i_1d_2w_3e == 1:  # use only for debug!!!
        logging.debug(msg)
    elif type_0i_1d_2w_3e == 2:
        logging.warning(msg)
    elif type_0i_1d_2w_3e == 3:
        sound_error()
        logging.error(msg)


def logging_and_print_info(msg=""):     # starichenko
    _log_and_print(msg, type_0i_1d_2w_3e=0)


def logging_and_print_debug_or_warning(msg="", result=None):     # starichenko
    """
    :param result: will use as desition to call warning or debug
    """
    msg = f"{msg}[{result=}]"
    if bool(result):
        logging_and_print_debug(msg)
    else:
        logging_and_print_warning(msg)


def logging_and_print_debug(msg="", _debug_mod=None):     # starichenko
    _log_and_print(msg, type_0i_1d_2w_3e=1, _debug_mod=_debug_mod)


def logging_and_print_warning(msg=""):     # starichenko
    _log_and_print(msg, type_0i_1d_2w_3e=2)


def logging_and_print_error(msg=""):  # starichenko
    # use it only in critical situation! only in testcase result!!! in other ones use WARNING ONLY!
    _log_and_print(msg, type_0i_1d_2w_3e=3)


def logging_debug_class_and_func_names(self_obj=None, _debug_mod=None):  # starichenko
    if not _debug_mod:
        return

    msg = debug_stack_or_obj_get_class_and_func_names(self_obj)
    logging_and_print_debug(msg)


def log_error_explanation_by_dict(exx, exx_dict=None, operation_name=None):     # starichenko
    """
    :param exx: Exception object
    :param exx_dict: user explanation dict for errors - usually found errors!
    :param operation_name: string describing operation! usually name of function
    """
    logging_and_print_debug(f'1=[{operation_name}][{type(exx)}][{exx}] UNEXPECTED ERROR')

    if exx_dict is None:
        exx_dict = DICT_EXCEPTION_EXPLANATION

    # KNOWN ERRORS!
    key, value = value_search_by_dict_return_key_and_value(
        source=str(exx),
        search_dict=exx_dict,
        search_type_1starts_2full_3ends_4any_5fullmatch=4
    )
    if value:
        msg = f"2=operation=[{operation_name}] error_explanation=[{value}]"
        logging_and_print_warning(msg)


# DEBUG ===============================================================================================================
def debug_stack_or_obj_get_class_and_func_names(self_obj=None, _debug_mod=None):  # starichenko
    """ logging point in code by ClassName and Function!

    :param self_obj: if passed in - will show Class name! else only func name!
    """
    if not _debug_mod:
        return

    parent_file, parent_func = debug_get_file_and_func_for_parent_frame_not_debug()

    if self_obj:
        class_name = self_obj.__class__.__name__
    else:
        class_name = pathlib.Path(parent_file).name

    return f"[{class_name}][{parent_func}]"


# STACK ---------------------------------------------------------------------------------------------------------------
def debug_stack_get_list(
        print_column=True,
        filename_show_full=False,
        filename_dont_use=False,
        _debug_mod=None):    # starichenko
    """useful to print/log exact file+class/function point

    :param print_column: print in column! one step in one line!
    :param filename_show_full: in result use full abs-name or only filename+extension
    :param filename_dont_use: will show only function!
    :param dont_start: this function spends a lot of time and you can simply disable it
    """
    if not _debug_mod:
        return
    # print("1=currentframe", inspect.currentframe())   # <frame at 0x000001C74197E440, file 'C:/!_HPN277SR/!!!_GD_additional/4.py', line 3, code <module>>
    # print("2=stack", inspect.stack())   # [FrameInfo(frame=<frame at 0x000001846A50E440, file 'C:/!_HPN277SR/!!!_GD_additional/4.py', line 4, code <module>>, filename='C:/!_HPN277SR/!!!_GD_additional/4.py', lineno=4, function='<module>', code_context=['print(inspect.stack())   #\n'], index=0)]
    # print(inspect.trace())   # []

    current_frame = inspect.currentframe()
    # print("3=getframeinfo", current_frame)   # Traceback(filename='C:/!_HPN277SR/!!!_GD_additional/4.py', lineno=8, function='<module>', code_context=['print(inspect.getframeinfo(frame))   # []\n'], index=0)

    outer_frames_stack = inspect.getouterframes(current_frame)
    # print("4=getouterframes", outer_frames_stack)   #

    stack_list = []
    for step_frame in outer_frames_stack[::-1][0:-1]:
        step_file = step_frame.filename
        if not filename_show_full:
            step_file = pathlib.Path(step_file).name
        step_line = step_frame.lineno

        step_func = step_frame.function
        if step_func == "<module>":
            step_func = "<ROOT>"

        if filename_dont_use:
            step_name = f"{step_func}"
        else:
            step_name = f"{step_file}[{step_line}]/{step_func}"

        stack_list.append(step_name)

    msg = f"=====STACK====={stack_list}"
    logging_and_print_debug(msg)

    if print_column:
        msg = f"{'v'*50} STACK {'v'*50}"
        logging_and_print_debug(msg)
        for step in stack_list:
            logging_and_print_debug(step)

        msg = f"{'^'*50} STACK {'^'*50}"
        logging_and_print_debug(msg)

    return stack_list


def debug_get_file_and_func_for_parent_frame_not_debug():     # starichenko
    """return func name from stack

    why its nesseccary if there are already special funcName key in logging?
    because if you will call from exact func separate debug func then you will see in logFile unfortunately DebugFuncName!
    """
    parent_file = None
    parent_func = None

    func_names_inner_debug_list = [
        "debug", "_debug",
        "logging", "_logging", "_log_", "_log",
        "inspect", "_inspect",
        # "debug_stack_or_obj_get_class_and_func_names", "logging_debug_class_and_func_names",
        # "_log_and_print"
    ]

    for i in range(10):
        parent_frame = inspect.stack()[i]
        parent_file = parent_frame.filename
        parent_func = parent_frame.function
        if not value_search_by_list(source=parent_func, search_list=func_names_inner_debug_list,
                                    search_type_1starts_2full_3ends_4any_5fullmatch=1):
            break

    return parent_file, parent_func


def import_module_get_link_by_str(module_name):   # starichenko
    """return object of imported module

    Example:
        openpyxl = module_imported_link = import_module_get_link_by_str("openpyxl")
        wb1 = openpyxl.Workbook()
        wb2 = module_imported_link.Workbook()
    """
    module_imported_link = None
    try:
        module_imported_link = import_module(module_name)
    except Exception as exx:
        msg = f"{exx!r}"
        logging_and_print_warning(msg)

    return module_imported_link


# MODULE PROCESSING ---------------------------------------------------------------------------------------------------
def import_obj_get_link_by_str(module_name, obj_name):   # starichenko
    """return object of imported object - class or function
    (module will be loaded whole code!)

    Example:
        obj_link = import_obj_get_link_by_str("openpyxl", "Workbook")
        wb1 = obj_link()
    """
    obj_link = None
    try:
        # module_imported_link = import_module(file_name + f".{obj_name}")  # ModuleNotFoundError("No module named 'test2.cls2'; 'test2' is not a package")
        module_imported_link = import_module(module_name)
        obj_link = getattr(module_imported_link, f"{obj_name}")
    except Exception as exx:
        msg = f"{exx!r}"
        logging_and_print_warning(msg)

    return obj_link


# DELETE!!!!!! # ============================================
pip_install_to_user_path = False


def module_install(module_name: str):   #old
    """Устанавливает модуль.

    :param module_name: Имя модуля, который требуется установить, используя pip.

    :return: bytes строка.
    :rtype: bytes
    """
    global pip_install_to_user_path
    out = None

    try:
        # Переделать установку модулей через библиотеку pip, т.к. после работы
        # check_output в консоль начинают идти все сообщения модуля logging.
        # После перезапуска приложения консоль с logging работает в нормальном режиме.
        out = check_output("pip install{} {}".format(" --user" if pip_install_to_user_path else "", module_name))
        logging.debug(f"Установлен модуль {module_name=}")
    except Exception as exx1:
        try:
            out = check_output(f"pip install --user {module_name}")
            pip_install_to_user_path = True
            logging_and_print_debug(f"Установлен модуль {module_name=}")
        except Exception as exx2:
            try:
                out = check_output(f"pip install --trusted-host "
                                   f"pypi.org --trusted-host files.pythonhosted.org {module_name}")
            except Exception as exx3:
                msg = f'ошибка установки модуля {module_name}//{exx3!r}//{exx2!r}'
                logging_and_print_warning(msg)
    return out


def modules_import():      # TODO: DO FULL REFUCT OR DEL!!! starichenko
    # TODO (yurgaev@t8.ru): Избавиться от этого. При импорте модуля не должно быть
    #  чтения каталога файлов. Реализовать как функцию в func_universal.py
    def recurs_installer(cnt_new):
        # print("cnt_new =", cnt_new)
        try:
            globals()[file[:-3]] = import_module('testplans.' + file[:-3])
        except ModuleNotFoundError as module_exc:
            if cnt_new >= cnt:
                print("Возможно не все импорты из модуля {} были разрешены".format(file))
                return
            get_msg = "Отсутствует python-модуль {} (импорт из модуля {})".format(
                module_exc.name, file[:-3])
            # print(get_msg)
            setup_status = module_install(module_exc.name)
            recurs_installer(cnt_new + 1)
        else:
            return

    for file in os.listdir(str(CONSTANTS.DIRPATH_TESTPLANS)):
        if file.lower().endswith("_measurement.py"):
            cnt = 5  # Предел рекурсивной установки недостающих python-модулей - Остановка рекурсии.

            recurs_installer(0)


# CLASSES PROCESSING --------------------------------------------------------------------------------------------------
def classes_get_dict_from_module(module_name=None, debug_print=True):  # starichenko
    """return all classes in 1st level in module.

    :param module_name: you can input module_name=__name__ from any other module_file to see its classes
        or imported module name!

    example:
        # clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        result = classes_get_dict_from_module(__name__)
    """
    if module_name is None:
        module_name = __name__

    if isinstance(module_name, type(sys.modules[__name__])):
        module_obj = module_name
    else:
        module_obj = sys.modules[module_name]

    print(dir(module_obj))

    class_tuple_list = inspect.getmembers(module_obj, inspect.isclass)
    class_dict = dict(class_tuple_list)

    if debug_print:
        print(type(module_name))
        print(type(module_obj))

        print(f"module_name=[{module_name}]")
        print(f"module_obj={module_obj}")
        print(f"class_dict={class_dict}")

    return class_dict


# OBJECTS PROCESSING --------------------------------------------------------------------------------------------------
def obj_link_get_by_name_in_files(name, path=None, file_pattern=None):      # starichenko
    """gives you ability to get class link by name in files

    must be used in all selectors/builders in TestSystem!!!
    usefull place it by separate file in dir where moduls will find! - so you dont need to pass in directry path! only object name!

    :param name: class name you want to get link
    :param path: path to directory (will find in all files) or file (will find only in it!)
        or None - for CWD path! but i think you need pass in
    :param file_pattern: USUAL WILDMASK!! NOT REGEXP!!!
        only if you want to specify exact filename or several by wildcard
    """
    # INPUT -------------------------------------------------------------------------------------------------------
    if not name:
        return

    file_pattern = file_pattern or '*.py'

    path = pathlib.Path(path or ".")
    if path.is_file():
        file_iter = [path, ]
        dir_root_find = path.parent
    elif path.is_dir():
        file_iter = path.rglob(file_pattern)
        dir_root_find = path

    # WORK --------------------------------------------------------------------------------------------------------
    obj_link = None
    for path_obj in file_iter:
        # print(f"[{path_obj=}]")
        if path_obj.is_file() and "py" in path_obj.suffix:

            # 1=create ability to import module
            dir_obj = path_obj.parent

            dir_str = str(dir_obj.resolve())
            flag_dir_was_in_sys = dir_str in sys.path
            sys.path.append(dir_str)

            try:
                mobule_imported = import_module(path_obj.stem)
                obj_link = getattr(mobule_imported, f"{name}")
                break
            except:
                # 10=reverse state
                msg = f"module was not found [{name=}/{dir_str=}]"
                logging_and_print_debug(msg)
                if not flag_dir_was_in_sys:
                    sys.path.remove(dir_str)

    # RESULT ------------------------------------------------------------------------------------------------------
    if obj_link is None:
        msg = f"module was not found [{name=}/{dir_root_find=}]"
        logging_and_print_warning(msg)

    return obj_link


def obj_get_name(source):  # starichenko
    """
    Gets the name of object - useful for CONSTANTS (was created for!!!) and other obj wich dont have __name__ attribute!
    Does it from the out most frame inner-wards.

    :param source: variable to get name from.
    :return: string

    when testing must check inner usage!!!
        def use_inner(var):
            print(obj_get_name(var))

        x, y, z = 1, 2, 3
        use_inner(y)    # y

        x, y, z = 1, 2, 2
        use_inner(y)    # y

    examples:
        obj_get_name(int)   # name=[int] value=[<class 'int'>]
        obj_get_name(3)     # name=[source] value=[3]
        obj_get_name("abc") # name=[source] value=[abc]
        abc = 100
        obj_get_name(abc)   # name=[abc] value=[100]
    """
    result_str = None

    if hasattr(source, '__name__'):
        result_str = source.__name__

    else:
        for fi in reversed(inspect.stack()):
            names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is source]
            if len(names) > 0:
                result_str = names[0]
                break

    msg = f"name=[{result_str}] value=[{source}]"
    logging_and_print_debug(msg)

    return result_str

def obj_elements_get_dict_all(source, show_builtin=False):       # starichenko
    """get all (module/class/instance/meth/attr) element for object

    :return: dict of element names with values
    """
    result = {}
    for element_name in dir(source):
        element_value = getattr(source, element_name)

        if not show_builtin and element_name.startswith("__"):
            continue

        # if all([not atr_or_method_name.startswith("__"),            # исключение магических методов и атрибутов
        #         not callable(atr_or_method_value),                  # исключение методов
        #         not hasattr(atr_or_method_value, "__module__")]):   # исключение объектов в атрибутах
        result.update({element_name: element_value})
    return result


# 0=CLASSES ===========================================================================================================
# TODO starichenko: DELETE THIS MO**FU***

class SettingsString(str):
    """ Subsidiary class of string-type
        for such measurement setting, which value is 'dict with empty values'
        (i.e. values are 'null' in .JSON-file, 'None' in Python).
        When class is called it returns only the first key instead of all items.
        Attribute 'SettingsString.keys' contains a set of all other keys.

        Class is used for storing and selecting one string from several ones.
    """

    def __init__(self, ordered_dict_with_empty_values):
        first_key = list(ordered_dict_with_empty_values)[0]
        self.keys = set(ordered_dict_with_empty_values) - set([first_key])
        return str.__init__(self)

    def __new__(self, ordered_dict_with_empty_values):
        first_key = str(list(ordered_dict_with_empty_values)[0])
        return str.__new__(self, first_key)


class SettingsInt(int):
    """ Subsidiary class of integer-type
        for such measurement setting, which value is 'dict with empty values'
        (i.e. values are 'null' in .JSON-file, 'None' in Python).
        When class is called it retuns only the first key instead of all items.
        Attribute 'SettingsInt.keys' contains a set of all other keys.

        Class is used for storing and selecting one integer number
        from several base_types.
    """

    def __init__(self, ordered_dict_with_empty_values):
        first_key = list(ordered_dict_with_empty_values)[0]
        self.keys = set(ordered_dict_with_empty_values) - set([first_key])
        return int.__init__(self)

    def __new__(self, ordered_dict_with_empty_values):
        first_key = int(list(ordered_dict_with_empty_values)[0])
        return int.__new__(self, first_key)


class SettingsFloat(float):
    """ Subsidiary class of float-type
        for such measurement setting, which value is 'dict with empty values'
        (i.e. values are 'null' in .JSON-file, 'None' in Python).
        When class is called it retuns only the first key instead of all items.
        Attribute 'SettingsFloat.keys' contains a set of all other keys.

        Class is used for storing and selecting one float number
        from several base_types.
    """

    def __init__(self, ordered_dict_with_empty_values):
        first_key = list(ordered_dict_with_empty_values)[0]
        self.keys = set(ordered_dict_with_empty_values) - set([first_key])
        return float.__init__(self)

    def __new__(self, ordered_dict_with_empty_values):
        first_key = float(list(ordered_dict_with_empty_values)[0])
        return float.__new__(self, first_key)


class _ClsCountExecutions:     # starichenko
    """special class for testing func_links!!!

    main idea - count times of execution methods!
    specially created for PyTesting funcs_all_true by parametrize!

    all params in methods shown only for ability to work with any params (no matter what and how much it would be)
    """
    COUNT = 0
    VALUE = "HELLO-1"

    def __init__(self):
        self._increase()
        print(f"self.__class__.COUNT=[{self.__class__.COUNT}]")

    # MISC -----------------------------------------------------
    @classmethod
    def set_value(cls, value="HELLO-2"):
        cls.VALUE = value

    @classmethod
    def _increase(cls):
        cls.COUNT += 1          # real counter

    @classmethod
    def _clear_counter(cls, _=None, **kwargs):
        cls.COUNT = 0

    # RETURNS WO --------------------------------------------------
    @classmethod
    def TRUE(cls, _=None, **kwargs):
        cls._increase()
        return True

    @classmethod
    def FALSE(cls, _=None, **kwargs):
        cls._increase()
        return False

    @classmethod
    def NONE(cls, _=None, **kwargs):
        cls._increase()
        return None

    @classmethod
    def EXCEPTION(cls, _=None, **kwargs):
        cls._increase()
        raise Exception()

    @staticmethod
    def TRUE_no_increase(_=None, **kwargs):
        return True

    @staticmethod
    def FALSE_no_increase(_=None, **kwargs):
        return False

    @staticmethod
    def NONE_no_increase(_=None, **kwargs):
        return None

    @staticmethod
    def EXCEPTION_no_increase(_=None, **kwargs):
        raise Exception()


# DECORATORS ==========================================================================================================
def TEMPLATE_decorator_for_class_method(_func_link):    # starichenko
    """
    this is only TAMPLATE for decorator! use it like a sample!
    works on INIT! like any others!)

    :param _func_link:
    :return:

    TESTING:
        class Cls:
            @decorator_for_class_method
            def __init__(self):
                print(f"INIT")

            @decorator_for_class_method
            def method(self, hello):
                print(hello)

        cls_obj = Cls()
        cls_obj.method("hello")
    """
    @functools.wraps(_func_link)
    def _wrapper_for_class_method(self, *args, **kwargs):
        # print(f"decorating[{self.__class__.__name__}.{_func_link.__name__}()]")
        return _func_link(self, *args, **kwargs)

    return _wrapper_for_class_method


def decorator_timeout(max_timeout, default=STR_EXCEPTION_MARK):
    """Timeout decorator.

    :param max_timeout: in seconds
    :param default: if timeout expected return the default
    """
    def _timeout_decorator(_func_link):
        """Wrap the original function."""

        @functools.wraps(_func_link)
        def _wrapper(*args, **kwargs):
            """Closure for function."""
            global _function_finished_flag
            _function_finished_flag = False
            try:
                pool = multiprocessing.pool.ThreadPool(processes=1)
                async_result = pool.apply_async(_func_link, args, kwargs)
                result = async_result.get(timeout=max_timeout)
                return result
            except TimeoutError:
                pool.close()
                _function_finished_flag = True
                return default

        return _wrapper
    return _timeout_decorator


def decorator_try__return_none_and_log_explanation(_func_link):     # starichenko
    """ PLACE IT ONLY ON _ONLY_*** methods!!!!

    first created for explaining errors in Connection Protocols and return None in case oа error!!

    if you need to pass in a special argument for decorator? create it only here!!!
    """
    @functools.wraps(_func_link)
    def _wrapper(*args, **kwargs):
        # 1=separate decorator args! --------------------------------------------
        _DECORATOR_show_error = True
        if "_DECORATOR_show_error" in kwargs:
            _DECORATOR_show_error = kwargs.pop("_DECORATOR_show_error")

        # 2=work ----------------------------------------------------------------
        result = None
        try:
            result = _func_link(*args, **kwargs)
        except Exception as exx:
            if _DECORATOR_show_error:
                logging_and_print_warning(f"{exx!r}")
                log_error_explanation_by_dict(exx=exx, operation_name=_func_link.__name__)
        return result
    return _wrapper


def decorator_start_in_thread(_func_link):
    @functools.wraps(_func_link)
    def _wrapper(*args, **kwargs):
        thread = Thread(target=lambda: _func_link(*args, **kwargs), daemon=1)
        thread.start()
    return _wrapper


# FUNCTION PROCESSING =================================================================================================
def func_get_arg_names_list(func_link):   # starichenko
    func_name = func_link.__name__

    params = inspect.signature(func_link).parameters
    msg = f"func_link.name=[{func_name}] introspect params=[{params}]"
    logging_and_print_debug(msg)
    return list(params)


# TODO: make CLASS!!!
def funcs_all_true(funcs_link_sequence=[], flag_run_all=False, func_link_with_final_result=None):   # STARICHENKO
    """ Выдает True. если все функции дали ожидаемый ответ.
    Если хоть одна функция не дала ожидаемое - остановка и выход (по умолчанию).
    поведение очень заумно настраивается флагами!

    1=DECIDE_TO_RUN ----------------------------
    if you want to decide run sequence at first
        use key "decide_run_sequence"=True in first items! you can use several one-by-one!
        can be only a dict
            question        - question for func
            func_link       - exact func link
            expected_answer - [True is default] expected exact(!!!) answer
            decide_run_sequence - exact flag to use in First element!
            result_sequence_if_decided_run_fail - useful if you really want return True in Fail case

    2=FUNCS_LINK_SEQUENCE ----------------------
    :param funcs_link_sequence:
        can be sequence of any two variants in any combination
            1= func_link - not recommended!!! if find - please rebuild to recommended!!!
            2= dict with structure (in any key value you can use None - it will be correct to get default!)
                    question            - question for func
                    func_link           - exact func link
                    expected_answer     - [True is default] expected exact(!!!) answer
                    use_answer          - if False - check expected answer only for info! and dont have effect on final result!
                    skip                - skip if True - question will be shown

                1ST LEVEL RULE EXCEPTION
                    always1_run         - if True step will be executed always!

                2ND LEVEL RULE EXCEPTION
                    always2_stop_if_step_false- WORK ГАЕУК STEP LINK!!! if True and get FalseAnswer in step func in any case run sequence will be stoped!
                    always2_stop_if_was_false- WORK ONLY BEFORE STEP_LINK!!! if True and get FalseAnswer in any func before in any case run sequence will be stoped!
                        IMPORTANT!!!! use as along trigger without func!!!
                            # always2_stop_if_was_false ===========================================================================
                            {"always2_stop_if_was_false": True},
                            # always2_stop_if_was_false ===========================================================================

                        by now i dont know if it usable!!! may be deprecated!
                    func_link_if_correct    -
                    func_link_if_wrong      -
                    func_link_if_exception  - if Not specified - will accept as func_link_if_wrong

                    func_link_with_result   - you can use it if you need to write result it results

    :param flag_run_all:
        False - stop executing on first False-Incorrect answer that is used!
        True - continue executing all funcs after get False from any of them and return False if any get False!

    :returns: if in sequence was FALSE or NONE - return False! else True!
        so if sequence is blank - return True!!!

    =================================================================================================================
    ПРИМЕРЫ ПРИМЕНЕНИЯ по возрастанию сложности:
    Замечание - все функции с их вопросами и результатами (Correct/Incorrect/Missed)
        всегда будут пролистаны в выводе! независимо от флагов остановки!

    -----------------------------------------------------------------------------------------------------------------
    1. ВСЕ ПАРАМЕТРЫ ПО-УМОЛЧАНИЮ
        выполнятся все до первого Fail
        - если добавить [use_answer]=False тогда некоторые функции если и дадут Wrong то это не остановит выполнения остальных!
        - если добавить [always1_run]=True тогда step функции будут выполнены всегда независимо от фактической остановки!
            НО они перестанут выполняться, если будет остановка по логике [always2_stop_*]
            поэтому если нужно иметь несколько групп функций и в определенный момент отключить их исполнение - этот случай удобен!!!

    2. ВКЛЮЧАЕМ [flag_run_all]
        при получении Wrong исполнение остальных функций не остановится! все выполнятся и в конце будет общий результат
        - параметр [always1_run] не работает потому что безсмысленнен! (возможно будет включен в будущем как перебивка always2)
        - если добавить [always2_stop_*] и логика сработает - то последующие шаги выполняться не будут - собственно для этой цели и созданы always2_stop_*
    """
    # todo: add nested availability!!!

    # flags main
    flag_sequence_was_false = None             # sequence get FalseResult in func with use_answer
    flag_sequence_always2_stop_if_step_false = False  # sequence get FalseResult in func with always2_stop_if_step_false

    # INPUTS
    type_check_by_variants(funcs_link_sequence, [list, tuple])

    # ===================================================================================================
    # 1=DECIDE TO RUN - may be only as first items group in sequence
    while True:
        # if seqгутсу have only elements that are all decide_to_run
        if len(funcs_link_sequence) == 0:
            return True

        item_decide_run = funcs_link_sequence[0]
        if isinstance(item_decide_run, dict) and ("decide_run_sequence" in item_decide_run) and item_decide_run.get("decide_run_sequence"):
            item_decide_run = funcs_link_sequence.pop(0)

            question = dict_value_get_with_default_and_replacing(item_decide_run, "question", "", [None])
            func_link = dict_value_get_with_default_and_replacing(item_decide_run, "func_link", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link):
                raise Exception(f"incorrect input type func_link=[{func_link}] =need CALLABLE!")
            expected_answer = item_decide_run.get("expected_answer", True)
            result_sequence_if_decided_run_fail = item_decide_run.get("result_sequence_if_decided_run_fail", None)

            if func_link() == expected_answer:
                logging_and_print_info(f"[0] DECIDE_TO_RUN question=[{question}]? --> CORRECT decide_run_sequence!")
            else:
                logging_and_print_warning(f"[0] DECIDE_TO_RUN question=[{question}]? --> FAIL decide_run_sequence!")
                return result_sequence_if_decided_run_fail
        else:
            break

    # 2=RUN =====================================================================================================
    step_prefix = random.choice("!@#$%^&*_-+=,.:;?<>")
    step_index = 0
    for item in funcs_link_sequence:
        step_index += 1
        step_prefix_w_index = f"{step_prefix}{step_index}"
        # flags step
        flag_step_get_exception = False

        # 2.1=DETECT STRUCTURE --------------------------------------------------------------------
        if callable(item):
            # if exact func_link element in sequence!
            question = None
            func_link = item
            expected_answer = True
            skip = False
            use_answer = True
            always1_run = False
            always2_stop_if_step_false = False
            always2_stop_if_was_false = False

            func_link_if_correct = FUNC_LINK_LAMBDA_TRUE
            func_link_if_wrong = FUNC_LINK_LAMBDA_TRUE
            func_link_if_exception = FUNC_LINK_LAMBDA_TRUE
            func_link_with_result = FUNC_LINK_LAMBDA_TRUE

        elif isinstance(item, dict):
            # 1=question --------------------
            question = dict_value_get_with_default_and_replacing(item, "question", "", [None])

            # 2=func_link -------------------
            func_link = dict_value_get_with_default_and_replacing(item, "func_link", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link):
                raise Exception(f"incorrect input type func_link=[{func_link}] =need CALLABLE!")

            # 3=answer ----------------------
            expected_answer = item.get("expected_answer", True)

            # 3=flags -----------------------
            skip = bool(item.get("skip", False))
            use_answer = bool(item.get("use_answer", True))
            always1_run = bool(item.get("always1_run", False))
            always2_stop_if_step_false = bool(item.get("always2_stop_if_step_false", False))
            always2_stop_if_was_false = bool(item.get("always2_stop_if_was_false", False))

            # 4=func_link_if_* -------------
            func_link_if_correct = dict_value_get_with_default_and_replacing(item, "func_link_if_correct", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link_if_correct):
                raise Exception(f"incorrect input type func_link_if_correct=[{func_link_if_correct}] =need CALLABLE!")

            func_link_if_wrong = dict_value_get_with_default_and_replacing(item, "func_link_if_wrong", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link_if_wrong):
                raise Exception(f"incorrect input type func_link_if_wrong=[{func_link_if_wrong}] =need CALLABLE!")

            func_link_if_exception = dict_value_get_with_default_and_replacing(item, "func_link_if_exception", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link_if_exception):
                raise Exception(f"incorrect input type func_link_if_exception=[{func_link_if_exception}] =need CALLABLE!")

            func_link_with_result = dict_value_get_with_default_and_replacing(item, "func_link_with_result", FUNC_LINK_LAMBDA_TRUE, [None])
            if not callable(func_link_with_result):
                raise Exception(f"incorrect input type func_link_with_result=[{func_link_with_result}] =need CALLABLE!")

        else:
            raise Exception(f"incorrect input type item=[{item}] =need SEQUENCE of CALLABLE!")

        if func_link_if_exception == FUNC_LINK_LAMBDA_TRUE:
            func_link_if_exception = func_link_if_wrong

        func_name = func_link.__name__
        logging_and_print_debug(f"[{step_prefix_w_index}][{func_name}] found func in sequence! {'-'*30}")

        # 2.2=STEP=DECIDE TO RUN --------------------------------------------------------------------
        # msg
        msg_step_prefix = f"[{step_prefix_w_index}][{func_name}] question=[{question}]?"

        # level2
        if always2_stop_if_was_false and flag_sequence_was_false:
            msg = msg_step_prefix + " --> MISSED OUT! by trigger always2_stop_if_WAS_FALSE"
            logging_and_print_warning(msg)
            continue
        elif flag_sequence_always2_stop_if_step_false:
            msg = msg_step_prefix + " --> MISSED OUT! by trigger always2_stop_if_STEP_FALSE"
            logging_and_print_warning(msg)
            continue

        # level1+0
        elif flag_run_all or always1_run or not flag_sequence_was_false:
            pass

        else:
            msg = msg_step_prefix + " --> MISSED out!"
            logging_and_print_warning(msg)
            continue

        if skip:
            msg = msg_step_prefix + " --> SKIPPED out!"
            logging_and_print_warning(msg)
            continue

        # 2.3=STEP=EXECUTE --------------------------------------------------------------------
        # get_answer = func_link()
        try:
            get_answer = func_link()
            logging_and_print_debug(
                f"[{step_prefix_w_index}][{func_name}] expected_answer=[{expected_answer}] get_answer=[{get_answer}]")
        except Exception as exx:
            flag_step_get_exception = True
            get_answer = "***EXCEPTION***"
            logging_and_print_warning(f"[{step_prefix_w_index}][{func_name}] expected_answer=[{expected_answer}] get_answer=[{get_answer}]")
            logging_and_print_warning(f"[{type(exx)}][{exx}]")

        # 2.4=STEP=RESOLVE --------------------------------------------------------------------
        result = get_answer == expected_answer
        if result:
            msg = msg_step_prefix + " --> CORRECT!"
            logging_and_print_info(msg)
        else:
            if use_answer:
                flag_sequence_was_false = True

                msg = msg_step_prefix + " --> FAIL critical"
                logging_and_print_error(msg)
            else:
                msg = msg_step_prefix + " --> FAIL warning"
                logging_and_print_warning(msg)

            if always2_stop_if_step_false:
                flag_sequence_always2_stop_if_step_false = True
                logging_and_print_warning(
                    f"[{step_prefix_w_index}][{func_name}] TRIGGER always2_stop_if_step_false=[{always2_stop_if_step_false}] --> STOP SEQUENCE!")

        # 2.5=STEP=FUNC_IF_*
        if result:
            func_link_if_correct()
            func_link_with_result(result)
        elif flag_step_get_exception:
            func_link_if_exception()
        else:
            func_link_if_wrong()
            func_link_with_result(result)

    # FINAL RESULT
    result_final = not flag_sequence_was_false
    if func_link_with_final_result:
        if not callable(func_link_with_final_result):
            msg = f"is not CALLABLE {func_link_with_final_result=}"
            raise Exception(msg)
        else:
            func_link_with_final_result(result_final)

    return result_final


def func_wait_true(
        func_link=FUNC_LINK_LAMBDA_TRUE,
        kwargs={},
        timeout=30,
        msg_question="Ждем положительного ответа",
        msg_result_true="True",
        msg_result_false="False",
):  # STARICHENKO
    """wait True from func - work only for short funcs!!! which return answer in short period!

    :param func_link: used func_link
    :param kwargs: kwargs dict for func
    :param timeout: total time for waiting - used only for
    :param sleep_remain: max time to sleep for steps if step time is less
    """
    progress_bar = LogProgressBarTimeout(max_value=timeout, title_prefix=f"{msg_question}")

    while not progress_bar.check_finish():
        result = func_link(**kwargs)
        if result:
            progress_bar.update(title=f" --> [{msg_result_true}]")
            break
        else:
            progress_bar.update(title=f" --> [{msg_result_false}]")
            time.sleep(1)

    progress_bar.update_status(result)
    return result


# TYPES ==============================================================================================================
pass


# todo: rebuild into TYPES!!!!
def type_check_by_variants(source, types_seq=None):  # starichenko
    """show if source object have one of exact type
    useful if you not setisfied buildin isinstance! - want to raise and want to print

    :param types_seq: one-type or any iterable sequence of types except str!
    """
    # todo: deprecate! star
    # 1=types_seq
    if isinstance(types_seq, type):
        types_tuple = (types_seq, )
    elif type_is_iterable_but_not_str(types_seq):
        types_tuple = tuple(types_seq)
    else:
        msg = f"Incorrect input type types_seq=[{types_seq}] need sequence or type!!!"
        raise Exception(msg)

    # 2=MAIN
    if not isinstance(source, types_tuple):
        obj_name = obj_get_name(source)
        msg = f"Incorrect input type obj_name=[{obj_name}] value=[{source}] need types_tuple={types_tuple}!!!"
        logging_and_print_warning(msg)
        return False
    else:
        return True


def type_is_1_module_link(source):  # starichenko
    return isinstance(source, type(sys))


def type_is_2_class_link_or_instance(source):  # starichenko
    return hasattr(source, "__mro__")


def type_is_2_class_link(source):  # starichenko
    return type_is_2_class_link_or_instance(source) and callable(source)


def type_is_2_class_instance(source):  # starichenko
    return type_is_2_class_link_or_instance(source) and not callable(source)


def type_is_3_function_link(source):  # starichenko
    return callable(source) and not type_is_2_class_link_or_instance(source)


def type_is_4_attribute(source):  # starichenko
    return not callable(source) and not type_is_1_module_link(source) and not type_is_2_class_link_or_instance(source)


def type_is_intable(source, float_before=False):   # starichenko
    """
    :param float_before: use float() before int()
    """
    try:
        if float_before:
            # source = str_try_to_float(source)
            float(source)
        else:
            int(source)
        return True
    except:
        return False


def type_is_floatable(source):   # starichenko
    try:
        float(source)
        return True
    except:
        return False


def type_is_iterable(source, dict_as_iterable=True, str_and_bytes_as_iterable=True):  # starichenko
    """checks if source is iterable.

    :param source: source data
    :param dict_as_iterable: if you dont want to use dict in your selecting,
        becouse maybe you need flatten all elements in list/set/tuple into one sequence
        and dict (as extended list) will be irrelevant!
    :param str_as_iterable: usually in data processing you need to work with str-type elements as OneSolid element
        but not iterating through chars!
    """
    if isinstance(source, dict):
        return dict_as_iterable
    elif isinstance(source, (str, bytes)):
        return str_and_bytes_as_iterable
    elif isinstance(source, (tuple, list, set, )):    # need to get it explicitly!!!
        return True
    elif hasattr(source, '__iter__') or hasattr(source, '__getitem__'):
        return True
    else:
        return False


def type_is_iterable_but_not_str(source):   # starichenko
    """checks if source is iterable, but not exactly str!!!"""
    return type_is_iterable(source, str_and_bytes_as_iterable=False)


def type_is_iterable_but_not_dict(source):   # starichenko
    """checks if source is iterable, but not exactly dict!!!"""
    return type_is_iterable(source, str_and_bytes_as_iterable=False)


def type_is_iterable_but_not_dict_or_str(source):   # starichenko
    """checks if source is iterable, but not exactly dict or str!!!"""
    return type_is_iterable(source, str_and_bytes_as_iterable=False, dict_as_iterable=False)


def type_is_instance_of_any_user_class(source):   # starichenko
    """check source for instance of any user class
    """
    if hasattr(source, "__module__") and hasattr(source, "__dict__") and hasattr(source, "__weakref__"):
        return True


# VALUES ==============================================================================================================
def value_is_blanked(
        source,
        spaces_as_blank=True,
        zero_as_blank=True,
        false_as_blank=False,
        addition_equivalent_list=[]):   # starichenko
    # 1=step spaces_as_blank
    if spaces_as_blank and isinstance(source, str):
        source = source.strip()

    if false_as_blank and source is False:
        return True

    if zero_as_blank and (source is not False) and str_try_to_float(source) == 0:
        return True

    # 2=step addition_equivalent_list
    blank_list = [None, "", (), [], {}, tuple(), list(), set(), dict(), b"", r"", *addition_equivalent_list]

    # 3=step result
    if source in blank_list:
        return True
    else:
        return False


def value_raise_if_blank(*sources, msg=None, dont_raise=False):     # starichenko
    """ raise if VALUE is blanked"""
    if msg is None:
        msg = f"RAISE FOR BLANK data in source=[{sources}]"

    for item in sources:
        if value_is_blanked(item):
            if dont_raise:
                return False
            else:
                raise Exception(msg)
    return True


def value_convert_to_bool(value):
    if isinstance(value, str):
        value = ''.join(value.lower().split())
        new_value = value.replace(';', ',').replace(',', '.').replace('..', '.')
        while value != new_value:
            value = new_value
            new_value = value.replace(';', ',').replace(',', '.').replace('..', '.')
        if 'false' in value or 'no' in value:
            return False
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            pass
    return bool(value)


def value_check_by_pattern(source, pattern, types_seq=[str, int, float]):     # starichenko
    """
    created for snmp oid
    """
    if not type_check_by_variants(source=source, types_seq=types_seq):
        return

    source = str(source)
    return bool(re.fullmatch(pattern=pattern, string=source))


def value_make_sequence_if_not_sequence(source, return_empty_list_if_blanked=True):    # starichenko
    """
    useful if you want to be sure it is finally sequence
    when your func can get string value or list of str - like params

    example:
        None    -> []
        ""      -> []
        []      -> []
        1       -> [1, ]
        "1"     -> ["1", ]
        {1:1}   -> {1:1, }
    """
    if return_empty_list_if_blanked and value_is_blanked(source, zero_as_blank=False):
        result = []
    elif type_is_iterable_but_not_str(source):
        result = source
    else:
        result = [source, ]

    return result


def value_search_by_list(source=None, search_list=[], search_type_1starts_2full_3ends_4any_5fullmatch=2):  # starichenko
    """check if source match by type search variants in list

    :param search_type_1starts_2full_3ends_4any_5fullmatch:
        be carefull to use 4 state!!! "CU" can be found before "CU1" - place less covered values on top!
    """
    match_item = None

    if search_type_1starts_2full_3ends_4any_5fullmatch == 1:
        for search_item in search_list:
            try:
                result = source.startswith(search_item)
            except:
                result = source == search_item

            if result:
                match_item = search_item
                break

    elif search_type_1starts_2full_3ends_4any_5fullmatch == 2:
        if source in search_list:
            match_item = source

    elif search_type_1starts_2full_3ends_4any_5fullmatch == 3:
        for search_item in search_list:
            try:
                result = source.endswith(search_item)
            except:
                result = source == search_item

            if result:
                match_item = search_item
                break

    elif search_type_1starts_2full_3ends_4any_5fullmatch == 4:
        for search_item in search_list:
            try:
                result = search_item in source
            except:
                result = source == search_item

            if result:
                match_item = search_item
                break

    elif search_type_1starts_2full_3ends_4any_5fullmatch == 5:
        for search_item in search_list:
            try:
                result = re.fullmatch(pattern=search_item, string=source)
            except:
                result = source == search_item

            if result:
                match_item = search_item
                break

    return match_item


def value_search_by_dict_return_key_and_value(
        source, search_dict,
        search_type_1starts_2full_3ends_4any_5fullmatch,
        _nested_key_pattern=r"\{\{.*\}\}"):  # starichenko
    """find comparison from source value by 1Level dict, and any nested!

    :param source: can be any type value if 2fullComparison, in other types only STR!!!
    :param search_dict: keys can be tuples or not sequenced key
    :param search_type_1starts_2full_3ends_4any_5fullmatch: method of comparing with keys in search_dict
    :param _nested_key_pattern: if you want to use nested dict - use this special pattern for special Blocks
    :return: tuple(match_key, match_value)

    example: useful if you need to get value for "CU" from
        search_dict = {
            "CU0": 0,
            "CU1": 1,
            ("CUACTIVE", "CU"): 1,
            "CUPASSIVE": None,
            ("CHASSIS", "CH", "-", "FU", "PS1", "PS2"): 0,
            "{{NESTED_BLOCK}}": {
                "ADR0": 0,
                "ADR1": 1,
            }
        }
    """
    match_key = None
    match_value = None

    if not type_check_by_variants(search_dict, dict):
        return match_key, match_value

    for key_tuple, value in search_dict.items():
        if isinstance(key_tuple, str) and re.fullmatch(pattern=_nested_key_pattern, string=key_tuple):
            match_key, match_value = value_search_by_dict_return_key_and_value(
                source=source,
                search_dict=value,
                search_type_1starts_2full_3ends_4any_5fullmatch=search_type_1starts_2full_3ends_4any_5fullmatch,
                _nested_key_pattern=_nested_key_pattern)
            if match_key or match_value:
                break

        key_tuple = value_make_sequence_if_not_sequence(source=key_tuple, return_empty_list_if_blanked=False)
        if len(key_tuple) == 0:
            key_tuple = (key_tuple, )
        match_key = value_search_by_list(
            source=source, search_list=key_tuple,
            search_type_1starts_2full_3ends_4any_5fullmatch=search_type_1starts_2full_3ends_4any_5fullmatch)
        # print(key_tuple, match_key, source)
        if match_key is not None and match_key in key_tuple:  # !!!its important!!! not just only IF MATCH_KEY!!!
            match_value = value
            break

    return match_key, match_value


def value_try_replace_by_dict(source, search_dict, search_type_1starts_2full_3ends_4any_5fullmatch=2, return_source_if_not=True):  # starichenko
    """ try to find and replace value by special dict.
    It is mostly (you can see) the same as value_search_by_dict_return_key_and_value
    BUT instead tuple at this time it returns final value or source!

    :param search_dict: have special structure! see value_search_by_dict_return_key_and_value!
    :param return_source_if_not: if False return None!

    example:
        func(100, {(1, 10, 100): 1000}) --> 1000
    """
    match_key, match_value = value_search_by_dict_return_key_and_value(source=source, search_dict=search_dict, search_type_1starts_2full_3ends_4any_5fullmatch=search_type_1starts_2full_3ends_4any_5fullmatch)
    if (match_key == match_value == None) and return_source_if_not:
        result = source
    else:
        result = match_value
    return result


# PARAMS ==============================================================================================================
def params_check_dependencies_return_wrong_list(source, func_link_read_param_or_dict, _root_level=True):  # starichenko
    wrong_list = []

    # INPUT
    if not source:
        return wrong_list

    if isinstance(func_link_read_param_or_dict, dict):
        _dict = func_link_read_param_or_dict
        func_link_read_param_or_dict = lambda p: _dict.get(p)
    elif not func_link_read_param_or_dict or not callable(func_link_read_param_or_dict):
        msg = f"[{func_link_read_param_or_dict=}] need callable!"
        logging_and_print_warning(msg)
        return

    # WORK
    for _name, _value in source.items():
        if not _value:
            continue

        value_read = func_link_read_param_or_dict(_name)

        if isinstance(_value, (list, tuple)):
            value_list = _value
        elif isinstance(_value, (str,)):
            value_list = [_value, ]
        elif isinstance(_value, (int, float)):
            value_list = [_value, ]
            value_read = str_try_to_float(value_read)
        elif isinstance(_value, (dict,)):
            value_list = list(_value)

        if value_read not in value_list:
            wrong_list.append(_name)
            msg = f"{_name=}[{value_read=}]not in {value_list=}"
            logging_and_print_warning(msg)
            continue

        elif isinstance(_value, (dict,)):
            wrong_list.extend(params_check_dependencies_return_wrong_list(source=_value[value_read], func_link_read_param_or_dict=func_link_read_param_or_dict, _root_level=False))

    # FINISH
    if wrong_list and _root_level:
        msg = f"{wrong_list=}"
        logging_and_print_warning(msg)

    return wrong_list


def params_check_deviation_or_equel__str_or_float(
        source: tp.Sequence[tp.Union[str, int, float]],
        deviation: tp.Union[str, int, float] = 0,
        round_float: int = 6,
) -> bool:  # starichenko
    """ compare values that may be generic int/float or string values!
    if any value cant be floated - all values will be compared as strings (deviation wont consider).
    otherwise deviation will be used!

    IMPORTANT:
        1. you need to prepare/strip values if its have aged spaces!!!
        here we assumed that we get this values from enough smart system not to toss such unexpected values!

    specially created for VolgaConnection comparing values after writing params!!!
    """
    # INPUT --------------------------------------------------------------------------------------
    source = set(source)
    if not source:
        msg = f"empty input {source=}"
        logging_and_print_warning(msg)
        return False

    try:
        deviation = float(deviation)
    except:
        msg = f"incorrect input {deviation=}"
        logging_and_print_warning(msg)
        deviation = 0

    # DECIDE DIGITS ------------------------------------------------------------------------------
    source_floated = set()
    try:
        for item in source:
            source_floated.add(float(item))
    except:
        source_floated.clear()

    # COMPARE DIGITS ------------------------------------------------------------------------------
    if source_floated:
        source_deviation = round(max(source_floated) - min(source_floated), round_float)
        result = source_deviation <= deviation
    else:
        result = len(source) == 1
    return result


# STR PROCESSING =====================================================================================================
# str-SPLIT ----------------------------------------------------------------------------------------------------------
def str_get_alphanum_list(source, use_float=False, float_signs=".", strip_spaces=False, return_text=False):
    """ Turn a string into a list of string and int/float-number chunks.
        use_float=False
            "z12z1.0" -> ["z", 12, "z", 1, ".", 0]
        use_float=True
            "z12z1.0" -> ["z", 12, "z", 1]
    """
    source = str(source)
    if use_float:
        pattern = f'([0-9]+(?:[{float_signs}][0-9]+)?)'
    else:
        pattern = f'([0-9]+)'

    result_temp = re.split(pattern, source)

    result = []
    for item in result_temp:
        if strip_spaces:
            item = item.strip()

        if not return_text:
            item = str_try_to_float(item)

        if item != "":
            result.append(item)

    return result


def str_split_smart(
        source="",
        sep=" ",
        exact_count_parts=None,
        maxsplit=-1,
        min_parts_input=0,
        min_parts_output=0,
        def_value=None,
        strip_spaces=True,
        replase_values_to_def=["", " "]):   # starichenko
    """created to make splitting with exact minimal length!
    :param sep: same as in built-in split
    :param maxsplit: same as in built-in split

    :param exact_count_parts: if specified func returns exact parts no matter specified or not maxsplit/min_parts
    :param min_parts_input: if actual parts count is less - will raise!
    :param min_parts_output: min splited parts for func output! all disadvantages fills by def_value

    :param def_value: if real output parts less then min_parts result will be appended by this value
    :param strip_spaces: strip SPACEs in splitted parts
    :param replase_values_to_def: replace all specified values to default
    """

    type_check_by_variants(source, str)

    if exact_count_parts is not None:
        maxsplit = exact_count_parts - 1
        min_parts_output = exact_count_parts

    result = source.split(sep, maxsplit)
    if len(result) < min_parts_input:
        msg = f"input parts is less then minimal needed!"
        raise Exception(msg)

    while len(result) < min_parts_output:
        result.append(def_value)

    if strip_spaces:
        result = [item.strip() if isinstance(item, str) else item for item in result]

    if replase_values_to_def:
        result = [def_value if item in replase_values_to_def else item for item in result]

    print(result)
    return result


# str-TYPE -----------------------------------------------------------------------------------------------------------
def str_try_to_int(source, none_if_exception=False):
    """ Try to convert string to int and return it, otherwise returns string.
    """
    if isinstance(source, str):
        source_temp = source.strip()
    else:
        source_temp = source

    try:
        return int(float(source_temp))  # need float before int!!!
    except:
        if none_if_exception:
            return None
        else:
            return source


def str_try_to_float(source, none_if_exception=False, round_float=None):
    """ Try to convert string to float and return it, otherwise returns string.
    If value is even intable - return int!
    """
    result = source
    if isinstance(source, str):
        source_temp = source.strip().replace(",", ".")
    else:
        source_temp = source

    try:
        result_float = float(source_temp)
        result_int = int(result_float)
        if result_float == result_int:
            result = result_int
        else:
            result = result_float
            if round_float:
                result = round(result, round_float)
    except:
        if none_if_exception:
            result = None

    return result


def str_get_number_near_measure_unit_or_none(source, measure_unit_list=None):  # starichenko
    """returns number if passed in string with measured unit!
    space characters allowed in any expected separate places!

    :param measure_unit_list: measured units expected - if not specified will used common expected!

    Example:
        " 12  "      -> int(12)
        " 12 В "      -> int(12)
        " 12.54 В "   -> float(12.54)
        " 12 В hey"  -> "12 В hey"   # not expected 3d element in whole string
        " 12 K "      -> "12 K"       # K-sign is not expected!
    """
    # INPUT
    if measure_unit_list is None:
        measure_unit_list = ["В", "Вт", "A", ]

    # TRIVIAL
    if isinstance(source, (int, float,)):
        return source
    elif not isinstance(source, str):
        return

    # WORK
    pattern = f'\s*([0-9]+(?:[.,][0-9]+)?)\s*({"|".join(measure_unit_list)})?\s*'
    match = re.fullmatch(pattern, source)
    if match:
        match_str = match[1]
        result = str_try_to_float(match_str)
    else:
        result = None

    return result


# str
def str_get_chars_range(start, finish, add_russian_yo=True, return_list=True):     # starichenko
    result = ""
    for i in range(ord(start), ord(finish)):
        char_i = chr(i)
        result += char_i
        if add_russian_yo:
            if char_i == "е":
                result += 'ё'  # находится после я!!! а не после Е!!!
            elif char_i == "Е":
                result += 'Ё'

    if return_list:
        return list(result)
    else:
        return result


# str-REPLACE --------------------------------------------------------------------------------------------------------
def str_replace_elements_by_dict(source, replace_dict={}, debug_print=False):
    """ Replaces symbols in 'string' with corresponding values from replace_dict
    """
    result = source
    for old, new in replace_dict.items():
        if not new:
            new = ""
        result = result.replace(str(old), str(new))

    if debug_print:
        print(f"source=[{source}]")
        print(f"result=[{result}]")
    return result


def str_replace_russian_letters(string):
    """ Replaces cyrillic letters in 'string' with latin ones
    """
    russian_to_english_translate = {
        'а': 'a',   'А': 'A',
        'в': 'b',   'В': 'B',
        'с': 'c',   'С': 'C',
        'д': 'd',   'Д': 'D',
        'е': 'e',   'Е': 'E',
        'ё': 'e',   'Ё': 'E',
        'о': 'o',   'О': 'O',
        'р': 'p',   'Р': 'P',
        'к': 'k',   'К': 'K',
        'х': 'x',   'Х': 'X',
        'и': 'u',   'И': 'U',
        'у': 'y',   'У': 'Y',
        'т': 't',   'Т': 'T',
        'м': 'm',   'М': 'M',
        'Н': 'H'}
    return str_replace_elements_by_dict(string, russian_to_english_translate)

def str_replace_all_substr_by_exact(string, replace_symbols_list=[], symbol_replacing_to=""):
    """ Returns shorted string by replacing all symbols with one one.
    """
    if not symbol_replacing_to:
        symbol_replacing_to = ""
    if not isinstance(string, str) or not string:
        return None

    for substr in replace_symbols_list:
        string = string.replace(substr, symbol_replacing_to)

    while len(string) != len(string.replace(symbol_replacing_to * 2, symbol_replacing_to)):
        string = string.replace(symbol_replacing_to * 2, symbol_replacing_to)

    return string


def str_replace_all_non_filesystem_name_chars(source, new_char="__"):    # starichenko
    """
    get string for filesystem working

    :param source:
    :param new_char:
    :return:
    """
    result = ""
    for char_i in source:
        if char_i in LIST_FILESYSTEM_WRONG_NAME_CHARS:
            result += new_char
        else:
            result += char_i
    return result


# str-FIND -----------------------------------------------------------------------------------------------------------
def str_pattern_get_groups_count(pattern):    # starichenko
    """ return count of grouping groups in pattern!
    if group have a quantification like "()?" - it will be counted as logically exected!

    tests:
        pattern = r'1(2)3(9)?'
        num_groups(pattern)     # 2

        pattern = r'(1(2)3(9)?)'
        num_groups(pattern)     # 3

        pattern = r'(?:1(2)3(9)?)'
        num_groups(pattern)     # 2
    """
    type_check_by_variants(pattern, str)

    result = re.compile(pattern).groups
    print(result)
    return result


# str=IP -------------------------------------------------------------------------------------------------------------
def str_host_get_ip(host):  # starichenko
    """
    return ip from ip or hostName!
    if error = return None! - it can be in case of DNS is not available
    """
    try:
        return socket.gethostbyname(host)
    except:
        return


def str_ip_host_validate(host):     # starihenko
    """Проверка на валидность IPv4 адреса or hostname
    :param host: IP адрес в текстовом виде
    :return: результат
    :rtype: bool
    """
    if not type_check_by_variants(host, [str, ]):
        return

    try:
        ip = str_host_get_ip(host)
        ipaddress.ip_address(ip)
        return True
    except:
        return


# str=CONVERSION -----------------------------------------------------------------------------------------------------
def str_convert_uptime_to_int_seconds(uptime_str, debug_print=True):    # starichenko
    """convert cu_uptime in any known patterns into integer seconds
     known is like "01:00:41:24"
     """
    type_check_by_variants(uptime_str, str)

    uptime_str = uptime_str.strip()
    uptime_int = None
    device_detected = None

    PATTERN_DICT = {    # pattern(must have 4groups!!!): comment(device+example)
        r"()()()(\d+)": "UPTIME just usual seconds ['123456']",
        r"(\d{2}):(\d{2}):(\d{2}):(\d{2})": "UPTIME VOLGA-style ['01:00:41:24']",
        r"(\d*)d:(\d*)h:(\d*)m:(\d*)s": "UPTIME just variant ['01d:00h:41m:24s']",
        r"(\d+)\sdays,\s:(\d{2})h:(\d{2})m:(\d{2})s": "UPTIME MOXA-nport5150-style ['0 days, 00h:10m:08s']",
    }

    match = None
    for pattern, comment in PATTERN_DICT.items():
        match = re.fullmatch(pattern, uptime_str, re.IGNORECASE)
        if match:
            device_detected = comment
            break

    if match:
        part_d = 0 if not match[1] else int(match[1])
        part_h = 0 if not match[2] else int(match[2])
        part_m = 0 if not match[3] else int(match[3])
        part_s = 0 if not match[4] else int(match[4])

        uptime_int = part_s + part_m * 60 + part_h * 60*60 + part_d * 60*60*24

    if debug_print:
        print(f"uptime_str={uptime_str}")
        print(f"uptime_int={uptime_int}")
        print(f"device_detected={device_detected}")

    return uptime_int


# RANGE PROCESSING ===================================================================================================
def range_check_covering_number(number=0.0, range_seq=[0.0, 1.0]):       # STARICHENKO
    return range_seq[0] <= number <= range_seq[1]


@decorator_try__return_none_and_log_explanation
def range_get_direction_sign(start, finish):                     # STARICHENKO
    # print(f"start=[{start}] finish=[{finish}]")
    return -1 if (finish - start) < 0 else 1


def range_get_direction_bool(start, finish):                     # STARICHENKO
    return True if range_get_direction_sign(start, finish) == 1 else False


def range_float_smart(first, last, step_module=1):                # STARICHENKO
    """ Аналог RANGE для FLOAT значений!

        1. правильно округляет!
        2. включает краевые значения!
        3. идет всегда в направлении от старта к стопу!
        4. шаг - берется модуль от указанного! знак не учитывается, т.к. берется из направления
        5. если значения равны - одно значение выдается!

        for i in range_float_smart(1, 0, 0.1):
            print(i)
        #-> [1, 0.9, 0.8 --- 0.0]
    """
    step_module = abs(step_module)

    step_module_splited = str(step_module).split(".")
    if len(step_module_splited) != 2:
        round_depth = 1
    else:
        round_depth = len(step_module_splited[1])

    direction = -1 if (last - first) < 0 else +1
    value_step = first
    while first * direction <= value_step * direction <= last * direction:
        yield value_step
        value_step = round(value_step + step_module * direction, round_depth)


# NUMBER 1=DEVIATION =================================================================================================
def number_deviation_check(normal, deviation, number):                     # STARICHENKO
    logging_and_print_debug(f"number_deviation_check: normal=[{normal}], deviation=[{deviation}], number=[{number}]")

    try:
        number = float(number)
        normal = float(normal)
        deviation = float(deviation)
    except:
        logging_and_print_warning(f"получены неверные типы данных для входных параметров")

    if abs(normal - number) <= deviation:
        return True
    else:
        return False


def number_deviation_check_list(normal, deviation, number_list=[], stop_at_fist_wrong=False, silent=False):     # STARICHENKO
    try:
        number_list = [float(number) for number in number_list]
        normal = float(normal)
        deviation = float(deviation)
    except:
        logging_and_print_warning(f"получены неверные типы данных для входных параметров")

    if number_list == []:
        logging_and_print_warning(f"получены пустые данные для number_list={number_list}")
        return

    pos = 0
    wrong_pos_list = []
    for number in number_list:
        pos += 1
        if abs(normal - number) > deviation:

            if stop_at_fist_wrong:
                msg = f"обнаружено значение [{number=}] [{pos=}] превышающее допустимое отклонение=[{deviation}]"
                logging_and_print_warning(msg)
                return False
            else:
                wrong_pos_list.append(pos)

    if wrong_pos_list and not silent:
        msg = f"{wrong_pos_list=}"
        logging_and_print_warning(msg)

    return len(wrong_pos_list) == 0


def number_deviation_get_max(normal=1.0, number_list=[1.1, 1.2]):                     # STARICHENKO
    """выдать значение из предложенных, с наибольшим отклдонением от нормы,
    из найденных вариантов выдает только одно значение (первое обнаруженное)
    работает только с int/float
    """
    try:
        normal = float(normal)
        number_list = [float(value) for value in number_list]
    except:
        logging_and_print_warning(f"получены неверные типы данных для входных параметров")

    if number_list == []:
        logging_and_print_warning(f"получены пустые данные для number_list={number_list}")
        return

    max_deviating_value = normal
    max_deviation = 0

    for value in number_list:
        deviation = abs(normal - value)
        if deviation > max_deviation:
            max_deviating_value = value
            max_deviation = deviation

    return max_deviating_value


# NUMBER 2= =======================================================================================================
def number_cutting(source, cutting_level=None):     # starichenko
    """
    cutting_level
        number_cutting(321.123, None) --> 321.123
        number_cutting(321.123, 0) --> 321.123

        number_cutting(321.123, 1) --> 320
        number_cutting(321.123, -1) --> 321.1

    created because usually it works wrong in expected python
        print(321.123//0.001)   # 321122.0
        print(321.123*1000//1)   # 321123.0
    """
    result = source
    if cutting_level:
        if cutting_level > 0:
            result = (result // (10 ** cutting_level)) * (10 ** cutting_level)
        if cutting_level < 0:
            result = (result * (10 ** (-cutting_level-1))//1) / (10 ** (-cutting_level-1))
    return result


def number_convert_to_list_by_baselist(source, number, zero_is_first=True):  # starichenko
    """DONT MESS WITH STANDART ENUMERATE SYSTEMS!!!!
    besouse it have some differenses!!!!
        func([0, 1], 2) ---> [0, 0, ]
        2 ---> b00000010

    Example:
        func([0, 1], 0) ---> [0, ]
        func([0, 1], 1) ---> [1, ]

        func([0, 1], 2) ---> [0, 0, ]
        func([0, 1], 3) ---> [1, 0, ]

        func([0, 1], 4) ---> [0, 1, ]
        func([0, 1], 5) ---> [1, 1, ]

        func([0, 1], 6) ---> [0, 0, 0, ]

    useful for excel column name creation from index

    :params first_index: only variants
    """
    result = []
    len_list = len(source)

    if not zero_is_first:
        number -= 1

    if number < 0:
        return result

    while True:
        if number < len_list:
            result.append(source[number % len_list])
            break
        else:
            result.append(source[number % len_list])
            number = number//len_list -1

    return result


# NUMBER 3=BIN =======================================================================================================
def number_get_bit_in_position(source, position):    # starichenko
    """return exact bit from number
    :param position: position begin [1:]
    """
    index = position - 1
    result = (source & (1 << index)) >> index
    # print(result, bin(result))
    return result


# SEQUENCE COMMON ====================================================================================================
def sequence_make_ensured_if_not(source):  # starichenko
    """make sequence if not from source

    useful if you want to make ensured sequence from not known source
    """
    if not type_is_iterable_but_not_str(source):
        source = [source, ]
    return source


def sequence_make_from_ints(
        first=None, last=None,
        use_all=True, final_seq=None,
        min=1, max=None):   # starichenko
    """return int_sequence from variants.

    Typical usage is for port listing for NetworkDevices.

    :param use_all: use all diapason from MIN to MAX!
        use_all is more important then final_seq
    :param final_seq: used if you want give final result and maybe want to correct it by Min/max edges!

    :param min: commonly used for specifying first value 0/1
        MIN/MAX can be used for priority limiting ranges - all outer values will be excluded
    :param max: usually equals maximum available port number
    """

    # todo: maybe need to deprecate!!! starichenko
    first = int(first) if isinstance(first, str) else first
    last = int(last) if isinstance(last, str) else last
    min = int(min) if isinstance(min, str) else min
    max = int(max) if isinstance(max, str) else max

    result = []
    if first is None:
        first = min

    if use_all:
        first = min
        last = max
        result = range_float_smart(first, last, step_module=1)

    elif final_seq is None:
        if last is None:
            last = first
        result = range_float_smart(first, last, step_module=1)
    else:
        result = final_seq

    if min is not None: result = [i for i in result if i >= min]
    if max is not None: result = [i for i in result if i <= max]

    return result


def sequence_delete_items(source, items_seq):            # STARICHENKO
    """delete all specified items from any sequence!
    """
    type_check_by_variants(source, (list, set, dict,))
    type_check_by_variants(items_seq, (list, set, tuple, dict, ))

    for i in items_seq:
        while True:
            try:
                source.remove(i)
            except:
                break
    return source


def sequence_delete_items_blank(source):                        # STARICHENKO
    return sequence_delete_items(source, items_seq=[None, "", [], (), {}, dict()])


def sequence_check_included_in_supersequence(sub_seq, super_seq):           # STARICHENKO
    """check if sub sequence fully is in super sequence
    work with all seq type - list/set/tuple/dict"""

    type_check_by_variants(sub_seq, (list, set, tuple, dict,))
    type_check_by_variants(super_seq, (list, set, tuple, dict,))

    return set(sub_seq).issubset(super_seq)


def sequences_get_longest_length(*seqs):
    """ return len of longest sequence"""
    return len(sequences_get_longest(*seqs))


def sequences_get_longest(*seqs):
    """ get longest sequence from inputed"""
    return max(*seqs, key=len)


def sequences_flatten(*seqs, miss_value_list=[]):     # starichenko
    """flatten all nested elements in all sequences
    if need actually dict flatten - use func dict_flatten!
    if dict or another extended data (base_types) - will used as original!

    :param miss_value_list: miss element if found in sequence
        you can miss any object even exact dict!
    """
    result = []

    for item in seqs:
        if item in miss_value_list:
            continue
        if type_is_iterable_but_not_dict_or_str(item):
            result_add = sequences_flatten(*item)
        else:
            result_add = [item, ]

        result += result_add
    return result


def sequence_join_to_string(
        *seqs,
        sep="",
        miss_value_list=[],
        replace_elements_dict={},
        nested=True,
        miss_noneelementary_types=False,
        raise_if_nonelementary=True):     # starichenko
    """create string by joining all nested printable elements.
    Created becouse common join not working with nonString elements like INT!!! - raise error!

    :param replace_elements_dict: use it to replace values like None/True/False or others!

    """
    result_str = ""

    type_check_by_variants(sep, (str,))

    if nested:
        seq_list = sequences_flatten(*seqs, miss_value_list=miss_value_list)
    else:
        seq_list = list(*seqs)

    for item in seq_list:
        # if nonElementary
        if not type_is_elementary_single(item):
            if miss_noneelementary_types:
                continue
            if raise_if_nonelementary:
                raise Exception(f"item type is not ElementarySingle!!! item=[{item}]")

        # if need to replace
        if item in replace_elements_dict:
            item = replace_elements_dict[item]

        if not result_str:
            result_str = str(item)
        else:
            result_str += sep + str(item)

    return result_str


def sequence_join_to_string_simple(source, sep="", skip_blank=True, revert_order=False, strip_space=False, strip_sep=False):   # starichenko
    """jioing all elements from sequence to string
    works with any types that have STR

    if already exists sep in sequeace - dont add!
    """
    if isinstance(source, str):
        return source

    result = ""

    if revert_order:
        source = copy.copy(source)[::-1]

    for item in source:
        # preapare item
        if item:
            if strip_space:
                item = f"{item}".strip()
            if sep and strip_sep:
                item = f"{item}".strip(sep)

        # decide use item
        if skip_blank and not item:
            continue

        # result
        if not result or result.endswith(sep):
            result += f"{item}"
        else:
            result += f"{sep}{item}"

    return result


def sequence_check_values_by_pattern(source, pattern, value_types_seq=[str, int, float]):     # starichenko
    """
    created for snmp oid

    """
    if type_check_by_variants(source, [str, int, float, ]):
        source = [source, ]

    if not type_is_iterable_but_not_dict(source):
        return

    for item in source:
        if not value_check_by_pattern(source=item, pattern=pattern, types_seq=value_types_seq):
            return

    return True


def sequences_get_different_elements(seq1, seq2):
    if not type_is_iterable_but_not_str(seq1) or not type_is_iterable_but_not_str(seq2):
        msg = f"incorrect input types {seq1=}/{seq2=}"
        logging_and_print_warning(msg)
        return

    diff_set = set(seq1).symmetric_difference(set(seq2))
    msg = f"find difference {diff_set=}"
    logging_and_print_debug(msg)
    return diff_set


# 1=LISTS ------------------------------------------------------------------------------------------------------------
def list_pretty_string(source, new_line_spacer=" "*4):     # starichenko
    if type_is_iterable_but_not_str(source):
        result = "["
        for line in source:
            result += f"\n{new_line_spacer}{line},"
        result += "\n]"
        print(result)
        return result


def list_tuples_del_index(tuples_list, index, delete_tuple_if_index_value=STR_NOT_INPUTED_MARK):      # starichenko
    """
    created special for pytest argvalues shorting lengs

    :param tuples_list: list of tuples for typest parametrisation
    :param index: index for deleting item in tuples
    :param delete_tuple_if_index_value: if item in tuple will be equel to it whole tuple will be deleted
    """
    result = []
    if not type_is_iterable_but_not_dict_or_str(tuples_list):
        msg = f"inconvenient type of tuples_list=[{tuples_list}]"
        raise Exception(msg)

    for item in tuples_list:
        if type_check_by_variants(item, (list, tuple, )):
            item = list(item)
            if len(item) >= index+1:
                if item[index] == delete_tuple_if_index_value:
                    continue
                del item[index]
            item = tuple(item)

        result.append(item)
    return result


def lists_sum(source_lists=[[], [], ], no_repetitions=False):             # Starichenko
    result_list = []
    for list_i in source_lists:
        list_i = sequence_make_ensured_if_not(list_i)
        for value in list_i:
            if value in result_list and no_repetitions:
                pass
            else:
                result_list.append(value)

    return result_list


def list_del_edged_blank(source, del_start=True, del_finish=True):   # starichenko
    """ delete all edged blank items!"""
    type_check_by_variants(source, [list, tuple])
    source = list(source)
    len_start = len(source)

    if del_start and value_is_blanked(source[0]):
        source.pop(0)
    if del_finish and value_is_blanked(source[-1]):
        source.pop(-1)

    if len(source) != len_start:
        source = list_del_edged_blank(source)

    return source


def list_sort_simple_floatable_items(source, use_float=True, separate_floatable_and_nums=False):  # starichenko
    """
    INT+FLOAT+STR
        typical usage for strings contains int numbers!
        all numbers found will be accepted as one symbol in string for sorting like priority level

    FLOAT!!!sort only as floats!

    EXAMPLES
        [1,10,2] --> [1,2,10]
        ["3",2,10,"2"]separate_nums=True --> [2,10,"2","3"]
        ["3",2,10,"2"]separate_nums=False --> [2,"2","3",10]

        ["3",2,"2T2",10,"2T1"]separate_nums=False --> [2,"2T1","2T2","3",10]
    """
    result_list = []
    num_list = []
    str_floatable_list = []
    str_list = []

    if use_float:
        func_float_int_link = float
    else:
        func_float_int_link = int

    for item in source:
        if isinstance(item, (int, float)):
            num_list.append(item)
        else:
            try:
                func_float_int_link(item)
                str_floatable_list.append(item)
            except:
                str_list.append(item)

    sorted_num = []
    sorted_str_floatable = []
    sorted_str = sorted(str_list)

    if separate_floatable_and_nums:
        sorted_num = sorted(num_list)
        sorted_str_floatable = sorted(str_floatable_list, key=func_float_int_link)
    else:
        sorted_num = sorted([*num_list, *str_floatable_list], key=func_float_int_link)

    result_list.extend([*sorted_num, *sorted_str_floatable, *sorted_str])
    return result_list


def list_sort_with_correct_inner_numbs(source, use_float=False, on_error_return_source=False):
    """ Returns given list sorted in the way that humans expect (numerically).

    WARNING:
    works only with identical first char DIGIT/STRING in strings!
    THE ONLY CORRECT CONDITION - IT MUST START FROM SAME type (DIGIT/STRING)! othewise return None!
        ["s", "1"] -->     INcorrect
        ["s", "f"] -->     correct

        ["s1", "ffff"] --> correct
        ["s1", "ffff"] --> correct

    EXAMPLE
        ["s10", "s1"] --> ["s1", "s10"]
        ["192.168.1.111", "192.168.0.111"] --> ["192.168.0.111", "192.168.1.111"]

    """
    source_list = list(source)
    try:
        result = sorted(source_list, key=lambda i: str_get_alphanum_list(source=i, use_float=use_float))
    except Exception as exx:
        msg = f"{exx!r}\n"
        msg += f"ERROR - some elements starts from DIGIT and others from LITERAL sign"
        logging_and_print_warning(msg)
        if on_error_return_source:
            result = source
        else:
            result = None

    return result


def list_sort_by_patterns(source, pattern_priority=[], delete_nomatched=False, patterns_to_delete=[]):  # STARICHENKO
    """sort any sequence!




    maybe help is wrong!!!

    will not change type!!!  all int, float, str

    DICT - will return sorted dict!
    ANY STRINGABLE TYPE! - will sort as STR()

    :param source: any sequence except str, inconvenient nonsortable tupes will be converted to typical LIST.
        items can be str or int/float! no sequences!

    :param pattern_priority: used to specify priority sorting! all not matched items goes last!
        you can set low/up prioritн for IP-strings

    Example:
        [1, "2", "10", 100, "100", "e1", "e2", "e10", '192.168.1.9', '192.168.1.123']

        created specially for sorting slot_names in VolgaDeviceDict
        ["-", "1", "2", 3, "4:CU0", "4:CU1", "FU", 'PS1', 'PS2']
    """
    # todo: FINISH!!!
    # raise Exception("NOT FINISHED")

    # type_check_by_variants(source, (tuple, list, set, dict, ))

    if type_check_by_variants(source, (tuple, list, set, dict,)):
        source_list = list(source)
    else:
        msg = f"ERROR [{source=}] need LIST!"
        logging_and_print_warning(msg)
        return

    result_list = []
    remain_for_groups_list = source_list

    if not pattern_priority:
        pattern_priority = [".*"]

    for pattern in pattern_priority:
        result_group_list = []

        # find match
        for item_orig in remain_for_groups_list:
            if re.fullmatch(string=str(item_orig), pattern=pattern):
                result_group_list.append(item_orig)

        # clear remain
        if result_group_list:
            result_group_list = list_sort_with_correct_inner_numbs(source=result_group_list, use_float=False, on_error_return_source=True)

            sequence_delete_items(source=remain_for_groups_list, items_seq=result_group_list)
            result_list.extend(result_group_list)

    if remain_for_groups_list:
        remain_for_groups_list = list_sort_with_correct_inner_numbs(source=remain_for_groups_list, use_float=False, on_error_return_source=True)
        result_list.extend(remain_for_groups_list)
    return result_list


def lists_compare_with_priority_by_numbers(list1, list2, return_index_not_list=True, first_index_is_major=True):   # starichenko
    """ compare and return largest list.
    if lens is not equal - will add missing numbers usually to the end.
    Typically used to compare product vertions

    :param list1: source list1, can be list of int/float or floatable/intable str
    :param list2: source list2
        dont work with not Floatable/intable strings!!!
            [1][1,"2rc3"] - gives error!!! but only if element comes to exact comparring!
            [2][1,"2rc3"] - return correct index=1!
    :param return_index_not_list:
    :param first_index_is_major: shows priority order for comparing elements in lists
    :return:
        if return_index_not_list
            0 if equal
            1 if list1 is bigger
            2 if list2 is bigger
        else return exact the bigger list in source variant!

    example:
        [1,1][1,0,5] -> [1,1] -> 1
        [1][1,0,5] -> [1,0,5] -> 2
        [1][1,0,0] -> equal -> 0
        [1][1,0,"0"] -> equal -> 0
        [1][1,0,"3rc4"] -> ERROR
        [2][1,0,"3rc4"] -> [2] -> 1
    """

    # todo: see special compare vertions!
    type_check_by_variants(list1, (list,))
    type_check_by_variants(list2, (list,))

    if first_index_is_major:
        list1_temp = copy.copy(list1)
        list2_temp = copy.copy(list2)
    else:
        # reverce order
        list1_temp = copy.copy(list1)[::-1]
        list2_temp = copy.copy(list2)[::-1]

    list1_temp, list2_temp = lists_make_equal_length(list1_temp, list2_temp, expand_value=0, expand_to_the_end=True)

    result_index = 0
    for el_list1, el_list2 in zip(list1_temp, list2_temp):
        el_list1 = float(el_list1)
        el_list2 = float(el_list2)

        if el_list1 == el_list2:
            continue
        elif el_list1 > el_list2:
            result_index = 1
            break
        else:
            result_index = 2
            break

    if return_index_not_list:
        result = result_index
    elif result_index in [0, 1]:
        result = list1
    else:
        result = list2

    return result


def sets_get_symmetric_difference_shrinked_by_patterns(source1: list, source2: list, patterns_fullmatch: tp.Union[str, tp.Iterable, dict]) -> set:   #starichenko
    source1_shrinked = list_shrink_by_patterns(source=source1, patterns_fullmatch=patterns_fullmatch, delete_copies=True)
    source2_shrinked = list_shrink_by_patterns(source=source2, patterns_fullmatch=patterns_fullmatch, delete_copies=True)

    difference: set = set(source1_shrinked).symmetric_difference(set(source2_shrinked))
    return difference


def list_shrink_by_patterns(source: list, patterns_fullmatch: tp.Union[str, tp.Iterable, dict], delete_copies: bool = True):   #starichenko
    """
    replace items so we can simply compare it
    vary need several patterns! one is not enough!

    gives you ability to compare lists (like parameters in Volga) for different crates.
    For example if you have ethalon set of params for 13slots crate and you need to compare it with any other slotCount crate
    """
    # INPUT -------------------------------------
    if isinstance(patterns_fullmatch, str):
        patterns_fullmatch = [patterns_fullmatch, ]
    if isinstance(patterns_fullmatch, (set, list, tuple)):
        patterns_fullmatch = dict(zip(patterns_fullmatch, patterns_fullmatch))
    if not isinstance(patterns_fullmatch, dict):
        msg = f"incorrect input {patterns_fullmatch=}"
        logging_and_print_warning(msg)
        return

    # WORK -------------------------------------
    result = []
    for item in source:
        pattern_found = None
        if delete_copies and item in result:
            continue
        for pattern, pattern_replace in patterns_fullmatch.items():
            if re.fullmatch(pattern, item):
                pattern_found = True
                item = pattern_replace
                if delete_copies and item in result:
                    break
                result.append(item)
                break
        if not pattern_found:
            result.append(item)

    return result


def lists_make_equal_length(*seqs, expand_value=None, expand_to_the_end=True):
    """make list with equal lens

    :param seqs:
    ;param expand_value: value to fill missing elements
    :param expand_to_the_end: place missing values to the end or start positions in list
    :return: tuple of result modified source lists

    example:
        [],[1,True] -. [None, None],[1, True]
    """
    max_length = sequences_get_longest_length(*seqs)

    result = []

    for sequence in seqs:
        type_check_by_variants(sequence, (list,))

        seq_expanded = list_expand_for_length(sequence, max_length, expand_value=expand_value,
                                              expand_to_the_end=expand_to_the_end)
        result.append(seq_expanded)

    return result


def list_expand_for_length(source, expected_len, expand_value=None, expand_to_the_end=True):
    """ expand list if it less then expected_len

    example:
        for 1 [1, 2] -> [1, 2]
        for 3 [1, 2] -> [1, 2, None]
    """
    type_check_by_variants(source, (list,))

    result = copy.copy(source)
    for _ in range(expected_len - len(source)):
        if expand_to_the_end:
            result.append(expand_value)
        else:
            result = [expand_value, ] + result
    return result


def list_add_items_if_have_not(source, items):    # starichenko
    """add elements in list if they are not exists in source

    usefull to merge two lists!
    """
    result = copy.copy(source)

    type_check_by_variants(source, [list, ])

    items = sequence_make_ensured_if_not(items)

    for i in items:
        if i not in source:
            result.append(i)
    return result


def list_get_item_by_circle_index(source, index):  # starichenko
    """

    Example:
        func([0, 1, 2], 0) ---> 0
        func([0, 1, 2], 3) ---> 0

    """
    return index % len(source)


def list_delete_strings_by_substring(source, substring, percent=None):    # starichenko
    """
    cteated spesially for delete elements in log_msg_list by "[DEBUG  ]"

    :param source:
    :param substring:
    :return:
    """
    result = copy.deepcopy(source)
    _counter = 0

    len_source = len(source)
    if percent is None:
        percent = 100
    percent_index = round(len_source * percent/100)-1

    part = source[percent_index::-1]
    for index, msg in enumerate(part):
        if substring in msg:
            _counter += 1
            del result[percent_index - index]
    return result


def list_replace_element(source, old, new, replace_all=True):    # starichenko
    """
    delete all elements from list

    cteated spesially for replace elements in log_msg_list by msg_old
    """
    result = copy.deepcopy(source)
    item_found_index = -1

    while True:
        try:
            item_found_index = source.index(old, item_found_index + 1)
        except:
            break
        result[item_found_index] = new
        if not replace_all:
            break
    return result


def list_get_repeated_elements(source):
    diff_set = set()
    if not type_is_iterable_but_not_str(source):
        msg = f"incorrect input {source=}"
        logging_and_print_warning(msg)
        return

    source_set = set(source)
    diff_count = len(source) - len(source_set)
    if diff_count:
        source_remain = copy.deepcopy(source)
        for element in source_set:
            source_remain.remove(element)
        diff_set = set(source_remain)
        msg = f"detected repeated elements {diff_count=}/{diff_set=}"
        logging_and_print_warning(msg)
    return diff_set


def list_split_by_groups(source, elements_in_group=2, max_groups=None):  # starichenko
    """
    yield source elements by groups.

    EXAMPLE:
        [1,2,3,4,5], 1 --> [[1],[2],[3],[4],[5]]
        [1,2,3,4,5], 2 --> [[1,2],[3,4],[5]]
        [1,2,3,4,5], 3 --> [[1,2,3],[4,5]]

    :param elements_in_group:
    :return:
    """
    if not source:
        return []

    if not elements_in_group:
        return source

    result = []

    index = 0
    index_group = 1
    index_inside = 0
    group = []
    for element in source:
        index += 1
        index_inside += 1

        if max_groups and max_groups < index_group:
            break

        group.append(element)

        if index_inside == elements_in_group:
            result.append(group)
            group = []
            index_group += 1
            index_inside = 0

    if group:
        result.append(group)
    return result


# ====================================================================================================================
def range_to_tuple_of_lists(range_string, dont_sort=False):
    """Создание кортежа списков с разобранными диапазонами.

    :param range_string: Диапазоны значений.
    :type range_string: str | list[str|int]

    :param dont_sort: Сортировать ли выходные данные. По умолчанию False - сортированные уникальные значения из
      переданных диапазонов. При True - последовательность значений и значений из диапазонов не сортируются и не
      уникальные - так можно задавать повторы (смотри пример).
    :type dont_sort: bool

    Примеры.

    На выходе получим `([], )`, если :param range_string: передан пустым, например, `None` | `""`.

    На выходе получим результат `([33, 35, 36, 37, 39, 40], )`, если range_string соответствует форматам:
      * " 33,  35-37, 40—39   ";
      * ["33", "35-37", "40—39"];
      * [37, 33, 36, 35, 39, 40].

    На выходе получим результат `([33, 35, 36, 37, 39, 40], [41, 42, 43, 44, 45], )`, если range_string содержит
    один из разделителей групп диапазонов (/, \\\\) и соответствует форматам:
      * " 33,  35-37 , 40—39/41, 42, 45-41  ";
      * " 33,  35-37 , 40—39\\\\41, 42, 45-41  ".

    На выходе получим строку `(["Обработка лишних пробелов строки"], )`, если range_string пришел строкой:
      * "\\ Обработка \\ лишних \\ \\ \\ пробелов строки\\ ".

    Важно! Пример БЕЗ СОРТИРОВКИ РЕЗУЛЬТАТА!
    На выходе получим `([35, 36, 37, 33, 40, 39], [41, 42, 45, 44, 43, 42, 41], )`, если
    range_string="35-37 , 33,  40—39/41, 42, 45-41  ", dont_sort=True.
    """
    temp_list = []
    if not range_string:
        return tuple([temp_list])

    if isinstance(range_string, str):
        # Чистка входной строки от мусора.
        range_string = re.sub(r'\s+', ' ', range_string.strip())
        range_string = range_string.replace(";", ",").replace("...", "-").replace("..", "-")
        if re.findall(r'\d+', range_string):
            # Если в строке есть хоть одна цифра, то удаляем все пробелы из строки
            range_string = ''.join(range_string.split())
    if isinstance(range_string, list):
        temp = ""
        for each in range_string:
            temp += str(each) + ","
        range_string = temp[:-1]
        del temp
    range_string = range_string.replace(";", ",").replace("...", "-").replace("..", "-")
    range_string = str_replace_all_substr_by_exact(range_string, replace_symbols_list=['\\'], symbol_replacing_to='/')
    pattern = r'(\d+)(?:[-–—]+)(\d+)'  # Соответствует '21-60'
    pattern_float = r'(\d+\.\d)(?:[-–—]+)(\d+\.\d)'  # Соответствует '21.5-60.5'
    pattern_with_e = r'(\d+e)(?:[-–—]+)(\d+e)'  # Соответствует '21e-60e'

    for each_range in range_string.split("/"):
        interim_list = []
        for each_num in each_range.split(','):
            current_match = re.match(pattern, each_num)
            current_match_float = re.match(pattern_float, each_num)
            current_match_with_e = re.match(pattern_with_e, each_num)

            if current_match:
                val1 = int(current_match.group(1))
                val2 = int(current_match.group(2))
                if val1 <= val2 or dont_sort is True:
                    increment = 1 if val1 <= val2 else -1
                    for each_number in range(val1, val2 + increment, increment):
                        interim_list.append(int(each_number))
                else:
                    for each_number in range(val2, val1 + 1):
                        interim_list.append(int(each_number))
            elif current_match_float:
                val1 = int(float(current_match_float.group(1)) * 10)
                val2 = int(float(current_match_float.group(2)) * 10)
                if val1 <= val2:
                    for each_number in range(val1, val2 + 1, 10):
                        interim_list.append(each_number / 10)
                else:
                    for each_number in range(val2 * 10, val1 * 10 + 1, 10):
                        interim_list.append(each_number / 10)
            elif current_match_with_e:
                # Половинчатые каналы, которые в Атласе отображаются 'Ch21e'. Тут разбираем '21e'.
                # Наличие 'e' характерно пока только для мультиплексоров:
                val1 = int(current_match_with_e.group(1).split('e')[0])
                val2 = int(current_match_with_e.group(2).split('e')[0])
                for each_number in range(min(val1, val2), max(val1, val2) + 1, 1):
                    interim_list.append("{}e".format(each_number))
            elif len(each_num) > 0:
                if '.' in each_num:
                    try:
                        interim_list.append(float(each_num))
                    except:
                        interim_list.append(each_num)
                else:
                    try:
                        interim_list.append(int(each_num))
                    except:
                        interim_list.append(each_num)
        if len(interim_list) > 0:
            if dont_sort is True:
                temp_list.append(interim_list)
            else:
                temp_list.append(sorted(list(set(interim_list))))

    return tuple(temp_list)


def cartesian2(arrays):
    """Строит все возможные комбинации из элементов двух списков.

    Источник: https://askdev.ru/q/ispolzovanie-numpy-dlya-postroeniya-massiva-iz-vseh-kombinaciy-dvuh-massivov-23880/

    Пример: ([1, 2], [3, 4]) => [[1, 3], [1, 4], [2, 3], [2, 4]]
    >>> cartesian2(arrays=([1, 2], [3, 4]))
    [[1, 3], [1, 4], [2, 3], [2, 4]]
    """
    arrays = [np.asarray(a) for a in arrays]
    shape = (len(x) for x in arrays)

    ix = np.indices(shape, dtype=int)
    ix = ix.reshape(len(arrays), -1).T

    for n, arr in enumerate(arrays):
        ix[:, n] = arrays[n][ix[:, n]]
    return np.array(ix).tolist()


def cartesian3(range_param):
    """Строит все возможные комбинации из элементов двух списков.

    Строка воспринимается как целое и ставится в начале списка.
    Выделяем строковый список, если есть.

    Пример:
        IN: ([1], [1, 2], ['1GE', 'STM1', 'STM4'])
        OUT: [[1, 1], [1, 2], ['1GE', 'STM1', 'STM4']]

    >>> cartesian3(([1], [1, 2], ['1GE', 'STM1', 'STM4']))
    [['1GE', 'STM1', 'STM4'], [1, 1], [1, 2]]
    """

    str_param = False
    range_param_new = []
    range_param_list = list(range_param)
    for item_list in range_param_list:
        if isinstance(item_list, list):
            for item in item_list:
                if isinstance(item, str):
                    str_param = item_list
                    range_param_list.remove(item_list)
                    break
                else:
                    str_param = False
        else:
            str_param = range_param
    try:
        range_param = tuple(range_param_list)
        if len(range_param) > 1:
            range_param_new = cartesian2(range_param)
        else:
            range_param_new = range_param_list
    except:
        logging.error("Не удалось преобразовать кортеж{}".format(range_param))
    if str_param:
        range_param_new.insert(0, str_param)
    return range_param_new


def cartesian4(range_param):
    """Строит все возможные комбинации из элементов двух списков.

    Строка воспринимается как целое и ставится в начале списка. Выделяем строковый список, если есть.

    Пример:
        IN: ([1], [1, 2], ['1GE', 'STM1', 'STM4'])
        OUT: [[1, 1,'1GE'], [1, 2, '1GE'],[1, 1,'STM1'], [1, 2,'STM1'],[1, 1,'STM4'], [1, 2,'STM4']

    >>> cartesian4(([1], [1, 2], ['1GE', 'STM1', 'STM4']))
    [[1, 1, '1GE'], [1, 2, '1GE'], [1, 1, 'STM1'], [1, 2, 'STM1'], [1, 1, 'STM4'], [1, 2, 'STM4']]
    """
    str_params = False
    range_param_new = []
    range_param_list = list(range_param)
    for item_list in range_param_list:
        if isinstance(item_list, list):
            for item in item_list:
                if isinstance(item, str):
                    str_params = item_list
                    range_param_list.remove(item_list)
                    break
                else:
                    str_params = False
        else:
            str_params = range_param

        # Преобразовываем числовой список,если нужно
    try:
        range_param = tuple(range_param_list)
        if len(range_param) > 1:
            range_param_new = cartesian2(range_param)
        else:
            range_param_new = range_param_list
    except:
        logging.error("Не удалось преобразовать кортеж{}".format(range_param))

    # Объединяем строковый и числовой списки,если нужно
    united_list = []
    if str_params:
        for str_param in str_params:
            for item in range_param_new:
                copyitem = copy.deepcopy(item)
                copyitem.append(str_param)
                united_list.append(copyitem)
        range_param_new = united_list
    return range_param_new


def collapse(channels):
    """ Takes tuple with channels lists and
        returns collapsed string of channels like this:
        ([21,22,23,25,26],[24,26,27,28,30]) ==> "21-23, 25, 26 / 24, 26-28, 30".
    """
    if channels == None:
        return channels

    return_string = ""
    for channels_list in channels:
        if channels_list[0:1]:
            temp_first_number = temp_last_number = int(channels_list.pop(0))
            while True:
                if channels_list[0:1]:
                    interim_sum = int(channels_list[0]) - temp_last_number
                else:
                    interim_sum = -1
                if interim_sum == 1:
                    temp_last_number = int(channels_list.pop(0))
                elif (interim_sum != 1) or (not channels_list[0:1]):
                    if temp_last_number == temp_first_number:
                        return_string += str(temp_first_number) + ', '
                    elif temp_last_number - temp_first_number == 1:
                        return_string += str(temp_first_number) + ', ' + str(temp_last_number) + ', '
                    else:
                        return_string += str(temp_first_number) + '-' + str(temp_last_number) + ', '
                    if channels_list[0:1]:
                        temp_first_number = temp_last_number = int(channels_list.pop(0))
                    else:
                        break

        if not return_string.endswith(' / , '):
            return_string = return_string[:-2] + ' / '
        else:
            return_string = return_string[:-2]
    return return_string[:-3]


def read_csv_and_return_matrix_of_values(csv_path):
    """ Reads csv-file and returns matrix of values
        (list of lists).
    """
    matrix_of_values = []
    file_path = os.path.realpath(csv_path)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for each_line in reader:
                if each_line != []:
                    matrix_of_values.append(each_line)

    return matrix_of_values


def ping(host, return_boolean=True):
    """ Ping-check for device availability,
        must work under windows, linux and macOSx
    """
    try:
        output = check_output('ping -n 1 -w 3000 {}'.format(host) if 'win' in system().lower()
                              else ['ping', '-c 1', '-w 3', host])
    except Exception as E:
        logging_and_print_debug("Error while ping {}: '{}' - '{}'".format(
            host, type(E), E))
        return False

    if return_boolean:
        return 'TTL' in str(output).upper()  # if 'TTL' in output -> ping was successful
    else:
        return output


def execution_statuses(statuses=None):
    """Статус сценария тестирования.

    :param statuses: Словарь статусов тестов. Ожидаемый формат:
    {"Тест 1": "OK", "Тест 2": "FAIL", "Тест 3": "SKIP"}.
    :type statuses: dict

    :returns: Возвращает строковое описание статуса выполнения тестового сценария. Возможны варианты:
    'Протестировано', 'В процессе', 'Ошибка', 'Не протестировано'.
    :rtype: str
    """
    non_tested = 'Не протестировано'
    if not statuses:
        return non_tested
    if not isinstance(statuses, dict):
        logging.warning(f"Неожиданный тип данных для расчета статуса сценария тестирования. "
                        f"Ожидается: dict. Получен: {type(statuses)}")
        return non_tested
    if statuses:
        if 'OK' in statuses.values() and 'FAIL' not in statuses.values() and 'SKIP' not in statuses.values() \
                and '' not in statuses.values():
            return 'Протестировано'
        elif 'OK' in statuses.values() and 'FAIL' not in statuses.values():
            return 'В процессе'
        elif 'FAIL' in statuses.values():
            return 'Ошибка'
        else:
            return non_tested


def dicts_merge_elemental(dicts_list):
    dicts_list_copy = dicts_list.copy()
    dict_item_copy = {}
    item_merge = []
    for dict_item in dicts_list_copy:
        for key_m, item_m in dict_item.items():
            for key_s, item_s in item_m.items():
                item_merge.append(item_s)
    dict_item_copy[key_m] = {key_s: item_merge}
    return dict_item_copy


def dicts_merge_family(parent, children_dict):
    """
    IN [{'no_detect_freeze': {'trials': {'trial:3; ': True}}}, {'trials': {'no_detect_freeze_2': [{'time:2; ': True},
    {'time:3; ': True}]}}]
    OUT {'no_detect_freeze': {'trials': {'trial:3; ': True, 'no_detect_freeze_2': [{'time:2; ': True},
    {'time:3; ': True}]}}}
    Или если parent и children_dict равны по старшинству - объединяем их.
    """
    parent_copy = copy.deepcopy(parent)
    children_copy = copy.deepcopy(children_dict)
    for key, val in parent_copy.items():
        for key_child, val_child in children_copy.items():
            if key == key_child:
                val.update(val_child)
            else:
                for val_c in val.values():
                    val_c.update(val_child)
    return parent_copy


def dicts_merge_hierarchy(h_dicts_list, h_keys):
    h_keys.reverse()
    # compress_dicts_list = compress_dict(h_dicts_list,h_keys, i=1)
    # return compress_dicts_list
    return compress_dict(h_dicts_list, h_keys, i=1)


def compress_dict(expanded_dicts_list, h_keys, i):
    """Объединение словарей.

    Объединяем список словарей, в один словарь, в соответствии с положением словарей в списке
    и иерархией внешнего списка ключей(от младшего к старшему, исключая самого младшего):
    1) Перебираем оба списка, если ключи совпали, записываем в список 'children'.
    2) Если ключи не совпали, записываем в список 'compress_dict_list' , если, при этом,
       видим список 'children', объединяем список 'children' с последним членом 'compress_dict_list'.
    3) Когда списки закончились, объединяем 'children' с последним членом 'compress_dict_list'.
    4) Если в последнем словаре из списка нет ключа из внешнего списка ключей, считаем его последним.
    """
    parent = False
    flag_end = False
    compress_dict_list = []
    children = []
    try:
        h_key = h_keys[i]
    except:
        h_key = False

    for dict_item in expanded_dicts_list:
        for key, item in dict_item.items():
            if key != h_key:
                if len(children) > 0:
                    children_dict = dicts_merge_elemental(children)
                    family_dict = dicts_merge_family(parent, children_dict)
                    compress_dict_list.append(family_dict)
                    compress_dict_list.remove(parent)
                    children.clear()
                compress_dict_list.append(dict_item)
                parent = dict_item
            else:
                if isinstance(item, dict):
                    for item_key in item.keys():
                        if item_key != 'step_status':
                            if item_key in h_keys:
                                children.append(dict_item)
                            else:
                                if len(children) > 0:
                                    children_dict = dicts_merge_elemental(children)
                                    family_dict = dicts_merge_family(parent, children_dict)
                                    compress_dict_list.append(family_dict)
                                    children.clear()
                                    parent = dict_item
                                else:
                                    parent = dict_item
                                    i = 1
                                    flag_end = True
    if len(children) > 0 and parent:
        children_dict = dicts_merge_elemental(children)
        family_dict = dicts_merge_family(parent, children_dict)
        compress_dict_list.append(family_dict)
        if not flag_end:
            compress_dict_list.remove(parent)

    if flag_end:
        compress_dicts = compress_dict_list
    else:
        compress_dicts = compress_dict(compress_dict_list, h_keys, i=i + 1)

    return compress_dicts


def index_hierarchy(func_list: list, count_master=1):
    """Индексирование списка.

    :param func_list: Список индексируемых уровней.
    :param count_master: Номер пункта, с которого следует начать нумерацию списка.

    Если член повторяется, последующие члены индексируются от него.

    Примеры (doctest):
    >>> index_hierarchy(func_list=['i1', 'i2', 'i3', 'i4', 'i4', 'i3', 'i4', 'i4', 'i4'], count_master=1)
    ['1', '1.1', '1.1.1', '1.1.1.1', '1.1.1.2', '1.1.2', '1.1.2.1', '1.1.2.2', '1.1.2.3']
    >>> "Далее не работающий пример"
    'Далее не работающий пример'
    >>> index_hierarchy(func_list=['i1', 'i1', 'i2', 'i3', 'i4', 'i4', 'i3', 'i4', 'i4', 'i4', \
    'i1', 'i1'], count_master=1) # doctest: +SKIP
    ['1', '2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '2.1.2.3', '3', '4']
    """
    count = 1
    indexes = []
    count_fix = ''
    func_prev = False
    flag_trans = False
    func_count_dict = {}
    priority_index_last = 100000  # для первого запуска
    for func in func_list:
        if func_prev:
            if func == func_prev:
                count += 1
                index = '{}.{}'.format(count_fix, count)
                indexes.append(str(index))
                flag_trans = True
            else:
                if func in func_count_dict.keys():
                    prior_index = priority_index(func_count_dict, func)
                    # Если приоритет(кол-во знаков) с индексом выше, переходим на этот индекс
                    if prior_index and int(prior_index) < int(priority_index_last):
                        flag_trans = True
                    priority_index_last = prior_index
                if flag_trans:
                    # Если есть флаг перехода, добавляем старший индекс и сбрасываем младший
                    count_master = count_string(func_count_dict[func])
                    count = 1
                    index = count_master
                    flag_trans = False
                else:
                    index = '{}.{}'.format(count_master, count)
                func_count_dict[func] = index
                indexes.append(str(index))
                count_fix = count_master
                count_master = index
        else:
            index = count_master
            indexes.append(str(index))
            # Заводим словарь функций-индексов
            func_count_dict[func] = index
        func_prev = func
    return indexes


def count_string(string):
    """Счетчик для строки '1.1...1.1'=>'1.1...1.2'

    Примеры:
    >>> count_string("1...5")
    '1...6'
    >>> count_string('1.1...1.5')
    '1.1...1.6'
    >>> count_string(1)
    '2'
    >>> count_string([1,2,3])
    False
    """
    index = False
    if isinstance(string, str):
        list_string = string.split('.')
        last_index = len(list_string) - 1
        list_string[last_index] = str(int(list_string[last_index]) + 1)
        prefix = list_string[0]
        for i in range(1, len(list_string)):
            count = list_string[i]
            index = '{}.{}'.format(prefix, count)
            prefix = index
    elif isinstance(string, int):
        index = str(string + 1)
    else:
        index = False
    return index


def priority_index(func_count_dict, func):
    """Приоритетный индекс.

    :param func_count_dict: Словарь.
    :type func_count_dict: dict

    :param func: Ключ словаря.
    :type func: str

    Примеры: '3' => 1; {"1": "1.10"} => [1,10] => 2
    >>> priority_index({"1": "1.10"}, "1")
    '2'
    """
    try:
        list_func_string = str(func_count_dict[func]).split('.')
        priority = len(list_func_string)
    except Exception as index_err:
        print(f'{index_err!r}')
        priority = '1'
    return str(priority)


def update_after_repeat(result_dict, result_repeat):
    """Обновляем сложно-структурированный словарь списком простых словарей."""
    excucute_update(result_dict, result_repeat)
    return result_dict


def excucute_update(result_dict, result_repeat):
    if isinstance(result_dict, list):
        for res_dict in result_dict:
            update_after_repeat(res_dict, result_repeat)
    elif isinstance(result_dict, dict):
        for func, value in result_dict.items():
            if isinstance(value, list):
                for item in value:
                    update_after_repeat({func: item}, result_repeat)
            elif isinstance(value, dict):
                for v_funcK, v_funcV in value.items():
                    for repeat_dict in result_repeat:
                        if isinstance(repeat_dict, dict):
                            for repeat_func, repeat_value in repeat_dict.items():
                                if isinstance(repeat_value, dict):
                                    for vr_func, vr_value in repeat_value.items():
                                        if v_funcK == 'step_status':
                                            value[v_funcK] = vr_value  # !!!!!
                                        elif v_funcK == vr_func and v_funcK != 'step_status':
                                            value.update(repeat_value)
                                        elif v_funcK == vr_func and isinstance(v_funcV, dict):
                                            if 'Error' in v_funcV.keys():
                                                value['step_status'] = False
                                            else:
                                                value['step_status'] = True
                                        elif v_funcK == repeat_func:
                                            update_after_repeat({v_funcK: v_funcV}, result_repeat)
                                        else:
                                            update_after_repeat(v_funcV, result_repeat)


# NEW NOT SORTED ======================================================================================================
def res_lists(measurement_data):
    """"Разбирает FILEPATH_RESULTS_LTR.

    Используется для построения виджета результатов, и протокола отчета.

    :returns: Список значений [indexes, descripts, ports, params, results, statuses]
    :rtype: list
    """
    indexes = []
    descripts = []
    sn = []
    ports = []
    params = []
    results = []
    statuses = []
    i = 1
    if measurement_data is not None:
        func_serv = ['engineer', 'date', 'pId', 'SrNumber', 'description', 'script']
        keys_dict_l = get_funcs_keys_all(measurement_data.results)
        for element in func_serv:
            try:
                keys_dict_l.remove([element])
            except ValueError:
                pass
        func_key_prev = False
        func_list_prev = []
        all_results = []

        for sc_names in measurement_data.results.values():
            # print('measured_dicts',measured_dicts)
            if isinstance(sc_names, list):
                for measured_dicts in sc_names:
                    if isinstance(measured_dicts, dict):
                        for func_keys in keys_dict_l:
                            # print('func_keys',func_keys)
                            if isinstance(func_keys, list):
                                for func_key in func_keys:
                                    if func_key in measured_dicts and func_key != 'Status_ОК':
                                        # and func_key != func_key_prev and func_key !="step_status":
                                        item_results_lists = recursive_results(
                                            func_key, func_keys, measured_dicts, descripts, sn, ports, params, results,
                                            statuses)
                                        func_key_prev = func_key
                                        # Далее запускаем индексацию
                                        results_copy = item_results_lists[0].copy()
                                        if func_list_prev:
                                            for f in func_list_prev:
                                                if f in results_copy:
                                                    results_copy.remove(f)
                                        func_list = results_copy
                                        func_list_prev = func_list
                                        if len(func_list) > 1:  # Для MD-D3
                                            for index in index_hierarchy(func_list, count_master=i):
                                                indexes.append(index)
                                        else:
                                            indexes.append(i)
                                        i = i + 1

    return [indexes, descripts, sn, ports, params, results, statuses]


def recursive_results(func_key, func_keys, measured_dicts, descripts, sn, ports, params, results, statuses):
    func_dict = {func_key: measured_dicts[func_key]}
    # func_dict = measured_dicts
    func_dict_table(func_keys, func_dict, descripts, sn, ports, params, results, statuses)
    return ports, params, results, statuses


def func_dict_table(func_keys, func_dict, descripts, sn, ports, params, results, statuses):
    if isinstance(func_dict, dict):
        func_slave = False
        for func, func_res_sn in func_dict.items():
            if isinstance(func_res_sn, dict):
                if func in func_keys:
                    ports.append(func)
                for key_f, func_res in func_res_sn.items():
                    if key_f == "descript_test":
                        descripts.append(func_res)
                    elif key_f in func_keys:
                        func_slave = func_res_sn
                    else:
                        if isinstance(func_res, dict):
                            if "." in key_f: sn.append(key_f)
                            for key, item in func_res.items():
                                if key == "step_status":
                                    statuses.append(item)
                                elif key not in func_keys:
                                    params.append(key)
                                    results.append(item)
            elif isinstance(func_res_sn, list):
                for func_r in func_res_sn:
                    func_dict_i = {func: func_r}
                    func_dict_table(func_keys, func_dict_i, descripts, sn, ports, params, results, statuses)
        if func_slave:
            func_dict_table(func_keys, func_slave, descripts, sn, ports, params, results, statuses)


def get_funcs_keys_all(parms):
    """Получаем список ключей из вложенных словарей "settings".

    :param parms: Словарь из "settings".
    :type parms: dict

    :return: Список ключей с названиями функций.
    """
    funcs_keys_all = []
    if isinstance(parms, dict):
        for f_key in list(parms.keys()):
            funcs_keys_all.append(get_func_keys_item({f_key: parms[f_key]}, []))
        return funcs_keys_all
    else:
        logging.error('Не верно заданы параметры settings')
        return False


def get_func_keys_item(parms, func_keys_item: list):
    """Рекурсивный разбор словаря функций.

    :param parms: Словарь функций сценария.

    :param func_keys_item: Пополняемый список функций сценария.

    Используется для шаблонизации функций. Функцией при разборе settings считается словарь, в котором есть ключ
    "params".
    """
    if isinstance(parms, dict):
        for func_name, func_params in parms.items():
            if func_name != "params":  # and func_name != "descript_test"  :
                func_keys_item.append(func_name)
                if isinstance(func_params, dict):
                    for func_name_slave in func_params.keys():
                        if func_name_slave != "params":  # and func_name_slave != "descript_test" :
                            func_params_slave = func_params[func_name_slave]
                            get_func_keys_item({func_name_slave: func_params_slave}, func_keys_item)
    return func_keys_item


def clean_dict(data: dict):
    """Чистит словарь с сохранением корневых ключей и заменой значений на пустышки.

    :param data: Словарь, который следует очистить.
    :type data: dict

    :rtype: dict

    Значения корневых ключей словаря перезаписываются пустыми структурами того же типа, что и в пришедших данных.
    Если пришел не словарь, то возвращается пустышка.

    Пример (doctest):
    >>> clean_dict(data={'int_': 15, 'float_': 1.5, 'bool_': True, 'none_': None, 'dict_': {'q1': 1, 'q2': [5, 6]}, \
    'list_': [1, 2, 3, 'asd'], 'str_': 'Строка'})
    {'int_': None, 'float_': None, 'bool_': False, 'none_': None, 'dict_': {}, 'list_': [], 'str_': ''}
    """
    if not isinstance(data, dict):
        return {}
    if len(data) > 0:
        json_data_types = {type(i): i for i in [[], {}, "", False]}
        for k, v in data.items():
            data.update({k: json_data_types.get(type(v), None)})
    return data


# TESTS ==============================================================================================================
def _test__socket():
    import socket
    import time

    address = ('192.168.21.223', 4001)
    obj = socket.socket()
    obj.settimeout(1)

    # print(obj.getpeername())    # OSError: [WinError 10057] Запрос на отправку или получение данных  (when sending on a datagram socket using a sendto call) no address was supplied

    try:
        result = obj.connect(address)
    except:
        result = None
    print(result)


    print(obj.getpeername())  # ('192.168.21.2', 4001)

    # 1=DISCONNECTED
    print(
        obj)  # <socket.socket fd=312, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 4998), raddr=('192.168.21.2', 4001)>
    print(obj.getsockname())  # ('0.0.0.0', 5259)

    # 2=CONNECTED
    print(
        obj)  # <socket.socket fd=368, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.127.111', 5004), raddr=('192.168.21.223', 4001)>
    obj_show_attr_all(obj, nested=True)

    exit()
    for i in range(100):
        print()
        print(obj.getsockname())  # ('192.168.127.111', 5238)
        # print(obj.__dir__())  # ('192.168.127.111', 5238)
        print(bool(obj))

        obj_show_attr_all(obj, nested=True)
        time.sleep(1)


def _test__zero():
    source = " 12,3  Вт "
    rep_dict = {
        "l": 5,
        "o": 1000
    }

    value_raise_if_blank(1, [])

    seq_list = ([None], [1, 2], True)
    # print(sequence_join_to_string(seq_list, replace_elements_dict={None: 0}))

    obj_show_attr_all(int)

    # print(list(dict_iter_combinations_by_key_list_and_value_list()))


def _test__sound():
    # sound_ask()
    sound_error()


# ====================================================================================================================
if __name__ == '__main__':  # starichenko
    msg = f"if you want to direct run some func here - GO TO FILE _example_direct_access_to_4__MISC.py"
    logging_and_print_warning(msg)


# ====================================================================================================================
