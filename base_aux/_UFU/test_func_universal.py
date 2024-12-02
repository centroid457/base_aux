import pathlib

import pytest
import time
import threading

import os
import copy

import utilities.func_other
import utilities.func_universal as UFU
from utilities.processor_file_excel import _ExcelProcessor


# Пример измерения как сценария:
scenario_dictionary_template = {
    "ConstructionCheckMeasurement": {
        "settings": {
            "description": "Проверка конструкции",
            "script": "by_funcs",
            "manual_check": {
                "descript_test": "Визуальная проверка конструкции",
                "params": {
                    "marking": "(ПМ1.2.1)"
                },
                "set_resettable_params": {
                    "descript_test": "Установка параметров, без проверки",
                    "params": {
                        "SetDefaultSettings": "Сброс всех параметров",
                        "wait_s": "5"
                    },
                    "set_switching_params": {
                        "descript_test": "Установка параметров, с проверкой",
                        "params": {
                            "range": "1-3",
                            "Dev.Port.State.Time.Set": "20"
                        }
                    }
                }
            },
            "set_switching_params_range": {
                "descript_test": "Установка параметров в диапазоне, с проверкой",
                "params": {
                    "range": "1,2/3-5/7-8",  # "range": "4,5",
                    "Ch{}Out{}.Port.State": "OOS"  # "Ch{}Out.Port.State": "OOS"
                },
                "set_switching_params": {
                    "descript_test": "Установка параметров[sub], с проверкой",
                    "params": {
                        "range": "sub",
                        "Dev{}.Port{}.State{}.Time.Set": "25"  # "Dev.Port.State.Time.Set": "25"
                    }
                }
            }
        }}}


def test_range_to_tuple_of_lists_for_range_in_as_string():
    """range_to_tuple_of_lists(range_string='21-60')"""
    result = UFU.range_to_tuple_of_lists(range_string='21-60')
    expect = tuple([list(range(21, 61, 1))])
    assert result == expect


def test_range_to_tuple_of_lists_for_range_in_as_float():
    """range_to_tuple_of_lists(range_string='21.5-60.5')"""
    result = UFU.range_to_tuple_of_lists(range_string='21.5-60.5')
    expect = tuple([list(i + 0.5 for i in range(21, 61, 1))])
    assert result == expect


def test_range_to_tuple_of_lists_for_range_in_as_string_with_e_channel():
    """range_to_tuple_of_lists(range_string='21e-60e')
    """
    result = UFU.range_to_tuple_of_lists(range_string='21e-60e')
    tmp_l = []
    list_channels_as_str = ["{}e".format(i) for i in range(21, 60 + 1, 1)]
    tmp_l.append(list_channels_as_str)
    expect = tuple(tmp_l)
    assert result == expect


@pytest.mark.parametrize(
    "range_string,dont_sort,expected",
    [
        ("", False, ([],)),
        ("33, 35-37, 40—39", False, ([33, 35, 36, 37, 39, 40],)),
        (["33", "35-37", "40—39"], False, ([33, 35, 36, 37, 39, 40],)),
        ([37, 33, 36, 35, 39, 40], False, ([33, 35, 36, 37, 39, 40],)),
        (" 33,  35-37 , 40—39/41, 42, 45-41  ", False, ([33, 35, 36, 37, 39, 40], [41, 42, 43, 44, 45],)),
        (" 33,  35-37 , 40—39\\41, 42, 45-41  ", False, ([33, 35, 36, 37, 39, 40], [41, 42, 43, 44, 45],)),
        ("Сброс всех параметров", False, (["Сброс всех параметров"],)),
        (" Обработка  лишних    пробелов строки ", False, (["Обработка лишних пробелов строки"],)),

        # Ответ должен быть не сортированным
        ("35-37 , 33,  40—39/41, 42, 45-41  ", True, ([35, 36, 37, 33, 40, 39], [41, 42, 45, 44, 43, 42, 41]))
    ]
)
def test_range_to_tuple_of_lists_for_range_with_exclusion_of_string_spaces(range_string, dont_sort, expected):
    result = UFU.range_to_tuple_of_lists(range_string=range_string, dont_sort=dont_sort)
    assert result == expected


@pytest.mark.parametrize(
    "arrays,expected",
    [
        ([[1, 2], [3, 4]], [[1, 3], [1, 4], [2, 3], [2, 4]])
    ]
)
def test_cartesian2(arrays, expected):
    result = UFU.cartesian2(arrays)
    assert result == expected


@pytest.mark.parametrize(
    "channel_string,expected",
    [
        ('21', 21), (21, 21), (' 21 ', 21),
        ("CH 21 In --> Line Out", 21), ("Line IN --> CH 21 OUT", 21),
        ("CH 21e In --> Line Out", '21e'),
        ("CH 21", 21), ("CH 21 ", 21)
    ]
)
def test_return_channel_number(channel_string, expected):
    result = UFU.return_channel_number(channel_string)
    assert result == expected


@pytest.mark.parametrize(
    "pid,expected",
    [
        ('OD-80-(21-60p)/h-01', 'OD-80-(21-60p)/h-01'),
        ('OD-80-(21-60p)/h', "OD-80-(21-60p)/h"),

        ('ОD-80-(21-60р)/h-01', 'OD-80-(21-60p)/h-01'),  # OD - первый символ русская О. p - русский символ
        ('ОD-80-(21-60р)/h', "OD-80-(21-60p)/h")  # OD - первый символ русская О. p - русский символ
    ]
)
def test_replace_russian_letters_in(pid, expected):
    result = UFU.str_replace_russian_letters(pid)
    assert result == expected


@pytest.mark.parametrize(
    "statuses,expected",
    [
        ({"T1": "OK"}, 'Протестировано'),
        ({"T1": "OK", "T2": "OK"}, 'Протестировано'),
        ({"T1": "OK", "T2": ""}, 'В процессе'), ({"T1": "OK", "T2": "SKIP"}, 'В процессе'),
        ({"T1": "OK", "T2": "FAIL"}, 'Ошибка'), ({"T1": "OK", "T2": "FAIL", "T3": "OK"}, 'Ошибка'),
        ({"T1": "non_tested_status 1", "T2": "non_tested_status 2"}, 'Не протестировано'),
        ("", "Не протестировано"), (None, "Не протестировано"), (["1", 1], "Не протестировано"),
        ("STRING 1", "Не протестировано"), (1000, "Не протестировано"), (("1", 1), "Не протестировано")
    ]
)
def test_execution_statuses(statuses, expected):
    assert UFU.execution_statuses(statuses) == expected


@pytest.mark.parametrize(
    "func_list,count_master,expected",
    [
        (
                ['i1', 'i2', 'i3', 'i4', 'i4', 'i3', 'i4', 'i4'], 1,
                ['1', '1.1', '1.1.1', '1.1.1.1', '1.1.1.2', '1.1.2', '1.1.2.1', '1.1.2.2']
        ),
        (
                ['i1', 'i2', 'i3', 'i4', 'i4', 'i3', 'i4', 'i4', 'i2'], 2,
                ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '2.2']
        )
    ]
)
def test_index_hierarchy(func_list, count_master, expected):
    assert UFU.index_hierarchy(func_list, count_master) == expected


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "func_list,count_master,expected",
    [
        (
                ['i1', 'i2', 'i3', 'i4', 'i4', 'i3', 'i4', 'i4', 'i3', 'i2', 'i1', 'i1', 'i2'], 2,
                ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '2.1.3', '2.2',
                 '3', '3.1', '2.3']
        )
    ]
)
def test_index_hierarchy__forward_and_reverse_order_of_levels(func_list, count_master, expected):
    """
    Баговые данные приходят. Проблема с увеличением уровня 1 в конце списка (смотри ..., '3', '3.2', А должно быть
    '3', '3.1').
    Уровень 1 соответствует функции объявленной непосредственно по settings в настройках сценария тестирования.
    Набор 1:
    ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '3', '3.2', '2.2']
    ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '3', '3.1']
    Набор 2
    ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '2.1.3', '2.2', '3', '3.2', '2.3']
    ['2', '2.1', '2.1.1', '2.1.1.1', '2.1.1.2', '2.1.2', '2.1.2.1', '2.1.2.2', '2.1.3', '2.2', '3', '3.1', '2.3']
    """
    assert UFU.index_hierarchy(func_list, count_master) == expected


@pytest.mark.parametrize(
    "parameter_string,expected",
    [
        ("1...5", "1...6"), ("1.1...1.5", "1.1...1.6"), (1, '2'), ([1, 2, 3], False)
    ]
)
def test_count_string(parameter_string, expected):
    assert UFU.count_string(parameter_string) == expected


@pytest.mark.parametrize(
    "func_count_dict,func,expected",
    [
        ("3", "", '1'), ({"1": "1.10"}, "1", '2'), ({"another_key": "1.1.2"}, "another_key", '3'),
        ({"another_key_without_args": "1.1.2"}, "", '1')
    ]
)
def test_priority_index(func_count_dict, func, expected):
    assert UFU.priority_index(func_count_dict, func) == expected


@pytest.mark.parametrize(
    "parms,expected",
    [
        (scenario_dictionary_template['ConstructionCheckMeasurement']['settings'],
         [['description'], ['script'], ['manual_check', 'descript_test', 'set_resettable_params',
                                        'descript_test', 'set_switching_params', 'descript_test'],
          ['set_switching_params_range', 'descript_test', 'set_switching_params', 'descript_test']])
    ]
)
def test_get_funcs_keys_all(parms, expected):
    assert UFU.get_funcs_keys_all(parms) == expected


@pytest.mark.parametrize(
    "parms,func_keys_item,expected",
    [
        (scenario_dictionary_template['ConstructionCheckMeasurement']['settings'], [],
         ['description', 'script', 'manual_check', 'descript_test', 'set_resettable_params', 'descript_test',
          'set_switching_params', 'descript_test', 'set_switching_params_range', 'descript_test',
          'set_switching_params', 'descript_test'])
    ]
)
def test_get_func_keys_item(parms, func_keys_item, expected):
    assert UFU.get_func_keys_item(parms, func_keys_item) == expected



# STARICHENKO ========================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================


# STACK --------------------------------------------------------------------
def test__debug_stack_or_obj_get_class_and_func_names():  # starichenko
    test_obj_link = UFU.debug_stack_or_obj_get_class_and_func_names

    # 1=CLASS ------------------------------------------------
    class Cls:
        def method(self):
            return UFU.debug_stack_or_obj_get_class_and_func_names(self_obj=self)

    obj = Cls()
    result = obj.method()
    _EXPECTED = f"[Cls][method]"
    assert result == _EXPECTED

    # 2=FUNC -------------------------------------------------
    result = test_obj_link()
    _EXPECTED = f"[test_func_universal.py][test__debug_stack_or_obj_get_class_and_func_names]"
    assert result == _EXPECTED


