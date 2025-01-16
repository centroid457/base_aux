import pytest
from base_aux.aux_pytester.m1_pytest_aux import  PytestAux

from base_aux.funcs import *
from base_aux.aux_iter import IterAux


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
    pytest_func_tester__no_kwargs(func_link, item, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, path, _EXPECTED",
    argvalues=[
        ((1, ), "1", (1, )),
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
def test__path__get_original(source, path, _EXPECTED):
    func_link = IterAux(source).path__get_original
    pytest_func_tester__no_kwargs(func_link, path, _EXPECTED)


class Test__2:
    # -----------------------------------------------------------------------------------------------------------------
    def test__path__list(self):
        assert IterAux([[1], 2]).path__get_original([0, ]) == Explicit([0, ])
        assert self.victim(["0", ], [[1], 2]) == Explicit([0, ])

        assert self.victim([0, 0], [1]) is None
        assert self.victim([0, 0], [[1]]) == Explicit([0, 0, ])
        assert self.victim([0, 1], [[1]]) is None

    def test__value__list__single(self):
        assert self.victim(0, [1]) == Explicit([0, ])
        assert self.victim("0", [1]) == Explicit([0, ])

        assert self.victim(1, [1]) is None
        assert self.victim("1", [1]) is None

        assert self.victim(1, [1, 11]) == Explicit([1, ])
        assert self.victim("1", [1, 11]) == Explicit([1, ])

    def test__value__list__multy(self):
        assert self.victim(0, [[1], 2]) == Explicit([0, ])
        assert self.victim("0", [[1], 2]) == Explicit([0, ])

        assert self.victim("0/0", [1]) is None
        assert self.victim("0/0", [[1]]) == Explicit([0, 0, ])
        assert self.victim("0/1", [[1]]) is None

    def test__value__dict_str(self):
        assert self.victim("hello", ["hello", ]) is None

        assert self.victim("hello", {"hello": 1}) == Explicit(["hello", ])
        assert self.victim("hello", {"HELLO": 1}) == Explicit(["HELLO", ])
        assert self.victim("HELLO", {"hello": 1}) == Explicit(["hello", ])

    def test__value__dict_int(self):
        assert self.victim("1", {"1": 11, }) == Explicit(["1", ])
        assert self.victim("1", {1: 11, }) == Explicit([1, ])
        assert self.victim(1, {1: 11, }) == Explicit([1, ])




# =====================================================================================================================
class Test__3:
    @classmethod
    def setup_class(cls):
        cls.victim = IterAux().value__get
        pass

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        assert self.victim("hello", {"hello": [1]}) == Explicit([1])
        assert self.victim("hello/1", {"hello": [1]}) is None
        assert self.victim("hello/0", {"hello": [1]}) == Explicit(1)


# =====================================================================================================================
class Test__4:
    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
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
