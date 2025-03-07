import pytest

from base_aux.aux_attr.m3_getattr0_echo import *


# =====================================================================================================================
def test__GetattrEcho():
    assert NestGaCls_Echo.hello == "hello"
    assert NestGaCls_Echo.Hello == "Hello"
    assert NestGaCls_Echo.ПРИВЕТ == "ПРИВЕТ"

    assert NestGaCls_Echo.hello_world == "hello_world"


def test__GetattrEchoSpace():
    assert NestGaCls_EchoSpace.hello == "hello"
    assert NestGaCls_EchoSpace.Hello == "Hello"
    assert NestGaCls_EchoSpace.ПРИВЕТ == "ПРИВЕТ"

    assert NestGaCls_EchoSpace.hello_world == "hello world"
    assert NestGaCls_EchoSpace.hello__world == "hello  world"


# =====================================================================================================================
