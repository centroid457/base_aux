from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_dict.m3_dict_ga1_simple import *


# =====================================================================================================================
dict_example = {
    "lowercase": "lowercase",
    # "nested": {"n1":1},
}


class Victim(DictGaAnnotRequired):
    lowercase: str


# =====================================================================================================================
def test__obj():
    # victim = DictGaAnnotRequired()
    # assert victim == {}
    #
    # victim = DictGaAnnotRequired(hello=1)
    # assert victim == {"hello": 1}

    try:
        victim = Victim()
    except:
        assert True
    else:
        assert False


def test__dict_only():
    assert LambdaTrySuccess(DictGaAnnotRequired) == True
    assert LambdaTrySuccess(DictGaAnnotRequired)

    assert LambdaTryFail(DictGaAnnotRequired) != True
    assert not LambdaTryFail(DictGaAnnotRequired)

    assert LambdaTrySuccess(DictGaAnnotRequired, **dict_example)
    assert LambdaTrySuccess(DictGaAnnotRequired, lowercase="lowercase")
    assert LambdaTrySuccess(DictGaAnnotRequired, LOWERCASE="lowercase")


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
