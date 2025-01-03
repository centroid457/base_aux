from typing import *
import pytest

from base_aux.attrs.m1_attr_0_init_kwargs import AttrsInitByKwArgs


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="kwargs, init_ok",
    argvalues=[
        ({1: 1}, False),

        ({"a1": 1}, True),
        ({"a1": 1, "a2": 2}, True),
    ]
)
def test__get_name(kwargs, init_ok):
    try:
        victim = AttrsInitByKwArgs(**kwargs)
    except:
        assert not init_ok
        return

    assert init_ok
    for name, value in kwargs.items():
        assert getattr(victim, name) == value


# =====================================================================================================================
