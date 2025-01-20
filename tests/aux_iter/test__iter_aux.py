import pytest
from base_aux.aux_pytester.m1_pytest_aux import  PytestAux
from base_aux.aux_iter.m1_iter_aux import IterAux
from base_aux.aux_values.m1_explicit import *


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, item, _EXPECTED",
    argvalues=[
        ((1, ), "1", 1),
        ((1, ), 1, 1),

        (("1", ), 1, "1"),
        (("1", ), "1", "1"),

        (("1", ), " 1 ", None),

        (("hello", ), "HELLO", "hello"),

        ([1,], "1", 1),
        ({1,}, "1", 1),
        ({1: 11}, "1", 1),
    ]
)
def test__item__get_original(source, item, _EXPECTED):
    func_link = IterAux(source).item__get_original
    PytestAux(func_link, item).assert_check(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, path, _EXPECTED",
    argvalues=[
        # ONE DIMENTION ===============
        ((1, ), 0, (0, )),
        ((1, ), "0", (0, )),

        ((1, ), "1", None),
        ((1, ), 1, None),

        # diff collections
        ([1,], 0, (0, )),
        ({1,}, 0, Exception),

        # list -----
        ([[1], 2], 1, (1, )),
        ([[1], 2], 0, (0, )),
        ([[1], 2], ("0", ), (0, )),
        ([[1], 2], (0, ), (0, )),
        ([[1], 2], (0, 0), (0, 0)),
        ([[1], 2], (0, 1), None),

        # DICTS ---------
        ({1: 11}, 0, None),
        ({1: 11}, 1, (1, )),
        ({1: 11}, "1", (1, )),

        ({"hello": 1}, "hello", ("hello", )),
        ({"hello": 1}, "HELLO", ("hello", )),
        ([{"hello": 1}, 123], (0, "HELLO"), (0, "hello")),
    ]
)
def test__path__get_original(source, path, _EXPECTED):
    func_link = IterAux(source).path__get_original
    PytestAux(func_link, path).assert_check(_EXPECTED)


# =====================================================================================================================
@pytest.mark.skip
class Test__Old:    # TODO: decide use or not this addressing style
    @classmethod
    def setup_class(cls):
        cls.victim = IterAux().value__get
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert self.victim("hello", {"hello": [1]}) == Explicit([1])
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == Explicit(1)

    # -----------------------------------------------------------------------------------------------------------------
    def test__2(self):
        data = [0,1,2,]
        assert not IterAux(data).value__set(5, 11, )
        assert data[1] == 1
        assert data == [0,1,2,]

        data = [0,1,2,]
        assert IterAux(data).value__set(1, 11) is True
        assert data[1] == 11
        assert data == [0,11,2,]

        data = [[0],1,2,]
        assert IterAux(data).value__set("0/0", 11) is True
        assert data[0] == [11]
        assert data == [[11],1,2,]

        data = {"hello": [0,1,2,]}
        assert IterAux(data).value__set("hello", 11) is True
        assert data == {"hello": 11}

        data = {"hello": [0,1,2,]}
        assert IterAux(data).value__set("hello/1", 11) is True
        assert data == {"hello": [0,11,2,]}


# =====================================================================================================================
