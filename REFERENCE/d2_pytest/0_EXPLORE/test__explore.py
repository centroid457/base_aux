# [test.py]
import pytest

from conftest import Fixtures
harvest = Fixtures.harvest

def test__1(harvest):
    assert harvest is None
