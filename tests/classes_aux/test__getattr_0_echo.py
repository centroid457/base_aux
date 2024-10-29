from typing import *
import pathlib

import pytest
from pytest import mark
from pytest_aux import *

from classes_aux import *


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
