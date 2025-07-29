from base_aux.base_lambdas.m1_lambda2_derivatives import *
from base_aux.aux_dict.m3_dict_ga import *


# =====================================================================================================================
dict_example = {
    "lowercase": "lowercase",
    # "nested": {"n1":1},
}


class Victim(DictIcKeys_Ga_AnnotRequired):
    lowercase: str


# =====================================================================================================================
def test__obj():
    # victim = DictIcKeys_Ga_AnnotRequired()
    # assert victim == {}
    #
    # victim = DictIcKeys_Ga_AnnotRequired(hello=1)
    # assert victim == {"hello": 1}

    try:
        victim = Victim()
    except:
        assert True
    else:
        assert False


def test__dict_only():
    assert Lambda_TrySuccess(DictIcKeys_Ga_AnnotRequired).resolve() == True
    assert Lambda_TrySuccess(DictIcKeys_Ga_AnnotRequired).resolve()

    assert Lambda_TryFail(DictIcKeys_Ga_AnnotRequired).resolve() != True
    assert not Lambda_TryFail(DictIcKeys_Ga_AnnotRequired).resolve()

    assert Lambda_TrySuccess(DictIcKeys_Ga_AnnotRequired, **dict_example).resolve()
    assert Lambda_TrySuccess(DictIcKeys_Ga_AnnotRequired, lowercase="lowercase").resolve()
    assert Lambda_TrySuccess(DictIcKeys_Ga_AnnotRequired, LOWERCASE="lowercase").resolve()


def test__with_annots():
    assert Lambda_TryFail(Victim).resolve()
    assert not Lambda_TrySuccess(Victim).resolve()

    victim = Victim(lowercase="lowercase")
    assert victim["lowercase"] == "lowercase"

    assert Lambda_TrySuccess(Victim, **dict_example).resolve()
    assert Lambda_TrySuccess(Victim, lowercase="lowercase").resolve()
    assert Lambda_TrySuccess(Victim, LOWERCASE="lowercase").resolve()

    assert Lambda_TryFail(Victim, hello="lowercase").resolve()

    victim = Victim(lowercase="lowercase")
    assert victim == {"lowercase": "lowercase"}

    # assert victim[1] == None
    assert Lambda_TryFail(lambda: victim[1]).resolve()

    assert victim.lowercase == "lowercase"


# =====================================================================================================================
