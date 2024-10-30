import pytest

from base_aux.funcs import *
from base_aux.classes import *


# =====================================================================================================================
class Test__BreederStrStack:
    @classmethod
    def setup_class(cls):
        class BreederStrStack_Example(BreederStrStack):
            name0: int = 0
            name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")

        cls.victim = BreederStrStack_Example()
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
    @pytest.mark.parametrize(
        argnames="index_start",
        argvalues=[
            None,

            -2,
            -1,
            0,
            1,
            2,
        ]
    )
    def test__index_start(self, index_start):
        class Victim(BreederStrStack):
            _INDEX_START = index_start
            name0: int = None
            name1: int | None = None
            series23: BreederStrSeries = BreederStrSeries(None, 2, "series23_%s")
            series45: BreederStrSeries = BreederStrSeries(None, 2, "series45_%s")
            name6: None = None

        victim = Victim()

        index_start = index_start or 0
        assert victim[index_start +0] == "name0"
        assert victim[index_start +1] == "name1"
        assert victim[index_start +2] == "series23_1"
        assert victim[index_start +3] == "series23_2"
        assert victim[index_start +4] == "series45_1"
        assert victim[index_start +5] == "series45_2"
        assert victim[index_start +6] == "name6"

    def test__index_start__exx_overlayd(self):
        class Victim(BreederStrStack):
            name0: int = None
            name1: int | None = 0
            series23: BreederStrSeries = BreederStrSeries(None, 2, "series23_%s")
            series45: BreederStrSeries = BreederStrSeries(None, 2, "series45_%s")
            name6: None = None

        try:
            victim = Victim()
            assert False
        except:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__index__auto(self):
        class Victim(BreederStrStack):
            name0: int = 0
            name1: int | None = None
            series23: BreederStrSeries = BreederStrSeries(None, 2, "series23_%s")
            series45: BreederStrSeries = BreederStrSeries(None, 2, "series45_%s")
            name6: None = None

        victim = Victim()
        assert victim[0] == "name0"
        assert victim[1] == "name1"
        assert victim[2] == "series23_1"
        assert victim[3] == "series23_2"
        assert victim[4] == "series45_1"
        assert victim[5] == "series45_2"
        assert victim[6] == "name6"

    def test__index__break_order(self):
        class Victim(BreederStrStack):
            name0: int = 0
            name2: int = 2
            name1: int = 1

        victim = Victim()
        assert victim[0] == "name0"
        assert victim[1] == "name1"
        assert victim[2] == "name2"

        assert victim._DATA == {
            0: "name0",
            1: "name1",
            2: "name2",
        }

    # -----------------------------------------------------------------------------------------------------------------
    def test__exx_1__overlayd_1(self):
        class Victim(BreederStrStack):
            name0: int = 0
            name1: int = 1
            name2: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")

        try:
            victim = Victim()
            assert False
        except:
            pass

    def test__exx_1__overlayd_2(self):
        class Victim(BreederStrStack):
            name0: int = 0
            name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(1, 2, "%s")

        try:
            victim = Victim()
            assert False
        except:
            pass

    def test__exx_1__skipped_1(self):
        class BreederStrStack_Example2(BreederStrStack):
            name0: int = 0
            name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")
            TAIL2: BreederStrSeries = BreederStrSeries(20, 2, "%s")

        try:
            victim = BreederStrStack_Example2()
            assert False
        except:
            pass

    def test__exx_1__skipped_2(self):
        class Victim(BreederStrStack):
            name0: int = 0
            # name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")

        try:
            victim = Victim()
            assert False
        except:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def test_1__main_1__getitem(self):
        assert self.victim[0] == "name0"
        assert self.victim[1] == "name1"
        assert self.victim[2] == "1"
        assert self.victim[3] == "2"
        try:
            assert self.victim[4]
            assert False
        except:
            pass

        assert self.victim["name0"] == 0
        assert self.victim["name1"] == 1
        assert self.victim["1"] == 2
        assert self.victim["2"] == 3
        try:
            assert self.victim["3"]
            assert False
        except:
            pass

    def test_1__main_2__contain(self):
        assert 0 in self.victim
        assert 1 in self.victim
        assert 2 in self.victim
        assert 3 in self.victim
        assert 4 not in self.victim
        assert 5 not in self.victim

        assert "name0" in self.victim
        assert "name1" in self.victim
        assert "attr11111" not in self.victim

        assert "0" not in self.victim
        assert "1" in self.victim
        assert "2" in self.victim
        assert "3" not in self.victim
        assert "4" not in self.victim
        assert "5" not in self.victim

    def test_2__sub_2__getitem(self):
        try:
            assert self.victim.TAIL[0]
            assert False
        except:
            pass
        assert self.victim.TAIL[1] == "1"
        assert self.victim.TAIL[2] == "2"
        try:
            assert self.victim[3]
            assert False
        except:
            pass

        # 2--------
        try:
            assert self.victim.TAIL["0"]
            assert False
        except:
            pass
        assert self.victim.TAIL["1"] == 1
        assert self.victim.TAIL["2"] == 2
        try:
            assert self.victim.TAIL["3"]
            assert False
        except:
            pass

    def test_2__sub_2__contain(self):
        assert 0 not in self.victim.TAIL
        assert 1 not in self.victim.TAIL
        assert 2 in self.victim.TAIL
        assert 3 in self.victim.TAIL
        assert 4 not in self.victim.TAIL
        assert 5 not in self.victim.TAIL

        assert "0" not in self.victim.TAIL
        assert "1" in self.victim.TAIL
        assert "2" in self.victim.TAIL
        assert "3" not in self.victim.TAIL
        assert "4" not in self.victim.TAIL
        assert "5" not in self.victim.TAIL

    # -----------------------------------------------------------------------------------------------------------------
    def test__count(self):
        class Victim(BreederStrStack):
            name0: int = 0
            name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")

        assert Victim().count() == 4

        class Victim(BreederStrStack):
            name0: int = 0
            name1: int = 1
            TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")
            TAIL2: BreederStrSeries = BreederStrSeries(4, 2, "%s")

        assert Victim().count() == 6


# =====================================================================================================================
