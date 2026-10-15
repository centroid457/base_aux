import pytest

# -----------------------------------------------------------------------------
# Частая ошибка: имя фикстуры совпадает с именем параметра в parametrize.
# Тогда pytest не сможет понять, что передавать, и тест упадёт с ошибкой.

# ======================================================================================================================
# ПАРАМЕТРИЗАЦИЯ: ОДИН ТЕСТ – МНОГО ВХОДНЫХ ДАННЫХ
# -----------------------------------------------------------------------------
# 1=ОДИНОЧНАЯ ПАРАМЕТРИЗАЦИЯ
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (10, 20, 30),
    (-1, 1, 0),
    pytest.param(100, 200, 300, id="big_numbers"),
])
def test_1__one_layer(a, b, expected):
    assert a + b == expected

# -----------------------------------------------------------------------------
# Параметризация может сочетаться с фикстурами:
@pytest.fixture
def multiplier():
    return 10

@pytest.mark.parametrize("value, expected", [
    (1, 10),
    (2, 20),
    (5, 50),
])
def test_2__multiply_by_fixture(value, expected, multiplier):
    assert value * multiplier == expected


# -----------------------------------------------------------------------------
# 2=МНОГОУРОВНЕВАЯ
"""
НАЧИНАЕТСЯ С ПОСЛЕДНЕГО И ЧЕРЕДУЕТ БОЛЕЕ ПЕРВЫЕ
============================= test session starts =============================
collecting ... collected 6 items

m1_test_4__parametrisation.py::test_3__double_layer[1_0-10-11] 
m1_test_4__parametrisation.py::test_3__double_layer[1_0-20-21] 
m1_test_4__parametrisation.py::test_3__double_layer[1_0-30-31] 
m1_test_4__parametrisation.py::test_3__double_layer[1_1-10-11] 
m1_test_4__parametrisation.py::test_3__double_layer[1_1-20-21] 
m1_test_4__parametrisation.py::test_3__double_layer[1_1-30-31] 

============================== 6 passed in 0.04s ==============================
"""
# -----------------------------------------------------------------------------
@pytest.mark.parametrize("v1, expected", [
    (10, 11),
    (20, 21),
    (30, 31),
])
@pytest.mark.parametrize("v2", [1, "1"])
def test_3__double_layer(v1, v2, expected, multiplier):
    assert v1 + int(v2) == expected


# ======================================================================================================================
