import pytest

from base_aux.aux_iter.m1_iter_aux import *
from base_aux.aux_attr.m4_kits import AttrKit_Blank
from base_aux.lambdas.m1_lambda import *
from base_aux.base_nest_dunders.m1_init2_annots1_attrs_by_kwargs import *
from base_aux.aux_values.m4_primitives import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, item, _EXPECTED",
    argvalues=[
        ((1, ), "1", 1),
        ((1, ), 1, 1),

        (("1", ), 1, "1"),
        (("1", ), "1", "1"),

        (("1", ), " 1 ", NoValue),

        (("hello", ), "HELLO", "hello"),

        ([1,], "1", 1),
        ({1,}, "1", 1),
        ({1: 11}, "1", 1),

        (AttrKit_Blank(arg1=1), "arg1", "arg1"),
        (NestInit_AnnotsAttrByKwArgs(arg1=1), "ARG1", "arg1"),
        (NestInit_AnnotsAttrByKwArgs(arg1=1), "hello", NoValue),
    ]
)
def test__item__get_original(source, item, _EXPECTED):
    victim = IterAux(source)
    func_link = victim.item__get_original
    Lambda(func_link, item).expect__check_assert(_EXPECTED)


def test__item__get_original_2():
    source = AttrKit_Blank(arg1=1)
    assert source.arg1 == 1
    assert source.ARG1 == 1

    # victim = IterAux(source)
    # func_link = victim.item__get_original
    # Lambda(func_link, item).check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, path, _EXPECTED",
    argvalues=[
        # ONE DIMENTION ===============
        ((1,),  (0,), [(0, ), 1]),
        ((1,),  ("0",), [(0, ), 1]),

        ((1,),  ("1",), [None, Exception]),
        ((1,),  (1,), [None, Exception]),

        # diff collections
        ((1,),  (0,), [(0, ), 1]),
        ([1,],  (0,), [(0, ), 1]),
        ({1,},  (0,), [Exception, Exception]),

        # list -----
        ([[1], 2], (1,), [(1, ), 2]),
        ([[1], 2], (0,), [(0, ), [1]]),
        ([[1], 2], ("0",), [(0, ), [1]]),
        ([[1], 2], (0,), [(0, ), [1]]),
        ([[1], 2], (0, 0), [(0, 0), 1]),
        ([[1], 2], (0, 1), [None, Exception]),

        # DICTS ---------
        ({1: 11}, (0,), [None, Exception]),
        ({1: 11}, (1,), [(1, ), 11]),
        ({1: 11}, ("1",), [(1, ), 11]),

        ({"hello": 1}, ("hello",), [("hello", ), 1]),
        ({"hello": 1}, ("HELLO",), [("hello", ), 1]),
        ([{"hello": 1}, 123], (0, "HELLO"), [(0, "hello"), 1]),


        # TODO: decide use or not this addressing style
        # ({"hello": [1]}, "hello", (0, "hello")),
        # hello/1

        (NestInit_AnnotsAttrByKwArgs(arg1=1), ("arg1",), [("arg1",), 1]),
        ([{"hello": NestInit_AnnotsAttrByKwArgs(arg1=1)}, 123], (0, "HELLO", "arg1"), [(0, "hello", "arg1"), 1]),
        ([{"hello": NestInit_AnnotsAttrByKwArgs(arg1=[1, 2])}, 123], (0, "HELLO", "arg1", 1), [(0, "hello", "arg1", 1), 2]),

    ]
)
def test__path__get_original__value_get(source, path, _EXPECTED):
    func_link = IterAux(source).keypath__get_original
    Lambda(func_link, *path).expect__check_assert(_EXPECTED[0])

    func_link = IterAux(source).value__get
    Lambda(func_link, *path).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
# @pytest.mark.skip
def test__valuse_set():
    data = [0,1,2,]
    assert data[1] == 1
    assert IterAux(data).value__set((5, ), 11) is False
    assert data[1] == 1
    assert data == [0,1,2,]

    data = [0,1,2,]
    assert data[1] == 1
    assert IterAux(data).value__set((1, ), 11) is True
    assert data[1] == 11
    assert data == [0,11,2,]

    data = [0,[1],2,]
    assert data[1] == [1]
    assert IterAux(data).value__set((1,0), 11) is True
    assert data[1] == [11]
    assert data == [0,[11],2,]

    data = [0,[1],2,]
    assert data[1] == [1]
    assert IterAux(data).value__set((1,0), 11) is True
    assert data[1] == [11]
    assert data == [0,[11],2,]

    data = [0,{"hello": [0,1,2,]},2,]
    assert IterAux(data).value__set((1, "hello", 1), 11) is True
    assert data == [0,{"hello": [0,11,2,]},2,]


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, variants, _EXPECTED",
    argvalues=[
        ((1, ), (), [1, 1]),
        ((1, ), (1, ), [1, None]),
        ((None, 1, ), (1, ), [1, None]),
        ((0, 1, ), (0, ), [0, 1]),
        ((None, 0, 1, ), (0, ), [0, None]),
        ((None, LAMBDA_NONE, ), (0, ), [LAMBDA_NONE, None, ]),
    ]
)
def test__get_first_is_not_none(source, variants, _EXPECTED):
    func_link = IterAux(source).get_first_is_not_none
    Lambda(func_link).expect__check_assert(_EXPECTED[0])

    func_link = lambda: IterAux(source).get_first_is_not(*variants)
    Lambda(func_link).expect__check_assert(_EXPECTED[1])


# =====================================================================================================================
