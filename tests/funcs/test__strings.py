import pytest

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.objects import *


# =====================================================================================================================
class Test__1:
    @classmethod
    def setup_class(cls):
        cls.victim = Strings().try_convert_to__elementary
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
    def test__same_value(self):
        assert self.victim(None) is None
        assert self.victim(0) == 0
        assert self.victim([]) == []
        assert self.victim({1: 1}) == {1: 1}

    def test__single__none(self):
        # single
        assert self.victim(None) is None
        assert self.victim("None") is None
        assert self.victim("null") is None

        # collects
        assert self.victim([None]) == [None]
        assert self.victim("[None]") == [None]
        assert self.victim("[null]") == [None]

        # assert self.victim("['None',]") == ['None']
        # assert self.victim("['null']") == ['None']

    def test__single__bool(self):
        assert self.victim(True) is True
        assert self.victim(False) is False

        assert self.victim("True") is True
        assert self.victim("False") is False

        assert self.victim("true") is True
        assert self.victim("false") is False

    def test__single__numbs(self):
        assert self.victim("000") == "000"
        assert self.victim("01") == "01"

        assert self.victim(0) == 0
        assert self.victim("0") == 0
        assert self.victim("10") == 10

        assert self.victim("1.0") == 1.0
        assert self.victim("1.000") == 1.0

    # iters -----------------------------------------------------------------------------------------------------------
    def test__iters1(self):
        assert self.victim("[]") == []

    def test__dicts(self):
        # INcorrect
        assert self.victim("{1: 1}") != {1: 1}      # FIXME: for dicts - use only string keys even for numbs!
        assert self.victim("{'1': 1}") != {1: 1}    # FIXME: for dicts - use only double quotes!

        # correct
        assert self.victim('{"1": 1}') == {"1": 1}

    @pytest.mark.skip
    def test__iters2(self):
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        pass


# =====================================================================================================================
