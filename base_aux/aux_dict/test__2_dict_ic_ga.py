from typing import *
import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_dict.m2_dict_ic import *
from base_aux.aux_dict.m3_dict_ga import *


# =====================================================================================================================
@pytest.mark.parametrize(argnames="VictimCls", argvalues=[DictIcKeys, DictIcKeys_Ga])
def test__universe(VictimCls):
    victim1 = VictimCls()
    victim1['NAme'] = 'VALUE'
    victim1[1] = 1

    victim2 = VictimCls(NAme='VALUE')
    victim2[1] = 1

    victim3 = VictimCls({"NAme": 'VALUE', 1: 1})

    # -------------------------------------------
    for victim in [victim1, victim2, victim3, ]:
        assert len(victim) == 2

        assert list(victim) == ["NAme", 1]

        # EQ
        assert victim == {1: 1, "naME": 'VALUE'}
        assert victim == {"naME": 'VALUE', 1: 1}

        assert victim != {"naME": 'VALUE', 1: 11}
        assert victim != {"naME": 'VALUE', 11: 1}
        assert victim != {"naME": 'VALUE2', 1: 1}
        assert victim != {"naME2": 'VALUE', 1: 1}

        # CONTAIN
        assert 'naME' in victim
        assert 1 in victim
        assert 0 not in victim

        # ACCESS
        Lambda(lambda: victim[0]).expect__check_assert(Exception)   # keep original behaviour - maybe need switch to None???
        Lambda(lambda: victim.get(0)).expect__check_assert(None)

        assert victim[1] == 1
        assert victim.get(1) == 1
        assert victim['name'] == "VALUE"
        assert victim['NAME'] == "VALUE"
        assert victim.get('NAME') == "VALUE"

        # update
        len0 = len(victim)
        victim['name'] = 'VALUE2'
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE2"

        victim['NAME'] = 'VALUE3'
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE3"

        victim.update({'NaMe': 'VALUE4'})
        assert len(victim) == len0
        assert victim['name'] == victim['NAME'] == "VALUE4"

        assert list(victim) == ["NAme", 1]

        # del ------
        try:
            del victim['name222']
        except:
            assert True
        else:
            assert False

        del victim['name']
        assert list(victim) == [1, ]
        victim['NAme'] = 'VALUE'

        # pop ------
        try:
            victim.pop('name222')
        except:
            assert True
        else:
            assert False

        assert victim.pop('name') == "VALUE"
        assert list(victim) == [1, ]
        # victim['NAme'] = 'VALUE'


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, keys_all_str, _EXPECTED",
    argvalues=[
        (dict(), True, []),
        (dict(attr1=1), True, ["attr1", ]),
        (dict(ATTR1=1), True, ["ATTR1", ]),
        ({1:1}, False, [1, ]),
    ]
)
@pytest.mark.parametrize(argnames="VictimClsPair", argvalues=[(DictIcKeys, DictIc_LockedKeys), (DictIcKeys_Ga, DictIc_LockedKeys_Ga)])
def test__keys(VictimClsPair, source, keys_all_str, _EXPECTED):
    Lambda(list(VictimClsPair[0](source))).expect__check_assert(_EXPECTED)
    Lambda(list(VictimClsPair[1](source))).expect__check_assert(_EXPECTED)

    if not keys_all_str:
        return

    Lambda(list(VictimClsPair[0](**source))).expect__check_assert(_EXPECTED)
    Lambda(list(VictimClsPair[1](**source))).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, key, keys_all_str, _EXPECTED",
    argvalues=[
        (dict(), "attr1", True, None),
        (dict(attr1=1), "attr1", True, "attr1"),
        (dict(attr1=1), "ATTR1", True, "attr1"),
        (dict(ATTR1=1), "ATTR1", True, "ATTR1"),
        (dict(attr1=1), "hello", True, None),

        (dict(attr1=1), 0, True, None),
        ({1:1}, 0, False, None),
        ({1:1}, 1, False, 1),
    ]
)
@pytest.mark.parametrize(argnames="VictimClsPair", argvalues=[(DictIcKeys, DictIc_LockedKeys), (DictIcKeys_Ga, DictIc_LockedKeys_Ga)])
def test__key__get_original(VictimClsPair, source, key, keys_all_str, _EXPECTED):
    Lambda(VictimClsPair[0](source).key__get_original(key)).expect__check_assert(_EXPECTED)
    Lambda(VictimClsPair[1](source).key__get_original(key)).expect__check_assert(_EXPECTED)

    if not keys_all_str:
        return

    Lambda(VictimClsPair[0](**source).key__get_original(key)).expect__check_assert(_EXPECTED)
    Lambda(VictimClsPair[1](**source).key__get_original(key)).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, key, keys_all_str, _EXPECTED",
    argvalues=[
        (dict(attr1=1), "attr1", True, [None, None]),
        (dict(attr1=1), "ATTR1", True, [None, None]),
        (dict(ATTR1=1), "ATTR1", True, [None, None]),
        (dict(attr1=1), "hello", True, [None, Exception]),

        (dict(attr1=1), 0, False, [None, Exception]),
        ({1:1}, 0, False, [None, Exception]),
        ({1:1}, 1, False, [None, None]),
    ]
)
@pytest.mark.parametrize(argnames="VictimClsPair", argvalues=[(DictIcKeys, DictIc_LockedKeys), (DictIcKeys_Ga, DictIc_LockedKeys_Ga)])
def test__si_update(VictimClsPair, source, key, keys_all_str, _EXPECTED):
    # -------------------------------------------------
    victim = VictimClsPair[0](source)
    Lambda(victim.update({key: 11})).expect__check_assert(_EXPECTED[0])
    Lambda(victim.get(key)).expect__check_assert(11)

    victim[key] = 111
    Lambda(victim.get(key)).expect__check_assert(111)

    if keys_all_str:
        Lambda(victim.update(**{key: 1111})).expect__check_assert(_EXPECTED[0])
        Lambda(victim.get(key)).expect__check_assert(1111)

        # kwargs out
        Lambda(dict(**VictimClsPair[0](source))).expect__check_assert(source)
        Lambda(dict(**VictimClsPair[1](source))).expect__check_assert(source)

    # -------------------------------------------------
    victim = VictimClsPair[1](source)
    Lambda(lambda: victim.update({key: 2})).expect__check_assert(_EXPECTED[1])

    if _EXPECTED[1] == Exception:
        assert key not in victim

        # ---------------
        try:
            victim[key] = 123
        except:
            pass
        else:
            assert False
        Lambda(victim.get(key)).expect__check_assert(None)

        # ---------------
        try:
            victim.update({key: 123})
        except:
            pass
        else:
            assert False
        Lambda(victim.get(key)).expect__check_assert(None)

    else:
        assert key in victim

        # ---------------
        Lambda(victim.update({key: 11})).expect__check_assert(_EXPECTED[1])
        Lambda(victim.get(key)).expect__check_assert(11)

        victim[key] = 111
        Lambda(victim.get(key)).expect__check_assert(111)


    # if not keys_all_str:
    #     return
    #
    # Lambda(VictimClsPair[0](**source).key__get_original(key)).expect__check_assert(_EXPECTED)
    # Lambda(VictimClsPair[1](**source).key__get_original(key)).expect__check_assert(_EXPECTED)


# =====================================================================================================================