def test__obj_show_attr_all__func_with_decor():   # starichenko
    def my_decorator(func_for_decor):
        def wrapper():
            pass
        return func_for_decor

    @my_decorator
    def my_func():
        pass

    func_link = my_func

    print(func_link)
    print(f"{func_link!r}")
    print(func_link.__name__)

    print(func_link)

    UFU.obj_show_attr_all(func_link)


def test__obj_show_attr_all__func_args_kwargs():   # starichenko
    FUNC_LINK = UFU.obj_show_attr_all
    def my_func_blank():
        pass
    FUNC_LINK(my_func_blank, go_nested_max=10, go_iterables_max=5)

    def my_func_args(arg_a, arg_b, arg_c):
        pass
    FUNC_LINK(my_func_args, go_nested_max=10, go_iterables_max=5)

    def my_func_kargs(karg_a=1, karg_b=2, karg_c=3):
        pass
    FUNC_LINK(my_func_kargs, go_nested_max=10, go_iterables_max=5)

    def my_func_args_kargs(arg_a, arg_b, arg_c, karg_a=1, karg_b=2, karg_c=3):
        pass
    FUNC_LINK(my_func_args_kargs, go_nested_max=10, go_iterables_max=5)


# 0=CLASSES ==========================================================================================================
pass


# !!!!!!!!!!!!!!!!!!!!!!! ТИПОВОЙ ПРИМЕР РАБОТЫ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@pytest.mark.parametrize(
    argnames="p1,_func_result,_EXPECTED,_EXPECT_COMPARE",   #_EXPECT_COMPARE=ожидание по сравнению
    argvalues=[
        (None, None, {}, True),       # BLANK input
        ({}, None, {}, True),

        ({1: 1}, None, {1: 1}, True),   # exact input
        ({"a": "a"}, None, {"a": "a"}, True),

        (None, lambda r: r.abc, None, True),  # ACCESS KEYS
        ({}, lambda r: r.abc, None, True),
        ({1: 1}, lambda r: r.abc, None, True),
        ({"abc": 1}, lambda r: r.abc, 1, True),

        (None, bool, False, True),  # BOOL
        ({}, bool, False, True),
        ({1: 1}, bool, True, True),

        (None, list, [], True),  # LIST
        ({}, list, [], True),
        ({1: 1}, list, [1], True),

        (None, lambda r: 1 in r, False, True),  # IN
        ({}, lambda r: 1 in r, False, True),
        ({1: 1}, lambda r: 1 in r, True, True),

        (None, lambda r: r.update({}) or r, {}, True),  # UPDATE
        ({}, lambda r: r.update({1: 1}) or r, {1: 1}, True),
        ({1: 1}, lambda r: r.update({1: 1}) or r, {1: 1}, True),
        ({"a": "a"}, lambda r: r.update({1: 1}) or r, {1: 1, "a": "a"}, True),

        (None, lambda r: r.pop(), UFU.STR_EXCEPTION_MARK, True),  # POP
        ({}, lambda r: r.pop(), UFU.STR_EXCEPTION_MARK, True),
        ({1: 1}, lambda r: r.pop(), UFU.STR_EXCEPTION_MARK, True),
        ({1: 1}, lambda r: r.pop(2), UFU.STR_EXCEPTION_MARK, True),
        ({1: 1}, lambda r: r.pop(1), 1, True),
        ({"a": "a"}, lambda r: r.pop("a"), "a", True),

        (None, lambda r: list(r.items()), [], True),  # ITEMS
        ({}, lambda r: list(r.items()), [], True),
        ({1: 1}, lambda r: list(r.items()), [(1, 1), ], True),
        ({1: 1, "a": "a"}, lambda r: list(r.items()), [(1, 1), ("a", "a")], True),

        (None, lambda r: list(iter(r)), [], True),  # ITER
        ({}, lambda r: list(iter(r)), [], True),
        ({1: 1}, lambda r: list(iter(r)), [1], True),
        ({1: 1, "a": "a"}, lambda r: list(iter(r)), [1, "a"], True),

        ({}, copy.copy, {}, True),    # COPY
        ({1: 1}, copy.copy, {1: 1}, True),
        ({1: 1, "a": "a"}, copy.copy, {1: 1, "a": "a"}, True),

        ({}, len, 0, True),  # LEN
        ({1: 1}, len, 1, True),
        ({1: 1, "a": "a"}, len, 2, True),

        ({}, str, "{}", True),  # STR
        ({1: 1}, str, "{1: 1}", True),
        ({1: 1, "a": "a"}, str, "{1: 1, 'a': 'a'}", True),
    ])
def test__DictDotAttrAccess(p1, _func_result, _EXPECTED, _EXPECT_COMPARE):  # starichenko
    test_obj_link = UFU.DictDotAttrAccess

    if _func_result is None:
        result_func_link = lambda i: i
    else:
        result_func_link = _func_result

    try:
        if p1 is None:
            result = result_func_link(test_obj_link())
        else:
            result = result_func_link(test_obj_link(p1))
    except:
        result = UFU.STR_EXCEPTION_MARK

    assert (result == _EXPECTED) == _EXPECT_COMPARE


def test__ClsCountExecutions():
    test_obj_link = UFU._ClsCountExecutions

    assert test_obj_link.COUNT == 0

    # test_obj = test_obj_link()
    assert test_obj_link().COUNT == 1
    assert test_obj_link().COUNT == 2
    assert test_obj_link.COUNT == 2

    test_obj_link._clear_counter()
    assert test_obj_link.COUNT == 0


# DECORATORS =========================================================================================================
@pytest.mark.parametrize(
    argnames="p1,_p1,_p2,_EXPECTED",
    argvalues=[
        # correct
        (1, 0.1, True, True),
        (1, 0.1, None, None),
        (1, 0.1, 123, 123),
        (1, 0.1, "123", "123"),

        # wrong
        (1, 1, True, UFU.STR_EXCEPTION_MARK),   # must be real wrong!!!
        (0.1, 1, True, UFU.STR_EXCEPTION_MARK),
    ]
)
def test__decorator_timeout(p1,_p1,_p2,_EXPECTED):
    test_obj_link = UFU.decorator_timeout

    @test_obj_link(p1)
    def victim():
        time.sleep(_p1)
        return _p2

    start = time.time()
    result = victim()
    real_execute_time = time.time() - start
    assert result == _EXPECTED
    assert real_execute_time <= p1 + 0.3    # additional 0.1 is not enough!!! 50% success!!! 0.3 is the best!!!


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__decorator_if_error_return_none_and_log_explanation():
    test_obj_link = UFU.decorator_try__return_none_and_log_explanation


# FUNCS ===============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (lambda: 123, []),
        (lambda a: 123, ["a", ]),
        (lambda a, b: 123, ["a", "b"]),
        (lambda a, b, c=123: 123, ["a", "b", "c"]),
    ]
)
def test__func_get_arg_names_list(p1, _EXPECTED):
    test_obj_link = UFU.func_get_arg_names_list

    result = test_obj_link(func_link=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED,__counter",
    argvalues=[
        # LINKS BARE -------------------------------------------------------------
        # TRIVIAL ONE
        ([], False, False, True, 0),
        ([UFU.FUNC_LINK_LAMBDA_TRUE], False, False, True, 0),
        ([UFU.FUNC_LINK_LAMBDA_FALSE], False, False, False, 0),
        ([UFU.FUNC_LINK_LAMBDA_NONE], False, False, False, 0),

        # TRIVIAL SEVERAL
        ([UFU.FUNC_LINK_LAMBDA_TRUE, UFU.FUNC_LINK_LAMBDA_TRUE], False, False, True, 0),   # all True

        ([UFU.FUNC_LINK_LAMBDA_TRUE, UFU.FUNC_LINK_LAMBDA_FALSE], False, False, False, 0),   # first True
        ([UFU.FUNC_LINK_LAMBDA_TRUE, UFU.FUNC_LINK_LAMBDA_NONE], False, False, False, 0),

        ([UFU.FUNC_LINK_LAMBDA_FALSE, UFU.FUNC_LINK_LAMBDA_TRUE], False, False, False, 0),   # last True
        ([UFU.FUNC_LINK_LAMBDA_NONE, UFU.FUNC_LINK_LAMBDA_TRUE], False, False, False, 0),

        ([UFU.FUNC_LINK_LAMBDA_FALSE, UFU.FUNC_LINK_LAMBDA_FALSE], False, False, False, 0),  # all false
        ([UFU.FUNC_LINK_LAMBDA_FALSE, UFU.FUNC_LINK_LAMBDA_NONE], False, False, False, 0),
        ([UFU.FUNC_LINK_LAMBDA_NONE, UFU.FUNC_LINK_LAMBDA_FALSE], False, False, False, 0),
        ([UFU.FUNC_LINK_LAMBDA_NONE, UFU.FUNC_LINK_LAMBDA_NONE], False, False, False, 0),

        # flag_run_all
        ([UFU._ClsCountExecutions.FALSE, UFU._ClsCountExecutions.TRUE], False, False, False, 1),
        ([UFU._ClsCountExecutions.FALSE, UFU._ClsCountExecutions.TRUE], True, False, False, 2),


        # DICTS --------------------------------------------------------------------------------------------------
        # 1=decide_run_sequence
        # 1=decide_run_sequence=1=blank sequence
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": False,
              "result_sequence_if_decided_run_fail": 123},
         ],
         False, False, True, 1),
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
         ],
         False, False, True, 1),
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
         ],
         False, False, 123, 1),
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": False,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
         ],
         False, False, True, 1),
        # 1=decide_run_sequence=2=blank sequence=2=DOUBLE
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 456},
         ],
         False, False, True, 2),
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 456},
         ],
         False, False, 123, 1),
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.TRUE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 456},
         ],
         False, False, 456, 2),

        # 1=decide_run_sequence=2=NOT blank sequence=1=LINK
        ([
             {"question": "hello",
              "func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": True,
              "decide_run_sequence": True,
              "result_sequence_if_decided_run_fail": 123},
             UFU._ClsCountExecutions.TRUE
         ],
         False, False, 123, 1),

        # 2=DICTS ====================================================================================================
        # 1=trivial
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE},
             {"func_link": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, True, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE},
             {"func_link": UFU._ClsCountExecutions.FALSE},
         ],
         False, False, False, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, False, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.FALSE},
         ],
         False, False, False, 1),

        # 2=expected_answer
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": False},
         ],
         False, False, True, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "expected_answer": True},
         ],
         False, False, False, 1),

        # 3=use_answer
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "use_answer": False},
         ],
         False, False, True, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "use_answer": False},
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "use_answer": False},
         ],
         False, False, True, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "use_answer": False},
             {"func_link": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, True, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "use_answer": False},
             {"func_link": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, True, 2),

        # 4=skip
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "skip": True},
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "skip": True},
         ],
         False, False, True, 0),

        # 5=always1_run
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,  # +skip
              "skip": True,
              "always1_run": True},
         ],
         False, False, True, 0),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "always1_run": True},
         ],
         False, False, False, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "always1_run": True},
             {"func_link": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, False, 2),

        # flag_run_all=True ==========================================================================================
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.TRUE},
             {"func_link": UFU._ClsCountExecutions.NONE},
         ],
         True, False, False, 3),
        # 6=always2_stop_if_step_false
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "always2_stop_if_step_false": True},
             {"func_link": UFU._ClsCountExecutions.FALSE},
         ],
         True, False, False, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "always2_stop_if_step_false": True},
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "always1_run": True},                         # +always1_run - not important!
         ],
         True, False, False, 2),

        # always2_stop_if_was_false
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "always2_stop_if_was_false": True},
         ],
         True, False, False, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE},
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "always2_stop_if_was_false": True},
         ],
         True, False, False, 1),

        # RESULTS =  ==================================================================
        # func_link_if_correct
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "func_link_if_correct": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, True, 2),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "func_link_if_correct": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, False, 1),
        # func_link_if_wrong -----------------------------------------------
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "func_link_if_wrong": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, True, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "func_link_if_wrong": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, False, 2),

        # func_link_if_exception
        ([
             {"func_link": UFU._ClsCountExecutions.EXCEPTION,
              "func_link_if_exception": UFU._ClsCountExecutions.TRUE},
         ],
         False, True, UFU.STR_EXCEPTION_MARK, 1),    # must execute ONLY ONE!!! EXCEPTION IS RAISED before second func
        ([
             {"func_link": UFU._ClsCountExecutions.EXCEPTION,
              "func_link_if_exception": UFU._ClsCountExecutions.TRUE},
         ],
         False, False, False, 2),

        # func_link_with_result
        ([
             {"func_link": UFU._ClsCountExecutions.TRUE,
              "func_link_with_result": UFU._ClsCountExecutions.set_value},
             {"func_link": lambda: UFU._ClsCountExecutions.VALUE},
         ],
         False, False, True, 1),
        ([
             {"func_link": UFU._ClsCountExecutions.FALSE,
              "func_link_with_result": UFU._ClsCountExecutions.set_value,
              "use_answer": False},
             {"func_link": lambda: UFU._ClsCountExecutions.VALUE == False},
         ],
         False, False, True, 1),
    ]
)
def test__funcs_all_true(p1,p2,p3,_EXPECTED,__counter):
    test_obj_link = UFU.funcs_all_true
    class_counter = UFU._ClsCountExecutions
    class_counter._clear_counter()

    try:
        result = test_obj_link(funcs_link_sequence=p1, flag_run_all=p2)
    except:
        result = UFU.STR_EXCEPTION_MARK

    count_called_funcs = class_counter.COUNT
    assert result == _EXPECTED and count_called_funcs == __counter

