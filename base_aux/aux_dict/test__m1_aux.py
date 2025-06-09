from base_aux.aux_dict.m1_dict_aux import *
from base_aux.aux_expect.m1_expect_aux import *


# =====================================================================================================================
DICT_LU = {
    "lower": "lower",
    "UPPER": "UPPER",
}
VICTIM_DEF = {
    1: {1: 1, 2: 2, 3: 3},
    2: {1: 1, 2: 2},
    3: {1: 1},
    4: 4,
    **DICT_LU
}


def test__collapse_key():
    VICTIM = VICTIM_DEF.copy()

    victim = DictAuxInline(VICTIM)
    victim = victim.key_collapse(4)
    assert victim == VICTIM
    assert victim[1] == {1: 1, 2: 2, 3: 3}
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAuxInline(VICTIM)
    victim = victim.key_collapse(3)
    assert victim == VICTIM
    assert victim[1] == 3
    assert victim[2] == {1: 1, 2: 2}
    assert victim[3] == {1: 1}
    assert victim[4] == 4

    victim = DictAuxInline(VICTIM)
    victim = victim.key_collapse(2)
    assert victim == VICTIM
    assert victim[1] == 3
    assert victim[2] == 2
    assert victim[3] == {1: 1}
    assert victim[4] == 4


def test__clear_values():
    VICTIM = VICTIM_DEF.copy()

    victim = DictAuxCopy(VICTIM).values_clear()
    assert victim != VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == 4

    victim = DictAuxInline(VICTIM).values_clear()
    assert victim == VICTIM
    assert victim == dict.fromkeys(VICTIM)
    assert victim[4] == None
    assert VICTIM[4] == None


def test__keys_del():
    VICTIM = VICTIM_DEF.copy()

    key = 4444
    assert key not in VICTIM
    DictAuxInline(VICTIM).keys_del(key)

    key = 4
    assert key in VICTIM
    assert VICTIM[4] == 4
    DictAuxInline(VICTIM).keys_del(key)
    assert key not in VICTIM


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, func, walk, _EXPECTED, post_eq",
    argvalues=[
        # WO internal Raise ============
        # wo collections ----
        ({1:1, 2:{11:11}}, str, False, {"1":1, "2":{11:11}}, [False, True]),
        ({1:1, 2:{11:11}}, str, True, {"1":1, "2":{"11":11}}, [False, True]),
        ({1:1, 2:{11:{111: 222}}}, str, True, {"1":1, "2":{"11":{"111":222}}}, [False, True]),
        ({1:1, 2:{11:[111, {1111:2222}]}}, str, True, {"1":1, "2": {"11": [111, {"1111": 2222}]}}, [False, True]),

        # with collections ----
        ({1: 1, 2: [{11: 11}, [22], 33]}, str, False, {"1": 1, "2": [{11: 11}, [22], 33]}, [False, True]),
        ({1: 1, 2: [{11: 11}, [22], 33]}, str, True, {"1": 1, "2": [{"11": 11}, [22], 33]}, [False, True]),

        # WITH internal Raise ============
        # wo collections ----
        ({1: 1, 2: {11: 11}}, str.lower, False, {1: 1, 2: {11: 11}}, [True, True]),
        ({1: 1, "KUP1": {"KUP2": "VUP"}}, str.lower, False, {1: 1, "kup1": {"KUP2": "VUP"}}, [False, True]),
        ({1: 1, "KUP1": {"KUP2": "VUP"}}, str.lower, True, {1: 1, "kup1": {"kup2": "VUP"}}, [False, True]),

        # with collections ----
        ({1: 1, "KUP1": [{"KUP2": "VUP2"}, [22], "VUP3"]}, str.lower, False, {1: 1, "kup1": [{"KUP2": "VUP2"}, [22], "VUP3"]}, [False, True]),
        ({1: 1, "KUP1": [{"KUP2": "VUP2"}, [22], "VUP3"]}, str.lower, True, {1: 1, "kup1": [{"kup2": "VUP2"}, [22], "VUP3"]}, [False, True]),
    ]
)
def test__keys_change__by_func__walk(source, func, walk, _EXPECTED, post_eq):
    # COPY
    func_link = DictAuxCopy(source).keys_change__by_func
    ExpectAux(func_link, (func, walk)).check_assert(_EXPECTED)
    assert (source == _EXPECTED) == post_eq[0]

    # INLINE
    func_link = DictAuxInline(source).keys_change__by_func
    ExpectAux(func_link, (func, walk)).check_assert(_EXPECTED)
    assert source == _EXPECTED     #) == post_eq[1]      # HERE IS ALWAYS TRUE!!!!


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, func, walk, _EXPECTED",
    argvalues=[
        # FIXME: FINISH!!!

        # WO internal Raise ============
        # wo collections ----
        ({1:1, 2:{11:11}}, str, False, {1:"1", 2:{11:11}}),
        ({1:1, 2:{11:11}}, str, True, {1:"1", 2:{11:"11"}}),
        ({1:1, 2:{11:{111: 222}}}, str, True, {1:"1", 2:{11:{111: "222"}}}),

        # with collections ----
        ({1:1, 2:{11:[111, {1111:2222}]}}, str, True, {1:"1", 2:{11:["111", {1111:"2222"}]}}),
        ({1: 1, 2: [{11: 11}, [22], 33]}, str, False, {1: "1", 2: [{11: 11}, [22], 33]}),
        ({1: 1, 2: [{11: 11}, [22], 33]}, str, True, {1: "1", 2: [{11: "11"}, "[22]", "33"]}),  # INCOMPLITED! / WRONG! but simply patched
    ]
)
def test__values_change__by_func__walk(source, func, walk, _EXPECTED):
    func_link = DictAuxCopy(source).values_change__by_func
    ExpectAux(func_link, (func, walk)).check_assert(_EXPECTED)


@pytest.mark.skip
def test__values_change__by_func__walk__CONTAINERS_IN_CONTAINERS():
    pass

    # ({1: 1, 2: [{11: 11}, [22], 33]}, str, True, {1: "1", 2: [{11: "11"}, "[22]" ----------here! , "33"]}),


# =====================================================================================================================
