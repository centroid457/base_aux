import pytest

from base_aux.aux_text.m3_parser1_cmd_args_kwargs import *


# =====================================================================================================================
class Test__LineParsed:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (CmdArgsKwargsParser,), {})

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__lowercase(self):
        victim = self.Victim("")
        assert victim.SOURCE == ""
        assert victim.PREFIX == ""
        assert victim.CMD == ""
        assert victim.ARGS == []
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 0

        victim = self.Victim("hello")
        assert victim.SOURCE == "hello"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == []
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 0

        victim = self.Victim("HELLO")
        assert victim.SOURCE == "HELLO"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == []
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 0

    def test__args_kwargs(self):
        victim = self.Victim("HELLO CH")
        assert victim.SOURCE == "HELLO CH"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == ["ch", ]
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 1
        assert victim.KWARGS_count() == 0

        victim = self.Victim("HELLO CH 1")
        assert victim.SOURCE == "HELLO CH 1"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == ["ch", "1", ]
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 2
        assert victim.KWARGS_count() == 0

        victim = self.Victim("HELLO CH=1")
        assert victim.SOURCE == "HELLO CH=1"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 1

        victim = self.Victim("HELLO CH1 CH2=2    ch3=3  ch4")
        assert victim.SOURCE == "HELLO CH1 CH2=2    ch3=3  ch4"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == ["ch1", "ch4"]
        assert victim.KWARGS == {"ch2": "2", "ch3": "3"}
        assert victim.ARGS_count() == 2
        assert victim.KWARGS_count() == 2

    def test__kwargs_spaces(self):
        victim = self.Victim("CH =  1")
        assert victim.SOURCE == "CH =  1"
        assert victim.PREFIX == ""
        assert victim.CMD == ""
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 1

        victim = self.Victim("hello CH =  1")
        assert victim.SOURCE == "hello CH =  1"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 1

        victim = self.Victim("hello CH ===  1")
        assert victim.SOURCE == "hello CH ===  1"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 1

    def test__kwargs_only(self):
        victim = self.Victim("CH=1")
        assert victim.SOURCE == "CH=1"
        assert victim.PREFIX == ""
        assert victim.CMD == ""
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 1

        victim = self.Victim("CH=1 ch2=2")
        assert victim.SOURCE == "CH=1 ch2=2"
        assert victim.PREFIX == ""
        assert victim.CMD == ""
        assert victim.ARGS == []
        assert victim.KWARGS == {"ch": "1", "ch2": "2"}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 2

    def test__prefix(self):
        victim = self.Victim("HELLO CH 1", prefix_expected="HELLO")
        assert victim.SOURCE == "HELLO CH 1"
        assert victim.PREFIX == "hello"
        assert victim.CMD == "ch"
        assert victim.ARGS == ["1", ]
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 1
        assert victim.KWARGS_count() == 0

        victim = self.Victim("HELLO CH 1", prefix_expected="HELLO CH 1")
        assert victim.SOURCE == "HELLO CH 1"
        assert victim.PREFIX == "hello ch 1"
        assert victim.CMD == ""
        assert victim.ARGS == []
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 0
        assert victim.KWARGS_count() == 0

        victim = self.Victim("HELLO CH 1", prefix_expected="HELLO123")
        assert victim.SOURCE == "HELLO CH 1"
        assert victim.PREFIX == ""
        assert victim.CMD == "hello"
        assert victim.ARGS == ["ch", "1", ]
        assert victim.KWARGS == {}
        assert victim.ARGS_count() == 2
        assert victim.KWARGS_count() == 0


# =====================================================================================================================
