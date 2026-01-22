import pytest

@pytest.fixture
def first_entry():
    return "a"

@pytest.fixture
def order():
    return []

@pytest.fixture(autouse=True)   # ЗАПУСКАЕТСЯ НА КАЖДОМ ТЕСТЕ
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]

def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]


