import pytest

from base_aux.base_inits.m3_init_attrs_by_kwargs import *


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
        victim = NestInit_AttrsByKwArgs(**kwargs)
    except:
        assert not init_ok
        return

    assert init_ok
    for name, value in kwargs.items():
        assert getattr(victim, name) == value


# =====================================================================================================================
