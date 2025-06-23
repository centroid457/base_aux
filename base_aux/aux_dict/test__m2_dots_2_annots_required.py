from base_aux.aux_callable.m2_lambda2_derivatives import Lambda_TrySuccess, Lambda_TryFail
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
    assert Lambda_TrySuccess(DictGaAnnotRequired) == True
    assert Lambda_TrySuccess(DictGaAnnotRequired)

    assert Lambda_TryFail(DictGaAnnotRequired) != True
    assert not Lambda_TryFail(DictGaAnnotRequired)

    assert Lambda_TrySuccess(DictGaAnnotRequired, **dict_example)
    assert Lambda_TrySuccess(DictGaAnnotRequired, lowercase="lowercase")
    assert Lambda_TrySuccess(DictGaAnnotRequired, LOWERCASE="lowercase")


def test__with_annots():
    assert Lambda_TryFail(Victim)
    assert not Lambda_TrySuccess(Victim)

    victim = Victim(lowercase="lowercase")
    assert victim["lowercase"] == "lowercase"

    assert Lambda_TrySuccess(Victim, **dict_example)
    assert Lambda_TrySuccess(Victim, lowercase="lowercase")
    assert Lambda_TrySuccess(Victim, LOWERCASE="lowercase")

    assert Lambda_TryFail(Victim, hello="lowercase")

    victim = Victim(lowercase="lowercase")
    assert victim == {"lowercase": "lowercase"}
    assert victim[1] == None
    assert victim.lowercase == "lowercase"


# =====================================================================================================================