@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        # TRIVIAL
        (lambda _p1: _p1, {"_p1": True}, 30, True),
        (lambda _p1: _p1, {"_p1": False}, 1, None),

        # VICTIM
        ("victim_time_sleep", {"sleep": 0.1, "ret": True}, 30, True),
        ("victim_time_sleep", {"sleep": 0.1, "ret": False}, 0.5, None),
    ]
)
def test__func_wait_true(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.func_wait_true

    # СЛОМАНО!!!!!!
    # СЛОМАНО!!!!!!
    # СЛОМАНО!!!!!!
    # СЛОМАНО!!!!!!
    # СЛОМАНО!!!!!!

    def victim_time_sleep(sleep, ret):
        time.sleep(sleep)
        return ret

    if p1 == "victim_time_sleep":
        p1 = victim_time_sleep

    result = test_obj_link(func_link=p1, kwargs=p2, timeout=p3)
    assert result == _EXPECTED


# VALUES ==============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,p5,_EXPECTED",
    argvalues=[
        # TRIVIAL
        ("", True, True, False, [], True),
        (f"", True, True, False, [], True),
        (r"", True, True, False, [], True),
        (b"", True, True, False, [], True),
        (None, True, True, False, [], True),
        ((), True, True, False, [], True),
        ([], True, True, False, [], True),
        ([""], True, True, False, [], False),
        ({}, True, True, False, [], True),
        (0, True, True, False, [], True),
        (0.0, True, True, False, [], True),

        # # BOOL
        (False, True, True, False, [], False),
        (False, True, True, True, [], True),

        # SPACES ONLY
        (" ", True, True, False, [], True),
        ("  ", True, True, False, [], True),
        (" ", False, True, False, [], False),
        (" ", False, True, False, [" "], True),
        ("  ", False, True, False, [" "], False),

        # SPACES INSIDE
        (" 1", True, True, False, [], False),
        (" 1", False, True, False, [], False),
        (" 1", True, True, False, ["1"], True),
        (" 1", False, True, False, ["1"], False),

        (" 1  2 ", True, True, False, ["12"], False),

        # NUMBS
        (1, True, True, False, [], False),
        (1, True, True, False, [1], True),
        (1, False, True, False, [1], True),
    ]
)
def test__value_is_blanked(p1, p2, p3, p4, p5, _EXPECTED):  # starichenko
    test_obj_link = UFU.value_is_blanked
    result = test_obj_link(source=p1, spaces_as_blank=p2, zero_as_blank=p3, false_as_blank=p4, addition_equivalent_list=p5)
    assert result == _EXPECTED


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__value_raise_if_blank():
    test_obj_link = UFU.value_raise_if_blank


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__value_convert_to_bool():
    test_obj_link = UFU.value_convert_to_bool


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        # DIRECT PATTERN
        ("", r"", [str, int, float], True),
        (1, r"1", [str, int, float], True),
        (1.2, r"1.2", [str, int, float], True),
        ("1", r"1", [str, int, float], True),
        ("11", r"1", [str, int, float], False),

        # INDIRECT PATTERN
        ("1", r"\d", [str, int, float], True),
        ("123", r"\d*", [str, int, float], True),
        ("", r"\d*", [str, int, float], True),
        (1.23, r"\d*", [str, int, float], False),
        (1.23, r"[\d.]*", [str, int, float], True),
    ]
)
def test__value_check_by_pattern(p1, p2, p3, _EXPECTED):
    test_obj_link = UFU.value_check_by_pattern
    result = test_obj_link(source=p1, pattern=p2, types_seq=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (None, True, []),
        (None, False, [None]),

        ("", True, []),
        ("", False, [""]),

        ([], True, []),
        ([], False, []),    # !!!

        ({}, True, []),
        ({}, False, {}),

        (0, True, [0, ]),
        ("0", True, ["0", ]),
        (1, True, [1, ]),
        ("1", True, ["1", ]),
        ("123", True, ["123", ]),
        ("123", False, ["123", ]),

        ([1, 2], True, [1, 2]),
        ({1: 1}, True, {1: 1}),
    ]
)
def test__value_make_sequence_if_not_sequence(p1, p2, _EXPECTED):
    test_obj_link = UFU.value_make_sequence_if_not_sequence
    result = test_obj_link(source=p1, return_empty_list_if_blanked=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        (None, ["1", ], 1, None),   # 0=not string
        (None, ["1", None], 1, None),
        ([], ["1", None], 1, None),
        ([], ["1", []], 1, []),
        ((), ["1", ()], 1, ()),

        ("123", ["1", "12"], 1, "1"),   # 1=STARTS
        (" 123", ["1", "12"], 1, None),
        (123, ["1", "12"], 1, None),
        (123, ["1", 123], 1, 123),

        ("123", ["1", "12"], 2, None),  # 2=FULL
        ("12", ["1", "12"], 2, "12"),
        (" 123", ["1", "12"], 2, None),

        ("123", ["1", "12", "23"], 3, "23"),  # 3=ENDS
        ("12", ["1", "12"], 3, "12"),
        (123, ["1", "123"], 3, None),

        ("123", ["1", "12", "23"], 4, "1"),  # 4=ANY
        ("12", ["1", "12"], 4, "1"),
        (123, ["1", "123", 12, 123], 4, 123),
        ("23", ["1", "123", "2"], 4, '2'),
        ("23", ["1", "123", "\d*"], 4, None),

        ("123", ["1", "12", "\d*"], 5, "\d*"),  # 5=FULLMATCH
        ("12", ["1", "12"], 5, "12"),
        (123, ["1", "123"], 5, None),
    ]
)
def test__value_search_by_list(p1, p2, p3, _EXPECTED):
    test_obj_link = UFU.value_search_by_list
    result = test_obj_link(source=p1, search_list=p2, search_type_1starts_2full_3ends_4any_5fullmatch=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        (None, {}, 1, r"\{\{.*\}\}", (None, None)),   # 0=not string
        (None, {"1": "1", }, 1, r"\{\{.*\}\}", (None, None)),
        (None, {None: 1, }, 1, r"\{\{.*\}\}", (None, None)),
        ([], {None: 1, }, 1, r"\{\{.*\}\}", (None, None)),
        ((), {(): 1, }, 1, r"\{\{.*\}\}", ((), 1)),

        ("123", {"2": 1, "{{nested}}": {"12": 12}}, 1, r"\{\{.*\}\}", ("12", 12)),  # Nested
        ("123", {"2": 1, "notNested": {"12": 12}}, 1, r"\{\{.*\}\}", (None, None)),

        ("123", {("1", "12"): 1, }, 1, r"\{\{.*\}\}", ("1", 1)),  # tuples
        (123, {"1": 1, ("123", 123): ("123", 123)}, 2, r"\{\{.*\}\}", (123, ("123", 123))),

        ("123", {"1": 1, "12": 12}, 1, r"\{\{.*\}\}", ("1", 1)),   # 1=STARTS
        (" 123", {"1": 1, "12": 12}, 1, r"\{\{.*\}\}", (None, None)),
        (123, {"1": 1, "12": 12}, 1, r"\{\{.*\}\}", (None, None)),
        (123, {"1": 1, 123: 123}, 1, r"\{\{.*\}\}", (123, 123)),

        ("123", {"1": 1, "12": 12}, 2, r"\{\{.*\}\}", (None, None)),  # 2=FULL
        ("123", {"1": 1, "123": 123}, 2, r"\{\{.*\}\}", ("123", 123)),
        (123, {"1": 1, "123": 132}, 2, r"\{\{.*\}\}", (None, None)),
        (123, {"1": 1, 123: 123}, 2, r"\{\{.*\}\}", (123, 123)),

        ("123", {"1": 1, "23": 23}, 3, r"\{\{.*\}\}", ("23", 23)),  # 3=ENDS
        ("123", {"1": 1, "123": 123}, 3, r"\{\{.*\}\}", ("123", 123)),
        (123, {"1": 1, "123": 123}, 3, r"\{\{.*\}\}", (None, None)),
        (123, {"1": 1, 123: 123}, 3, r"\{\{.*\}\}", (123, 123)),

        ("123", {"1": 1, "12": 12}, 4, r"\{\{.*\}\}", ("1", 1)),  # # 4=ANY
        (" 123", {"1": 1, "12": 12}, 4, r"\{\{.*\}\}", ('1', 1)),
        (123, {"1": 1, "12": 12}, 4, r"\{\{.*\}\}", (None, None)),
        (123, {"1": 1, 123: 123}, 4, r"\{\{.*\}\}", (123, 123)),
        ("1", {"12": 12, r"\d*": 1}, 4, r"\{\{.*\}\}", (None, None)),

        ("123", {"1": 1, "12": 12, "123": 123}, 5, r"\{\{.*\}\}", ("123", 123)),  # 5=FULLMATCH
        (" 123", {"1": 1, "\d*": 123, "[\d ]*": 123}, 5, r"\{\{.*\}\}", ("[\d ]*", 123)),
        (123, {"1": 1, "\d*": 12}, 5, r"\{\{.*\}\}", (None, None)),
    ]
)
def test__value_search_by_dict_return_key_and_value(p1, p2, p3, p4, _EXPECTED):
    test_obj_link = UFU.value_search_by_dict_return_key_and_value
    result = test_obj_link(source=p1, search_dict=p2, search_type_1starts_2full_3ends_4any_5fullmatch=p3, _nested_key_pattern=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        (None, {}, 1, True, None),   # 0=not string
        (None, {}, 1, False, None),
        (None, {"1": "1", }, 1, True, None),
        # (None, {None: 1, }, 1, True, 1),
        ([], {None: 1, }, 1, True, []),
        ((), {(): 1, }, 1, True, 1),

        ("123", {"2": 1, "{{nested}}": {"12": 12}}, 1, True, 12),  # Nested
        ("123", {"2": 1, "notNested": {"12": 12}}, 1, True, "123"),

        ("123", {("1", "12"): 1, }, 1, True, 1),  # tuples
        (123, {"1": 1, ("123", 123): ("123", 123)}, 2, True, ("123", 123)),

        ("123", {"1": 1, "12": 12}, 1, True, 1),   # 1=STARTS
        (" 123", {"1": 1, "12": 12}, 1, True, " 123"),
        (123, {"1": 1, "12": 12}, 1, True, 123),
        (123, {"1": 1, 123: 123}, 1, True, 123),

        # other is the same!!!
    ]
)
def test__value_try_replace_by_dict(p1, p2, p3, p4, _EXPECTED):
    test_obj_link = UFU.value_try_replace_by_dict
    result = test_obj_link(source=p1, search_dict=p2, search_type_1starts_2full_3ends_4any_5fullmatch=p3, return_source_if_not=p4)
    assert result == _EXPECTED


