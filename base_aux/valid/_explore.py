import pytest


class Cls:
    A1 = 1
    A2 = 2


class Test_1:
    CLS = Cls

    @pytest.mark.parametrize(
        argnames="attr, _EXPECTED",
        argvalues=[
            (CLS.A1, 1),
            (CLS.A2, 2),
        ]
    )
    def test__1(self, attr, _EXPECTED):
        assert attr == _EXPECTED


class Cls2:
    A1 = 11
    A2 = 22


class Test_2:
    CLS = Cls2

