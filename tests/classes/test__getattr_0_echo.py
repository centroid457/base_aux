from typing import *
import pytest
from pytest import mark

from base_aux.funcs import *
from base_aux.classes import *


# =====================================================================================================================
def test__GetattrEcho():
    assert GetattrEcho.hello == "hello"
    assert GetattrEcho.Hello == "Hello"
    assert GetattrEcho.ПРИВЕТ == "ПРИВЕТ"

    assert GetattrEcho.hello_world == "hello_world"


def test__GetattrEchoSpace():
    assert GetattrEchoSpace.hello == "hello"
    assert GetattrEchoSpace.Hello == "Hello"
    assert GetattrEchoSpace.ПРИВЕТ == "ПРИВЕТ"

    assert GetattrEchoSpace.hello_world == "hello world"
    assert GetattrEchoSpace.hello__world == "hello  world"


# =====================================================================================================================