# PARAMS ==============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (None, None, []),
        ({}, None, []),
        ({}, {}, []),

        # values
        ({1:1}, {1:1}, []),
        ({1: 1}, {1: 2}, [1]),

        # list
        ({1: [1,2]}, {1: 2}, []),

        # dict
        ({1: {1: {2: 2}}}, {}, [1]),
        ({1: {1: {2: 2}}}, {1: 2}, [1]),
        ({1: {1: {2: 2}}}, {1: 1}, [2]),
        ({1: {1: {2: 2}}}, {2: 2}, [1]),

        ({1: {1: {2: 2}}}, {1: 1, 2: 2}, []),
        ({1: {1: {2: 2}}}, {1: 1, 2: 8}, [2]),
        ({1: {1: {2: [2, 8]}}}, {1: 1, 2: 8}, []),

        ({"1": {"1": {"2": ["2", "8"]}}}, {1: 1, 2: 8}, ["1"]),
        ({"1": {"1": {"2": ["2", "8"]}}}, {"1": "1", "2": "8"}, []),
    ]
)
def test__params_check_dependencies_return_wrong_list(p1, p2, _EXPECTED):
    test_obj_link = UFU.params_check_dependencies_return_wrong_list
    result = test_obj_link(source=p1, func_link_read_param_or_dict=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        ([], None, False),

        # INT_STR
        ([1, 1, "1"], None, True),
        ([1, 1, "2"], None, False),
        ([1, 1, "2"], 1, True),

        # STRINGS
        (["1", "1"], None, True),
        (["1", "2"], None, False),
        (["1", "2"], 1, True),

        # FLOAT
        ([1.1, 1.1, "01.10"], None, True),
        ([1.1, 1.0, "01.10"], 0, False),
        ([1.1, 1.0, "01.10"], 0.1, True),
    ]
)
def test__params_check_deviation_or_equel__str_or_float(p1, p2, _EXPECTED):
    test_obj_link = UFU.params_check_deviation_or_equel__str_or_float
    result = test_obj_link(source=p1, deviation=p2)
    assert result == _EXPECTED


# TYPE ================================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # P1 = different SOURCE
        (123, str, False),
        ("123", str, True),

        ([], tuple, False),  # tuple
        ((), tuple, True),
        ((123), tuple, False),               # !
        ((123, 123), tuple, True),

        ([], list, True),    # list
        ([123], list, True),
        ([123, 123], list, True),

        # P2 = different format of TYPES_SEQ
        (123, str, False),

        (123, int, True),
        (123, (int,), True),
        (123, (int, str), True),
        (123, [int, str], True),
        (123, {int, str}, True),
        (123, {int:1, str:2}, True),
    ]
)
def test__type_check_by_variants(p1,p2,_EXPECTED):
    test_obj_link = UFU.type_check_by_variants

    try:
        result = test_obj_link(source=p1, types_seq=p2)
    except:
        result = UFU.STR_EXCEPTION_MARK

    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (None, True),
        (True, True),
        (False, True),
        (bool(), True),

        (0, True),
        (123, True),
        (123.123, True),
        (123/123, True),
        (123+123, True),

        ("", True),
        ("123", True),
        ("""123""", True),
        (UFU.STR_EXCEPTION_MARK, True),

        (b"", True),
        (b"123", True),
        (b"""123""", True),

        ([], True),
        ([123], True),
        ((), True),
        ((123), True),      # !
        ((123,), True),
        (set(), True),
        ({123}, True),
        (dict(), True),
        ({123:123}, True),

        (lambda: 123, False),
        (UFU.FUNC_LINK_LAMBDA_TRUE, False),
    ]
)
def test__type_is_elementary_single_or_container(p1,_EXPECTED):
    test_obj_link = UFU.type_is_elementary_single_or_container
    result = test_obj_link(source=p1)
    assert result == _EXPECTED

@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (None, True),
        (True, True),
        (False, True),
        (bool(), True),

        (0, True),
        (123, True),
        (123.123, True),
        (123/123, True),
        (123+123, True),

        ("", True),
        ("123", True),
        ("""123""", True),
        (UFU.STR_EXCEPTION_MARK, True),

        (b"", True),
        (b"123", True),
        (b"""123""", True),

        ([], False),
        ([123], False),
        ((), False),
        ((123), True),      # !
        ((123,), False),
        (set(), False),
        ({123}, False),
        (dict(), False),
        ({123:123}, False),

        (lambda: 123, False),
        (UFU.FUNC_LINK_LAMBDA_TRUE, False),
    ]
)
def test__type_is_elementary_single(p1,_EXPECTED):
    test_obj_link = UFU.type_is_elementary_single
    result = test_obj_link(source=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # all types
        (None, False, False),

        # NUMBERS
        (0, False, True),
        (0.0, False, True),
        (0.1, False, True),
        (1.1, False, True),

        # str
        ("", False, False),
        ("123", False, True),
        ("123 ", False, True),
        (" 123 ", False, True),

        ("1.0", False, False),
        ("1.0", True, True),
        ("1.2", False, False),
        ("1.2", True, True),
        ("1,2", True, False),

        ("1.2.3", True, False),

        ("#123", False, False),
        ("#123", True, False),

        # collections
        ({}, False, False),
        ({123}, False, False),
        ((), False, False),
        ((123), False, True),   # !
        ((123, ), False, False),
        ([], False, False),
        ([123], False, False),
        (dict(), False, False),
        ({1: 1}, False, False),
    ]
)
def test__type_is_intable(p1,p2,_EXPECTED):
    test_obj_link = UFU.type_is_intable
    result = test_obj_link(source=p1, float_before=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        # all types
        (None, False),

        # NUMBERS
        (0, True),
        (0.0, True),
        (0.1, True),
        (1.1, True),

        # str
        ("", False),
        ("123", True),
        ("123 ", True),
        (" 123 ", True),

        ("1.0", True),
        ("1.2", True),
        ("1.2", True),
        ("1,2", False),

        ("1.2.3", False),

        ("#123", False),

        # collections
        ({}, False),
        ({123}, False),
        ((), False),
        ((123), True),   # !
        ((123, ), False),
        ([], False),
        ([123], False),
        (dict(), False),
        ({1: 1}, False),
    ]
)
def test__type_is_floatable(p1,_EXPECTED):
    test_obj_link = UFU.type_is_floatable
    result = test_obj_link(source=p1)
    assert result == _EXPECTED


argvalues_for__type_is_iterable=[
    # SINGLE
    (None, True, True, False),
    (True, True, True, False),
    (False, True, True, False),

    (0, True, True, False),
    (1, True, True, False),
    (123, True, True, False),
    (123.123, True, True, False),

    # STR
    ("", True, True, True),
    ("123", True, True, True),
    ("123", True, False, False),

    (b"", True, True, True),
    (b"123", True, True, True),
    (b"123", True, False, False),

    # ITERABLES
    ({}, True, True, True),
    ([], True, True, True),
    ((), True, True, True),

    ({1}, True, True, True),
    ([1], True, True, True),
    ((1), True, True, False),   # !
    ((1, ), True, True, True),

    (iter("123"), True, True, True),

    # DICT
    (dict(), True, True, True),
    (dict(), False, True, False),
    ({1: 1}, True, True, True),
    ({1: 1}, False, True, False),

    # RANGE
    (range(3), True, True, True),
]

