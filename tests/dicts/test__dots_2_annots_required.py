from typing import *
import pytest

from base_aux.base_objects import LAMBDA_EXX

from base_aux.lambdas import *
from base_aux.dicts import *
# from base_aux.classes import *


# =====================================================================================================================
dict_example = {
    "lowercase": "lowercase",
    # "nested": {"n1":1},
}


class Victim(DictDotsAnnotRequired):
    lowercase: str


# =====================================================================================================================
def test__obj():
    victim = DictDotsAnnotRequired()
    assert victim == {}

    victim = DictDotsAnnotRequired(hello=1)
    assert victim == {"hello": 1}

    try:
        victim = Victim()
    except:
        assert True
    else:
        assert False

    # assert victim == {}
    # assert victim.annot__get_nested__dict_types() == {"lowercase": str}
    # assert victim.annot__get_not_defined() == ["lowercase", ]
    # victim.annot__raise_if_not_defined()


def test__dict_only():
    assert LambdaTrySuccess(DictDotsAnnotRequired) == True
    assert LambdaTrySuccess(DictDotsAnnotRequired)

    assert LambdaTryFail(DictDotsAnnotRequired) != True
    assert not LambdaTryFail(DictDotsAnnotRequired)

    assert LambdaTrySuccess(DictDotsAnnotRequired, **dict_example)
    assert LambdaTrySuccess(DictDotsAnnotRequired, lowercase="lowercase")
    assert LambdaTrySuccess(DictDotsAnnotRequired, LOWERCASE="lowercase")


def test__with_annots():
    assert LambdaTryFail(Victim)
    assert not LambdaTrySuccess(Victim)

    victim = Victim(lowercase="lowercase")
    assert victim["lowercase"] == "lowercase"

    assert LambdaTrySuccess(Victim, **dict_example)
    assert LambdaTrySuccess(Victim, lowercase="lowercase")
    assert LambdaTrySuccess(Victim, LOWERCASE="lowercase")

    assert LambdaTryFail(Victim, hello="lowercase")

    victim = Victim(lowercase="lowercase")
    assert victim == {"lowercase": "lowercase"}
    assert victim[1] == None
    assert victim.lowercase == "lowercase"


# =====================================================================================================================
