import pytest

from base_aux.aux_attr.m3_getattr0_echo import *


# =====================================================================================================================
def test__GetattrEcho():
    assert GetattrClsEcho.hello == "hello"
    assert GetattrClsEcho.Hello == "Hello"
    assert GetattrClsEcho.ПРИВЕТ == "ПРИВЕТ"

    assert GetattrClsEcho.hello_world == "hello_world"


def test__GetattrEchoSpace():
    assert GetattrClsEchoSpace.hello == "hello"
    assert GetattrClsEchoSpace.Hello == "Hello"
    assert GetattrClsEchoSpace.ПРИВЕТ == "ПРИВЕТ"

    assert GetattrClsEchoSpace.hello_world == "hello world"
    assert GetattrClsEchoSpace.hello__world == "hello  world"


# =====================================================================================================================