@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=argvalues_for__type_is_iterable
)
def test__type_is_iterable(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.type_is_iterable

    result = test_obj_link(source=p1, dict_as_iterable=p2, str_and_bytes_as_iterable=p3)
    assert result == _EXPECTED


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=argvalues_for__type_is_iterable
)
def test__type_is_iterable_but_not_str(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.type_is_iterable_but_not_str


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__type_is_iterable_but_not_dict():
    test_obj_link = UFU.type_is_iterable_but_not_dict


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__type_is_iterable_but_not_dict_or_str():
    test_obj_link = UFU.type_is_iterable_but_not_dict_or_str


@pytest.mark.skip("СДЕЛАТЬ ПОТОМ!!!**********************************************************")
def test__type_is_instance_of_any_user_class():
    test_obj_link = UFU.type_is_instance_of_any_user_class


# STRING ==============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # TRIVIAL
        ("", False, ""),
        ("", True, None),

        # SPACES ONLY
        # (" ", False, True),

        # SPACES INSIDE
        # (" 1", False, False),

        # NUMBS
        # INT
        (1, False, 1),
        (1, True, 1),
        ("1", False, 1),
        (" 123 ", False, 123),
        (" 123 ", True, 123),
        (" 1 23 ", False, " 1 23 "),
        (" 1 23 ", True, None),

        # FLOAT
        (1.23, False, 1),
        (1.23, True, 1),
        ("1.23", False, 1),
        ("1.23", True, 1),
        (" 1.23 ", False, 1),
        (" 1.23 ", True, 1),

    ]
)
def test__str_try_to_int(p1, p2, _EXPECTED):
    test_obj_link = UFU.str_try_to_int
    result = test_obj_link(source=p1, none_if_exception=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        # TRIVIAL
        ("", False, None, ""),
        ("", True, None, None),

        # SPACES ONLY
        # (" ", False, True),

        # SPACES INSIDE
        # (" 1", False, False),

        # NUMBS
        # INT
        (1, False, None, 1),
        (1, True, None, 1),
        ("1", False, None, 1),
        (" 123 ", False, None, 123),
        (" 123 ", True, None, 123),
        (" 1 23 ", False, None, " 1 23 "),
        (" 1 23 ", True, None, None),

        # FLOAT
        (1.00, False, None, 1),
        (" 1.00 ", False, None, 1),
        (1.23, True, None, 1.23),
        ("1.23", False, None, 1.23),
        ("1.23", True, None, 1.23),
        (" 1.23 ", False, None, 1.23),
        (" 1.23 ", True, None, 1.23),

        # ROUND
        (" 1.23 ", True, 0, 1),
        (" 1.23 ", True, 1, 1.2),
        (" 1.23456 ", True, 4, 1.2346),

    ]
)
def test__str_try_to_float(p1, p2, p3, _EXPECTED):
    test_obj_link = UFU.str_try_to_float
    result = test_obj_link(source=p1, none_if_exception=p2, round_float=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        (None, 5, "...", 3, None),
        ("", 5, "...", 3, ""),
        ("123456", 3, "...", 3, "..."),

        ("123", 3, "#", 3, "123"),

        ("1223", 3, "#", 1, "#23"),
        ("1223", 3, "#", 2, "1#3"),
        ("1223", 3, "#", 3, "12#"),

        ("1223", 3, "##", 1, "##3"),
        ("1223", 3, "##", 2, "##3"),
        ("1223", 3, "##", 3, "1##"),

        ("1223", 3, "###", 1, "###"),
        ("1223", 3, "###", 2, "###"),
        ("1223", 3, "###", 3, "###"),

        ("1223", 1, "###", 1, "#"),
        ("1223", 1, "###", 2, "#"),
        ("1223", 1, "###", 3, "#"),
    ]
)
def test__str_short_with_multydots(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = UFU.str_short_with_multydots
    result = test_obj_link(source=p1, max_len=p2, marker=p3, short_part_1start_2mid_3end=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        # trivial
        (None, None),
        (123, 123),
        ("", ""),
        ("  ", ""),

        ("123\n", "123\n"),
        ("123\n\n", "123\n"),
        ("123\n\n\n\n", "123\n"),
        ("123\n\n\v\t\n\n", "123\n"),
    ]
)
def test__str_replace_blank_lines(p1, _EXPECTED):
    test_obj_link = UFU.str_replace_blank_lines
    result = test_obj_link(source=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        # trivial
        (None, None),
        (123, 123),
        ("", ""),
        ("  ", ""),

        ("123", "123"),
        ("12 3", "123"),
        ("[\n\t\v\f\r ]", "[]"),

    ]
)
def test__str_delete_wightspaces(p1, _EXPECTED):
    test_obj_link = UFU.str_delete_wightspaces
    result = test_obj_link(source=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        # trivial
        (None, None, None, None),
        (123, None, None, 123),
        ("", None, None, ""),
        ("  ", None, None, "  "),

        ("123", None, None, "123"),
        ("12 3", None, None, "12 3"),
        ("[\n\t\v\f\r ]", None, None, "[ ]"),
        (b"[\n\t\v\f\r ]", None, None, b"[ ]"),     # так это не работает!!!!

        ("	VPtNumber", None, None, "VPtNumber"),   #TAB
        ("Slot¬Power¬Set", None, None, "SlotPowerSet"),
        (b"SlotPowerSet", None, None, b"SlotPowerSet"),
        (b"SlotPowerSet\n", None, None, b"SlotPowerSet"),

        ("<VALUE>������v�� �ְ�w�����s���j�5����z��yw�ٞ��o:��~��?.�s?��� �� �w�����U~� ��6�������z|�������վ��������� }�w�f{}���v������W�7�</VALUE>", None, None, "NMSServerUrl"),

    ]
)
def test__str_replace_nonprintable(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.str_replace_nonprintable
    result = test_obj_link(source=p1, new=p2, keep_whitespaces=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # trivial
        (None, [], None),
        (0, [], 0),
        (1, [], 1),
        (1.2, [], 1.2),
        ("", [], None),

        (" 1 ", [], 1),
        (" 1.2 ", [], 1.2),
        (" 1.2 W ", [], None),

        (" 1.2 W ", ["W"], 1.2),
        (" 1. 2 W ", ["W"], None),
    ]
)
def test__str_get_number_near_measure_unit_or_none(p1,p2,_EXPECTED):
    test_obj_link = UFU.str_get_number_near_measure_unit_or_none
    result = test_obj_link(source=p1,measure_unit_list=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,p5,_EXPECTED",
    argvalues=[
        ("000", True, ".", True, False, [0]),
        ("1", True, ".", True, False, [1]),
        ("123", True, ".", True, False, [123]),

        ("1.3", True, ".", True, False, [1.3]),
        ("1,3", True, ".", True, False, [1, ",", 3]),
        ("1,3", True, ".,", True, False, [1.3]),
        ("1,3", True, ".,", True, True, ["1,3"]),   #return_text
        ("1,3", False, ".,", True, False, [1, ",", 3]),
        ("1,3", False, ".,", True, True, ["1", ",", "3"]),     #return_text

        ("1z1.0", True, ".", True, False, [1, "z", 1]),
        ("1z1.0", False, ".", True, False, [1, "z", 1, ".", 0]),

        ("Slot12", False, ".", True, False, ["Slot", 12]),

        # spaces
        ("Slot1 2", False, ".", True, False, ["Slot", 1, 2]),
        (" Sl ot1 2", False, ".", True, False, ["Sl ot", 1, 2]),
        (" Sl ot1 2", False, ".", False, False, [" Sl ot", 1, " ", 2]),
    ]
)
def test__str_get_alphanum_list(p1,p2,p3,p4,p5,_EXPECTED):
    test_obj_link = UFU.str_get_alphanum_list
    result = test_obj_link(source=p1, use_float=p2, float_signs=p3, strip_spaces=p4, return_text=p5)
    assert result == _EXPECTED


# NUMBER ==============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (0, 1, 0),
        (0, 2, 0),

        (1, 1, 1),
        (1, 2, 0),

        (0b1, 1, 1),
        (0b1, 2, 0),
        (0b10, 1, 0),
        (0b10, 2, 1),
        (0b10, 3, 0),
        (0b101, 1, 1),
        (0b101, 2, 0),
        (0b101, 3, 1),

        (2, 1, 0),
        (2, 2, 1),
        (2, 3, 0),
    ]
)
def test__number_get_bit_in_position(p1, p2, _EXPECTED):
    test_obj_link = UFU.number_get_bit_in_position
    result = test_obj_link(source=p1, position=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        # 1=zero_is_first=True
        ([0, 1], -1, True, []),

        ([0, 1], 0, True, [0, ]),
        ([0, 1], 1, True, [1, ]),

        ([0, 1], 2, True, [0, 0]),
        ([0, 1], 3, True, [1, 0]),

        ([0, 1], 4, True, [0, 1]),
        ([0, 1], 5, True, [1, 1]),

        ([0, 1], 6, True, [0, 0, 0]),

        # 2=zero_is_first=False
        ([0, 1], 0, False, []),
        ([0, 1], 1, False, [0, ]),
        ([0, 1], 2, False, [1, ]),
        ([0, 1], 3, False, [0, 0]),

    ]
)
def test__number_convert_to_list_by_baselist(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.number_convert_to_list_by_baselist
    result = test_obj_link(source=p1, number=p2, zero_is_first=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (321.123, None, 321.123),
        (321.123, 0, 321.123),

        (321.123, 1, 320),
        (321.123, 2, 300),
        (321.123, 3, 0),
        (321.123, 4, 0),

        (321.123, -1, 321),
        (321.123, -2, 321.1),
        (321.123, -3, 321.12),
        (321.123, -4, 321.123),     # 321.122 != 321.123
        (321.123, -5, 321.123),     # 321.1229 != 321.123
    ]
)
def test__number_cutting(p1, p2, _EXPECTED):
    test_obj_link = UFU.number_cutting
    result = test_obj_link(source=p1, cutting_level=p2)
    assert result == _EXPECTED


