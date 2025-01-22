from typing import *
import pytest

from base_aux.aux_dict.m2_dict_dots1_simple import *


# =====================================================================================================================
dict_example = {
    "lowercase": "lowercase",
    "nested": {"n1":1},
}


class Victim(DictDots):
    lowercase: str


# =====================================================================================================================
def test__init():
    victim = Victim()
    assert victim == {}
    assert victim[1] == None
    assert victim.lowercase == None

    victim = Victim({})
    assert victim == {}
    assert victim[1] == None
    assert victim.lowercase == None

    victim = Victim(**{})
    assert victim == {}
    assert victim[1] == None
    assert victim.lowercase == None

    victim = Victim({1:1})
    assert victim == {1:1}
    assert victim[1] == 1
    assert victim.lowercase == None

    victim = Victim(dict_example)
    assert victim == dict_example
    assert victim[1] == None
    assert victim.lowercase == "lowercase"

    victim = Victim(**dict_example)
    assert victim == dict_example
    assert victim[1] == None
    assert victim.lowercase == "lowercase"

    victim = Victim(lowercase="lowercase")
    assert victim == {"lowercase": "lowercase"}
    assert victim[1] == None
    assert victim.lowercase == "lowercase"


# ---------------------------------------------------------------------------------------------------------------------
def test__not_exist():
    victim = Victim(dict_example)
    assert victim == dict_example

    assert victim.NOT_EXIST == None
    assert victim["NOT_EXIST"] == None
    victim["NOT_EXIST"] = 1
    assert victim.not_exist == 1
    assert victim["not_exist"] == 1


# ---------------------------------------------------------------------------------------------------------------------
def test__access_get():
    victim = Victim(dict_example)
    assert victim == dict_example
    assert victim.get("lowercase") == "lowercase"
    assert victim.get("LOWERCASE") == "lowercase"


def test__access_attrs():
    victim = Victim(dict_example)
    assert victim == dict_example

    assert victim.lowercase == "lowercase"
    assert victim.LOWERCASE == "lowercase"

    victim.lowercase = 111
    assert victim.lowercase == 111
    assert victim.LOWERCASE == 111

    victim.LOWERCASE = 222
    assert victim.lowercase == 222
    assert victim.LOWERCASE == 222


def test__access_items():
    victim = Victim(dict_example)
    assert victim == dict_example

    assert victim["lowercase"] == "lowercase"
    assert victim["LOWERCASE"] == "lowercase"

    victim["lowercase"] = 111
    assert victim["lowercase"] == 111
    assert victim["LOWERCASE"] == 111

    victim["LOWERCASE"] = 222
    assert victim["lowercase"] == 222
    assert victim["LOWERCASE"] == 222
    victim["lowercase"] = "lowercase"

    assert victim[1] == None
    victim[1] = 1
    assert victim[1] == 1


def test__nested():
    victim = Victim(dict_example)

    assert victim.nested == {"n1":1}
    assert victim.nested.n1 == 1

    victim.nested.n1 = 2
    assert victim.nested.n1 != 2    # NESTED LEVELS ONLY READ ONLY!!!
    assert victim.nested.n1 == 1


# ---------------------------------------------------------------------------------------------------------------------
def test__del():
    victim = Victim()

    victim.hello = None
    assert "hello" in victim
    del victim["hello"]
    assert "hello" not in victim

    victim.hello = None
    assert "hello" in victim
    del victim.hello
    assert "hello" not in victim


def test__pop():
    victim = Victim()

    victim.hello = None
    assert "hello" in victim
    victim.pop("hello")
    assert "hello" not in victim

    victim.hello = None
    assert "hello" in victim
    victim.pop("HELLO")
    assert "hello" not in victim


def test__clear():
    victim = Victim({1:1})
    assert victim == {1:1}
    victim.clear()
    assert victim == {}


# ---------------------------------------------------------------------------------------------------------------------
def test__contain():
    victim = Victim(dict_example)
    assert victim == dict_example

    assert 1 not in victim
    assert "HELLO" not in victim
    assert "lowercase" in victim
    assert "LOWERCASE" in victim


def test__list_len_bool():
    victim = Victim()
    assert list(victim) == []
    assert len(victim) == 0
    assert bool(victim) == False
    victim[1] = 1
    assert list(victim) == [1]
    assert len(victim) == 1
    assert bool(victim) == True


def test__iter():
    dict_1 = {1:1, "hello": 2}
    victim = Victim(dict_1)
    for key1, key2 in zip(victim, dict_1):
        assert key1 == key2


def test__update():
    victim = Victim()
    victim[1] = 1
    victim.update({1:11})
    assert victim[1] == 11


# =====================================================================================================================