# SEQUENCE ============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,p5,p6,_EXPECTED",
    argvalues=[
        ([1, ],             "",     True, False, False, False, "1"),
        ([1, 2, 3],         "",     True, False, False, False, "123"),
        ([1, 2, 3],         " ",    True, False, False, False, "1 2 3"),
        ([1, 2, "ABC"],     " ",    True, False, False, False, "1 2 ABC"),

        # skip_none
        ([None, 2, 3],      "*",    True, False, False, False, "2*3"),
        ([1, None, 3],      "*",    True, False, False, False, "1*3"),
        ([1, None, 3],      "*",    False, False, False, False, "1*None*3"),

        # revert_order
        ([1, None, 3],      "*",    True, True, False, False, "3*1"),

        # strip_space
        (["  1  ", " ", 3], "*",    True, False, False, False, "  1  * *3"),
        (["  1  ", " ", 3], "*",    True, False, True, False, "1*3"),

        # strip_sep
        (["**1**", "2", 3], "*",    True, False, False, False, "**1**2*3"),
        (["*1*", "2", 3],   "*",    True, False, False, True, "1*2*3"),
    ]
)
def test__sequence_join_to_string_simple(p1,p2,p3,p4,p5,p6,_EXPECTED):
    test_obj_link = UFU.sequence_join_to_string_simple
    result = test_obj_link(source=p1, sep=p2, skip_blank=p3, revert_order=p4, strip_space=p5, strip_sep=p6)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        # blank
        (None, [None]),
        ("", [""]),
        (b"", [b""]),
        (0, [0]),

        # single
        (1, [1]),
        ("1", ["1"]),
        (b"1", [b"1"]),

        # list
        ([1], [1]),
        ([1, 2], [1, 2]),
        (["1"], ["1"]),

        # tuple
        ((1, ), (1, )),
        ((1, 2), (1, 2)),

        # set
        ({1}, {1}),
        ({1, 2}, {1,2}),

        # dict
        ({1:1}, {1:1}),
        ({1:1, 2:2}, {1:1, 2:2}),

        # range
        (range(1), range(1)),
    ]
)
def test__sequence_make_ensured_if_not(p1, _EXPECTED):
    test_obj_link = UFU.sequence_make_ensured_if_not
    result = test_obj_link(source=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        (None, [], None),
        (1, [], None),
        ("123", [], None),

        ([1, 2], [1, 3], {2,3}),
        ([1, 2], [1, 1], {2,}),
        ([1, 1], [1, 1], set()),
        ([1, 1], [2], {1,2}),

        ({1, 1}, {1, 2}, {2}),
    ]
)
def test__sequences_get_different_elements(p1,p2,_EXPECTED):
    test_obj_link = UFU.sequences_get_different_elements
    result = test_obj_link(seq1=p1, seq2=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        ([1, 2], None, None, [1, 2]),
        ([1, 2], 0, None, [1, 2]),

        (None, 1, None, []),
        ([], 1, None, []),
        ([1,2], 1, None, [[1], [2]]),
        ([1, 2, 3], 2, None, [[1,2],[3]]),
        ([1, 2, 3], 3, None, [[1, 2, 3]]),
        ([1, 2, 3], 10, None, [[1, 2, 3]]),

        ((1, 2, 3), 2, None, [[1,2],[3]]),
        ({1:1, 2:2, 3:3}, 2, None, [[1, 2], [3]]),

        # max_groups
        ([1, 2, 3, 4, 5, 6], 2, 0, [[1, 2], [3, 4], [5, 6]]),
        ([1, 2, 3, 4, 5, 6], 2, 1, [[1, 2], ]),
        ([1, 2, 3, 4, 5, 6], 2, 2, [[1, 2], [3, 4]]),
    ]
)
def test__list_split_by_groups(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.list_split_by_groups
    result = test_obj_link(source=p1, elements_in_group=p2, max_groups=p3)
    assert result == _EXPECTED


# LISTS ===============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[

        ([], False, []),
        ([1, 1], False, [1, 1]),
        ([1, 1], True, [1]),

        ([[1], [1]], False, [1, 1]),
        ([[1], [1]], True, [1]),

        ([[1], 1], False, [1, 1]),
        ([[1], 1], True, [1]),
    ]
)
def test__lists_sum(p1, p2, _EXPECTED):
    test_obj_link = UFU.lists_sum
    result = test_obj_link(source_lists=p1, no_repetitions=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[

        ([], 0, []),
        ([1,2,3], 0, [1,2,3]),
        ([(1,2,3)], 0, [(2,3),]),
        ([(1, 2, 3)], 1, [(1, 3), ]),

        # overscored
        ([(1, 2, 3)], 10, [(1, 2, 3), ]),

        # different lengs
        ([(1, ), (1, 2)], 1, [(1, ), (1, )]),

        # different types
        ([(1,), 1], 0, [(), 1]),
    ]
)
def test__list_tuples_del_index(p1, p2, _EXPECTED):
    test_obj_link = UFU.list_tuples_del_index
    result = test_obj_link(tuples_list=p1, index=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[

        ([0, 1, 2], 0, 0),
        ([0, 1, 2], 3, 0),
        ([0, 1, 2], 7, 1),
    ]
)
def test__list_get_item_by_circle_index(p1, p2, _EXPECTED):
    test_obj_link = UFU.list_get_item_by_circle_index
    result = test_obj_link(source=p1, index=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        ([], True, True, []),

        # nums
        ([1], True, True, [1]),
        ([2,1], True, True, [1,2]),

        # str floatable
        (["2", "1"], True, True, ["1", "2"]),
        (["1.2", "1.11", "1"], True, True, ["1", "1.11", "1.2"]),

        # str
        (["a2", "a1"], True, True, ["a1", "a2"]),
        (["a2", "a10"], True, True, ["a10", "a2"]),

        # all
        (["1a", "2", 30], True, True, [30, "2", "1a"]),
        (["1a", "2.1", 30], True, False, ["2.1", 30, "1a"]),   # separate_floatable_and_nums=False

        # int -------------------------
        (["2", "1"], False, True, ["1", "2"]),
        (["2", "1.0"], False, True, ["2", "1.0", ]),

    ]
)
def test__list_sort_simple_floatable_items(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.list_sort_simple_floatable_items
    result = test_obj_link(source=p1,use_float=p2,separate_floatable_and_nums=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        ([], True, []),

        # nums
        ([1], True, [1]),
        ([2,1], True, [1,2]),

        # str floatable
        (["2", "1"], True, ["1", "2"]),
        (["1.2", "1.11", "1"], True, ["1", "1.11", "1.2"]),
        (["1.2", "1.11", "1"], False, ["1", "1.2", "1.11"]),

        # str
        ([1, 10, "1e"], False, [1, "1e", 10]),

        (["a2", "a1"], True, ["a1", "a2"]),
        (["a2", "a10"], True, ["a2", "a10"]),

        # all
        (["1a", "20", 15], True, ["1a", 15, "20"]),

        (["192.168.1.111", "192.168.0.111"], False, ["192.168.0.111", "192.168.1.111"]),

        (["1a", "a2"], True, None),

    ]
)
def test__list_sort_with_correct_inner_numbs(p1,p2,_EXPECTED):
    test_obj_link = UFU.list_sort_with_correct_inner_numbs
    result = test_obj_link(source=p1, use_float=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # nums
        ([], [], []),
        ([1], [], [1]),
        ([2,1], [], [1,2]),

        # str floatable
        (["2", "1"], [], ["1", "2"]),
        (["1.2", "1.11", "1"], [], ["1", "1.2", "1.11"]),

        # str
        (["a2", "a1"], [], ["a1", "a2"]),
        (["a2", "a10"], [], ["a2", "a10"]),

        # all
        ([1, 10, "1e"], [], [1, "1e", 10]),
        (["1a", "20", 15], [], ["1a", 15, "20"]),

        (["192.168.1.111", "192.168.0.111"], [], ["192.168.0.111", "192.168.1.111"]),

        (["1a", "a2", "2a"], [], ["1a", "a2", "2a"]),   ###
        (["1a", "a2", "2a"], ["\d+.*"], ["1a", "2a", "a2"]),

        ([3, "-", "1", "4:CU1", "4:CU0", "FU", 'PS2', 'PS1'], ["-", "\d+.*"], ["-", "1", 3, "4:CU0", "4:CU1", "FU", 'PS1', 'PS2'])
    ]
)
def test__list_sort_by_patterns(p1,p2,_EXPECTED):
    test_obj_link = UFU.list_sort_by_patterns
    result = test_obj_link(source=p1, pattern_priority=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        (["", "1", "2", "11"], "1", None, ["", "2", ]),
        (["", "1", "2", "11"], "1", 100, ["", "2", ]),
        (["", "1", "2", "11"], "1", 50, ["", "2", "11", ]),
    ]
)
def test__list_delete_strings_by_substring(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.list_delete_strings_by_substring

    result = test_obj_link(source=p1, substring=p2, percent=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        ([1, 2, 3, 1], 1, 11, True, [11, 2, 3, 11]),
        ([1, 2, 3, 1], 1, 11, False, [11, 2, 3, 1]),
    ]
)
def test__list_replace_element(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = UFU.list_replace_element

    result = test_obj_link(source=p1, old=p2, new=p3, replace_all=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (None, None),
        (1, None),
        ("123", None),

        ([1, 2, 3], set()),
        ([1, 2, 1], {1}),
        ([1, 1, 1], {1}),
        ([0, 1, 1], {1}),

        ({1,2,3}, set()),

        ({1: 1, 2: 2}, set()),
    ]
)
def test__list_get_repeated_elements(p1,_EXPECTED):
    test_obj_link = UFU.list_get_repeated_elements

    result = test_obj_link(source=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[

        # TRIVIALS
        ([], {}, True, []),

        (["slot1en", "slot2en", "slot2reset"], {}, True, ["slot1en", "slot2en", "slot2reset"]),
        (["slot1en", "slot2en", "slot2reset"], {r"slot\den": "slot{}en"}, True, ["slot{}en", "slot2reset"]),
        (["slot1en", "slot2en", "slot2reset"], {r"slot\den": "slot{}en"}, False, ["slot{}en", "slot{}en", "slot2reset"]),

        # STR
        (["slot1en", "slot2en", "slot2reset"], "slot\den", True, ["slot\den", "slot2reset"]),

        # LIST
        (["slot1en", "slot2en", "slot2reset"], ["slot\den", ], True, ["slot\den", "slot2reset"]),
    ]
)
def test__list_shrink_by_patterns(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.list_shrink_by_patterns
    result = test_obj_link(source=p1, patterns_fullmatch=p2, delete_copies=p3)
    assert result == _EXPECTED


# DICTS ===============================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        #
        # # TRIVIALS
        # ({}, {}, None, {}),
        # ({1:1}, {}, None, {1:1}),
        # ({1:1}, {1:1}, None, {}),
        # ({1:1}, {1: 2}, None, {1:1}),
        # ({1:1, 2:2}, {2: 2}, None, {1: 1}),
        # ({1: 1}, {"1": 1}, None, {1:1}),
        #
        # ({1: 1}, {1: "1"}, lambda x1, x2: str(x1) == str(x2), {}),
        # ({1: 1}, {"1": 1}, lambda x1, x2: str(x1) == str(x2), {1:1}),
    ]
)
def test__dict_compare_by_same_values(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.dict_compare_by_same_values
    result = test_obj_link(source=p1, compare=p2, func=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[

        # TRIVIALS
        ({}, {}, {}),
        ({1:1}, {}, {1:1}),
        ({1: 1}, {1:1}, {1: 1}),
        ({}, {1: 1}, {1: 1}),

        # SEVERAL
        ({1: 1}, {2: 2}, {1: 1, 2: 2}),

        # UPDATE
        ({1: 1}, {1: 111}, {1: 111}),
    ]
)
def test__dicts_merge(p1, p2, _EXPECTED):
    test_obj_link = UFU.dicts_merge
    result = test_obj_link(source_list=(p1,p2))
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        ({}, 1, 2, {}),
        ({1:1}, 1, 2, {2:1}),
        ({1: 1}, "1", 2, {1: 1}),

        ({"k1": "v1", }, "k1", "k2", {"k2": "v1"}),

        ({"k1": "v1", "k2": "v2",  "k3": "v3"}, "k2", "k222", {"k1": "v1", "k222": "v2",  "k3": "v3"}),
    ]
)
def test__dict_key_rename(p1, p2, p3, _EXPECTED):
    test_obj_link = UFU.dict_key_rename__by_name
    result = test_obj_link(source=p1, key=p2, new_key=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        # 0=trivial
        (None, None, None, None, None),
        (1, None, None, None, 1),
        ({}, None, None, None, {}),

        # 1=keys
        ({1: 1}, None, None, None, {1: 1}),
        ({1:1}, 1, None, None, {}),
        ({1: 1}, [2], None, None, {1: 1}),
        ({1: 1}, [1], None, None, {}),
        ({1: 1, 2:2}, [1], None, None, {2:2}),
        ({1: 1, 2:2}, [1], True,  None, {1:1}),  # reverse_decision

        # 2=func_link
        ({1: 1, 2:2}, lambda k: k == 1, None, None, {2:2}),
        ({1: 1, 2:2}, lambda k: k == 1, True,  None, {1:1}),  # reverse_decision

        # 3=nested
        ({1: 1},      1, None, False, {}),
        ({1: {2: 2}}, 1, None, True, {}),
        ({1: {2: 2}}, 2, None, True, {1: {}}),
        ({1: {2: 2}}, 2, True, True, {}),  # reverse_decision
    ]
)
def test__dict_keys_delete_by_name(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = UFU.dict_keys_delete_by_name
    result = test_obj_link(source=p1, keys_list_or_func_link=p2, reverse_decision=p3, nested=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,p5,p6,_EXPECTED",
    argvalues=[
        # 0=trivial
        (None, [], None, None, None, None, None),
        (1, [], None, None, None, None, 1),
        ("1", [], None, None, None, None,  "1"),
        ([], [], None, None, None, None, []),
        ({}, [], None, None, None, None, {}),

        # dict
        ({1:1}, [], None, None, None, None, {1:1}),

        # OLD_VALUES
        ({1: 1}, 1, 111, None, None, None, {1: 111}),
        ({1: 1}, [1], 111, None, None, None, {1: 111}),
        ({1: 1}, lambda v: v==1, 111, None, None, None, {1: 111}),

        ({1: 1, 2:2}, lambda v: v==1, 111, None, None, None, {1: 111, 2:2}),
        ({1: 1, 2: 2}, lambda v: True, 111, None, None, None, {1: 111, 2: 111}),

        # NEW_VALUE
        ({1: 1}, 1, 111, None, None, None, {1: 111}),
        ({1: 1}, 1, lambda v: v*111, None, None, None, {1: 111}),

        # PROTECT_KEYS
        ({1: 1}, 1, 111, 1, None, None, {1: 1}),
        ({1: 1}, 1, 111, [1], None, None, {1: 1}),

        # NESTED
        ({1: 1, 2:{1:1}}, 1, 111, None, False, None, {1: 111, 2:{1:1}}),
        ({1: 1, 2: {1: 1}}, 1, 111, None, True, None, {1: 111, 2: {1: 111}}),

        # DELETE KEYS
        ({1: 1, 2: {1: 1}}, 1, 111, None, False, True, {2: {1: 1}}),
        ({1: 1, 2: {1: 1}}, 1, 111, None, True, True, {2: {}}),
    ]
)
def test__dict_values_replace(p1,p2,p3,p4,p5,p6,_EXPECTED):
    test_obj_link = UFU.dict_values_replace
    result = test_obj_link(
        source=p1,
        old_values_list_or_func_link=p2,
        new_value_or_func_link=p3,
        protect_keys_or_func_link=p4,
        nested=p5,
        delete_found_keys=p6,
    )
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[
        # TRIVIALS
        ({}, None, None),
        ({}, [], None),
        ({1: 1}, [], None),

        ({1: 1}, 1, 1),
        ({1: 1}, [1], 1),
        ({1: 1}, [1, 2], None),
        ({1: 1}, [2, 1], None),
        ({1: 1}, [1, 1], None),

        ({1: {2: 2}}, [1], {2: 2}),
        ({1: {2: 2}}, [1, 2], 2),
        ({1: {2: 2}}, [2, 1], None),

    ]
)
def test__dict_value_get_by_keypath(p1,p2,_EXPECTED):
    test_obj_link = UFU.dict_value_get_by_keypath
    result = test_obj_link(source=p1, keypath=p2)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[

        # 1=LEVEL ----------------------------
        # TRIVIALS
        ([{}, None], None),
        ([{}, {}], {}),
        ([{1: 1}, {}], {1: 1}),
        ([{}, {1: 1}], {1: 1}),
        ([{1: 1}, {1: 1}], {1: 1}),

        # NONE
        ([{1: None}, {1: 1}], {1: 1}),
        ([{1: None}, {1: 1}], {1: 1}),
        ([{1: 1}, {1: None}], {1: None}),

        # SEVERAL
        ([{1: 1}, {2: 2}], {1: 1, 2: 2}),

        # UPDATE
        ([{1: 1}, {1: 111}], {1: 111}),

        # 2=LEVEL ----------------------------
        # SEVERAL
        ([{1: {1:1}}, {2: {2:2}}], {1: {1:1}, 2: {2:2}}),

        # UPDATE
        ([{1: {1: 1}}, {1: {1: 111}}], {1: {1: 111}}),

        # MERGE
        ([{1: {1: 1}}, {1: {2: 2}}], {1: {1: 1, 2: 2}}),

        # 3=LEVEL ----------------------------
        # UPDATE
        ([{1: {1: {1:1}}}, {1: {1: {1:111}}}], {1: {1: {1: 111}}}),

        # MERGE
        ([{1: {1: {1:1}}}, {1: {1: {2:2}}}], {1: {1: {1: 1, 2:2}}}),
    ]
)
def test__dicts_merge(p1,_EXPECTED):
    test_obj_link = UFU.dicts_merge
    result = test_obj_link(source_list=p1)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,p5,_EXPECTED",
    argvalues=[
        # 0=trivial
        (None, 1, False, True, False, None),
        (1, 1, False, True, False, None),
        ({}, 1, False, True, False, []),

        # level 1
        ({1:1}, 1, False, True, False, [1]),
        ({1: 1, 2:2}, 1, False, True, False, [1]),

        # nested
        # no_repetitions
        ({1: 1, 2: {1:1}}, 1, False, True, False, [1]),
        ({1: 1, 2: {1:1}}, 1, False, False, False, [1, 1]),

        # return_first_value
        ({1: 1, 2: {1: 11}}, 1, True, True, False, 1),      # root level
        ({11: 11, 2: {1: 11}}, 1, True, True, False, 11),   # nested

        # use_blank
        ({1: None, 2: {1: 11}}, 1, False, True, True, [None, 11]),
        ({1: None, 2: {1: 11}}, 1, False, True, False, [11]),
        ({1: "", 2: {1: 11}}, 1, False, True, False, [11]),
        ({1: 0, 2: {1: 11}}, 1, False, True, False, [0, 11]),

    ]
)
def test__dict_values_get_list_for_key(p1,p2,p3,p4,p5,_EXPECTED):
    test_obj_link = UFU.dict_values_get_list_for_key
    result = test_obj_link(
        source=p1,
        key=p2,
        return_first_value=p3,
        no_repetitions=p4,
        use_blank=p5,
    )
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        ({}, None, None, None),
        ({}, {}, None, True),
        ({1: 1}, {}, [], False),
        ({1: 1}, {}, [1], False),
        ({1: 1}, {}, [2], True),

        ({1: 1, 2:2}, {2:2}, [2], True),
        ({1: 1, 2: 2}, {2: 22}, [2], False),

    ]
)
def test__dicts_compare(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.dicts_compare
    result = test_obj_link(dict1=p1,dict2=p2, use_only_keys_list=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        ({}, None, True, True, False),
        ({1:1}, "", True, True, False),

        ({}, {}, True, True, True),
        ({1: 1}, {}, True, True, True),
        ({}, {1:1}, True, True, False),
        ({1:1}, {1: 1}, True, True, True),

        # None types
        ({1: 1}, {1: 1}, True, True, True),
        ({1: 1}, {1: None}, True, True, True),
        ({1: None}, {1: 1}, True, True, True),
        ({1: None}, {1: None}, True, True, True),

        # types different
        ({1: 1}, {1: 1}, True, True, True),
        ({1: []}, {1: 1}, True, True, False),
        ({1: {}}, {1: 1}, True, True, False),

        # nested
        ({1: {}}, {1: {}}, True, True, True),
        ({1: {1:1}}, {1: {}}, True, True, True),
        ({1: {1: 1}}, {1: {1:1}}, True, True, True),

        ({1: {}}, {1: {1: 1}}, True, True, False),
        ({1: {}}, {1: {1: 1}}, True, False, True),  # nested=False
        ({1: {1:1}}, {1: {1: ()}}, True, True, False),
        ({1: {1: 1}}, {1: {1: ()}}, True, False, True),  # nested=False

        # allow_extra_keys
        ({1: 1}, {1: 1}, False, True, True),
        ({1: 1}, {}, False, True, False),
        ({1: 1}, {}, True, True, True),

    ]
)
def test__dict_validate_by_etalon(p1,p2,p3,p4,_EXPECTED):
    test_obj_link = UFU.dict_validate_by_etalon
    result = test_obj_link(source=p1, etalon=p2, allow_extra_keys=p3, nested=p4)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,p3,_EXPECTED",
    argvalues=[
        (None, None, None, None),
        ({}, None, None, None),
        ({1:1}, None, None, None),
        ({1: 1}, 1, None, {1:1}),
        ({1: 1}, 111, None, {1:1}),

        ({1: {1:1}}, 1, None, {1: 1}),
        ({1: {1:1}}, 111, None, {1: None}),
        ({1: {1: 1}}, 111, 555, {1: 555}),      # default

        ({1: {1: {1:1}}}, 1, None, {1: {1:1}}),
        ({1: {1: {1:1}}}, 1, None, {1: {1:1}}),

        ({1: {1: 1}, 2:2}, 1, None, {1: 1, 2:2}),   # dont touch not dicts

    ]
)
def test__dict_collapse_values_dict_by_key(p1,p2,p3,_EXPECTED):
    test_obj_link = UFU.dict_collapse_values_dict_by_key
    result = test_obj_link(source=p1, key_priority_seq=p2, default=p3)
    assert result == _EXPECTED


@pytest.mark.parametrize(
    argnames="p1,p2,_EXPECTED",
    argvalues=[

        # TRIVIALS
        ({}, 0, {}),
        ({1:1}, 0, {1:1}),
        ({1:1, 2:2}, 0, {1:1, 2:2}),

        ({}, 1, {}),
        ({1: 1}, 1, {1: 1}),
        ({1: 1, 2: 2}, 1, {1: 1, 2: 2}),

        ({1:{11:11}}, 0, {1: {11:11}}),
        ({1:{11:11}}, 1, {11: 11}),
        ({1: {11: 11, 22:22}}, 1, {11: 11, 22:22}),
        ({1: {11: 11, 22: 22}, 2:2}, 1, {11: 11, 22: 22, 2:2}),

        ({1: {11: 11, 22: 22}, 2: 2}, -1, {11: 11, 22: 22, 2: 2}),
    ]
)
def test__dict_unique__collapse_flatten_by_level(p1, p2, _EXPECTED):
    test_obj_link = UFU.dict_unique__collapse_flatten_by_level
    result = test_obj_link(source=p1, level=p2)
    assert result == _EXPECTED


# TIME ================================================================================================================
def test__TimeoutWorker():  # starichenko
    test_obj_link = UFU.TimeoutWorker

    # 1=check_finish
    timeout = 0.2
    test_obj = test_obj_link(timeout=timeout)
    assert test_obj.check_finish() == False, f"0.0seconds of {timeout}"
    time.sleep(0.1)
    assert test_obj.check_finish() == False, f"0.1seconds of {timeout}"
    time.sleep(0.11)
    assert test_obj.check_finish() == True, f"0.21seconds of {timeout}"

    # 2=restart
    timeout = 0.2
    test_obj = test_obj_link(timeout=timeout)
    assert test_obj.check_finish() == False, f"0.0seconds of {timeout}"
    time.sleep(0.1)
    assert test_obj.check_finish() == False, f"0.1seconds of {timeout}"
    test_obj.restart()
    time.sleep(0.11)
    assert test_obj.check_finish() == False, f"0.21seconds of {timeout}"
    time.sleep(0.11)
    assert test_obj.check_finish() == True, f"0.21seconds of {timeout}"

    # 3=wait_timeout
    timeout = 0.2
    step = 0.05
    time_start = time.time()
    test_obj = test_obj_link(timeout=timeout)
    test_obj.wait_timeout(step=step)
    time_finish = time.time()
    time_process = time_finish - time_start
    assert timeout <= time_process, f"{timeout=} {step=}"
    assert time_process <= timeout+step*3, f"{timeout=} {step=}"

    # 4=drop
    timeout = 1
    step = 0.1
    time_start = time.time()
    test_obj = test_obj_link(timeout=timeout)
    while not test_obj.check_finish():
        test_obj.drop()

    time_finish = time.time()
    time_process = time_finish - time_start
    assert time_process <= step*3, f"{timeout=} {step=}"

    # 5=get_time_passed
    timeout = 0.5
    step = 0.2
    test_obj = test_obj_link(timeout=timeout)

    time.sleep(step)
    time_process = test_obj.get_time_passed()
    assert step <= time_process, f"{timeout=} {step=}"
    assert time_process <= step*2, f"{timeout=} {step=}"

    # +cutting_level
    test_obj.restart()
    time.sleep(step)
    time_process = test_obj.get_time_passed(cutting_level=-2)
    assert step == time_process, f"{timeout=} {step=}"


def test__timedate_get_date_or_time_structtime_part():
    test_obj_link = UFU.timedate_get_date_or_time_structtime_part

    time_20220101_235959 = (2022, 1, 1, 23, 59, 59, 5, 1, -1)

    time_20220101_000000 = (2022, 1, 1,  0,  0,  0, 5, 1, -1)
    time_19000101_235959 = (1900, 1, 1, 23, 59, 59, 0, 1, -1)

    time_19000101_075959 = (1900, 1, 1, 7, 59, 59, 0, 1, -1)

    assert test_obj_link(source=time_20220101_235959, type_1date_2time=1) == time_20220101_000000
    assert test_obj_link(source=time_20220101_235959, type_1date_2time=2) == time_19000101_235959


# OTHER ================================================================================================================
@pytest.mark.parametrize(
    argnames="p1,_EXPECTED",
    argvalues=[
        (0, ""),
        (1, "A"),
        (26, "Z"),
        (27, "AA"),
        (28, "AB"),
    ]
)
def test__column_get_name_by_number(p1,_EXPECTED):
    test_obj_link = _ExcelProcessor.column_get_name_by_number
    result = test_obj_link(number=p1)
    assert result == _EXPECTED


pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================
pass    # ============================================================================================================


#  PYTEST INVESTIGATE =================================================================================================
@pytest.mark.parametrize(
    argnames="p1,p2,p3,p4,_EXPECTED",
    argvalues=[
        # TRIVIAL
        ("", True, True, [], True),
        (f"", True, True, [], True),
        (r"", True, True, [], True),
        (b"", True, True, [], True),
        (None, True, True, [], True),
        ((), True, True, [], True),
        ([], True, True, [], True),
        ([""], True, True, [], False),
        ({}, True, True, [], True),
        (0, True, True, [], True),
        (0.0, True, True, [], True),
    ]
)
def test__HOW_TO_PYTEST_DIRECT_ACCESS_TO_ALL_DEBUG_DATA(request, p1, p2, p3, p4, _EXPECTED):   # starichenko
    # correct only here!!!
    FUNC_LINK = UFU.value_is_blanked
    result = FUNC_LINK(source=p1, spaces_as_blank=p2, zero_as_blank=p3, addition_equivalent_list=p4)
    params_dict_additional = {}    # only if you use additional params inside!!!

    # DONT CORRECT BELOW!!!
    _PARAMS_DICT = {**request.node.callspec.params, **params_dict_additional}
    try:
        _PARAMS_DICT.pop("_EXPECTED")
    except:
        pass
    _STATUS = result == _EXPECTED
    _FUNC_TESTED = FUNC_LINK.__name__
    _FAIL_MSG = UFU.STR_PATTERN_FOR_PYTEST_FAIL_MSG.format(_FUNC_TESTED, _PARAMS_DICT, result, _EXPECTED)
    assert result == _EXPECTED, _FAIL_MSG   # you need to place here 'result == _EXPECTED' not the _STATUS!!!


@pytest.mark.parametrize(argnames="p1,p2", argvalues=[(55,55), (66,66)])
# @pytest.mark.parametrize(argnames="p1,p2", argvalues=[(1,1)])
def test__pytest_research__param(request, p1, p2):   # starichenko
    """research only"""
    print(1)
    print(2)
    print(3)

    print(f"ТЕСТКЕЙС ПЕРЕМЕННЫЕ ЛИСТ ВСЕ=[{request.fixturenames}]")     # ['request', 'p1', 'p2']
    print(f"ТЕСТКЕЙС ПЕРЕМЕННЫЕ ЛИСТ ВСЕ=[{request.node.fixturenames}]")    # ['request', 'p1', 'p2']

    print(f"ТЕСТКЕЙС ПЕРЕМЕННЫЕ СЛОВАРЬ ВСЕ=[{request.node.funcargs}]")     # {'request': <FixtureRequest for <Function test__pytest_research__param[1-1]>>, 'p1': 1, 'p2': 1}
    print(f"ТЕСТКЕЙС ПЕРЕМЕННЫЕ СЛОВАРЬ КРОМЕ REQUEST=[{request.node.callspec.params}]")    # [{'p1': 1, 'p2': 1}]

    print(f"ТЕСТКЕЙС ПЕРЕМЕННЫЕ ИНДЕКС ИЗ ПАРАМЕТРИЗАЦИИ=[{request.node.callspec.indices}]")    # {'p1': 0, 'p2': 0} - начинается с НУЛЯ!!!

    print(f"ТЕСТКЕЙС ФАЙЛ=[{request.fspath}]")  # [C:\!_HPN277SR\!!!_GD_additional\dwdm_test_system\utilities\test_func_universal.py]
    print(f"ТЕСТКЕЙС ФАЙЛ=[{request.node.fspath}]")     # [C:\!_HPN277SR\!!!_GD_additional\dwdm_test_system\utilities\test_func_universal.py]
    print(f"ТЕСТКЕЙС ИМЯ ОТЧЕТНОЕ=[{request.node.name}]")   # [test__pytest_research__param[1-1]]
    print(f"ТЕСТКЕЙС ИМЯ ФУНКЦИИ=[{request.node.originalname}]")    # [test__pytest_research__param]

    return
    print()
    print(f"request=[{request}]")
    UFU.obj_show_attr_all(request)

    print()
    print(f"request.node=[{request.node}]")
    UFU.obj_show_attr_all(request.node)

    print()
    print(f"request.node.callspec=[{request.node.callspec}]")
    UFU.obj_show_attr_all(request.node.callspec)

    print()
    print(f"request.node.keywords=[{request.node.keywords}]")
    UFU.obj_show_attr_all(request.node.keywords)

    print()
    print(f"request.node.keywords['pytestmark']=[{request.node.keywords['pytestmark']}]")
    UFU.obj_show_attr_all(request.node.keywords['pytestmark'])


    print(3)
    print(2)
    print(1)
    assert True, "ERROR"


def test__pytest_research():    # starichenko
    assert True, "ERROR1"
    assert True, "ERROR2"
    assert True, "ERROR3"


# ====================================================================================================================
