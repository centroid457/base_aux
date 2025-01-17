import pytest

from base_aux.base_objects.m1_obj2_info import ObjectInfo
from base_aux.requirements.strings import *


# =====================================================================================================================
class Test__Cls:
    Victim: type[ReqCheckStr_Base]
    @classmethod
    def setup_class(cls):
        pass

        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "true"
            TRUE = True
            FALSE = False
            NONE = None
            NOT_EXIST: Any

            bool_if__TRUE: TYPE__RESULT_BOOL
            bool_if_not__TRUE: TYPE__RESULT_BOOL
            # ...
            raise_if__TRUE: TYPE__RESULT_RAISE
            raise_if_not__TRUE: TYPE__RESULT_RAISE
            # ...

        cls.Victim = Victim

    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__marker__not_exist(self):
        try:
            self.Victim.hello__true()
            assert False
        except:
            assert True

    def test__marker__case_sense(self):
        assert self.Victim.bool_if__true() is True
        assert self.Victim.BOOL_IF__TRUE() is True
        assert self.Victim.bool_if__TRUE() is True

    def test__marker__all_variants(self):
        assert self.Victim.bool_if__TRUE() is True
        assert self.Victim.bool_if__FALSE() is False
        assert self.Victim.bool_if__NONE() is False
        assert self.Victim.bool_if__NOT_EXIST() is False

        assert self.Victim.bool_if_not__TRUE() is False
        assert self.Victim.bool_if_not__FALSE() is True
        assert self.Victim.bool_if_not__NONE() is True
        assert self.Victim.bool_if_not__NOT_EXIST() is True

        try:
            self.Victim.raise_if__TRUE()
            assert False
        except:
            assert True
        self.Victim.raise_if__FALSE()
        self.Victim.raise_if__NONE()
        self.Victim.raise_if__NOT_EXIST()

        self.Victim.raise_if_not__TRUE()
        try:
            self.Victim.raise_if_not__FALSE()
            assert False
        except:
            assert True
        try:
            self.Victim.raise_if_not__NONE()
            assert False
        except:
            assert True
        try:
            self.Victim.raise_if_not__NOT_EXIST()
            assert False
        except:
            assert True


# =====================================================================================================================
class Test__Instance:
    Victim: type[ReqCheckStr_Base]
    @classmethod
    def setup_class(cls):
        pass

        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "true"
            TRUE = True
            FALSE = False
            NONE = None
            NOT_EXIST: Any

            bool_if__TRUE: TYPE__RESULT_BOOL
            bool_if_not__TRUE: TYPE__RESULT_BOOL
            # ...
            raise_if__TRUE: TYPE__RESULT_RAISE
            raise_if_not__TRUE: TYPE__RESULT_RAISE
            # ...

        cls.Victim = Victim

    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # TRIVIAL CASES ---------------------------------------------------------------------------------------------------
    def test__no_getter(self):
        class Victim(ReqCheckStr_Base):
            _GETTER = None
            _RAISE = False

        try:
            victim = Victim()
        except:
            assert True
        else:
            assert False

        # -----------------------
        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "true"
            _RAISE = False

        victim = Victim()

    def test__no_reqs(self):
        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "true"
            _RAISE = False

        victim = Victim()

        assert victim.check() is False
        assert victim._value_actual == "true"

        # -----------------------
        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "true"
            _RAISE = False
            FALSE = False

        victim = Victim()

        assert victim.check() is False
        assert victim._value_actual == "true"

    @pytest.mark.skip
    def test__inits(self):
        assert self.Victim(_getter=lambda: "hello", _raise=False, _meet_true=True).check() is False
        assert self.Victim(_getter=lambda: "hello", _raise=False, _meet_true=False).check() is True

        assert self.Victim(_getter=lambda: "hello", _raise=False).check("HELLO") is True
        assert self.Victim(_getter=lambda: "hello", _raise=False).bool_if__HELLO() is True

        assert self.Victim.bool_if__HELLO() is True

    # ACCEPTANCE VARIANTS ---------------------------------------------------------------------------------------------
    def test__req_met_true(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello = True
        victim = self.Victim()

        assert victim.check() is True

    def test__req_met_true__several_variants(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello1 = False
        self.Victim.hello = True
        self.Victim.hello2 = False
        victim = self.Victim()

        assert victim.check() is True

    def test__req_met_false(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello = False
        try:
            victim = self.Victim()
        except Exx_Requirement:
            assert True
        else:
            assert False

    # SETTINGS ATTRIBUTES ---------------------------------------------------------------------------------------------
    def test__set_raise(self):
        # _RAISE = True
        self.Victim._GETTER = lambda: "Hello"
        self.Victim._RAISE = True
        self.Victim.hello = False
        try:
            victim = self.Victim()
        except Exx_Requirement:
            assert True
        else:
            assert False

        # _RAISE = False
        self.Victim._RAISE = False
        victim = self.Victim()
        assert victim.check() is False

    def test__set_part(self):
        self.Victim._RAISE = False
        self.Victim._GETTER = lambda: "Hello"

        # _CHECK_FULLMATCH = True
        self.Victim._CHECK_FULLMATCH = True
        self.Victim.hell = True

        victim = self.Victim()
        # victim.hello
        assert victim.check() is False

        # _CHECK_FULLMATCH = False
        self.Victim._CHECK_FULLMATCH = False
        assert victim.check() is True

    def test__set_meet_true(self):
        class Victim(ReqCheckStr_Base):
            _GETTER = lambda: "Hello"
            _RAISE = False
            _MEET_TRUE = True

            HELLO = True

        victim = Victim()
        assert victim.check() is True

        Victim.HELLO = False
        assert victim.check() is False

        Victim._RAISE = True
        try:
            victim.check()
            assert False
        except:
            assert True

        # _MEET_TRUE = False
        Victim._RAISE = False
        Victim._MEET_TRUE = False
        Victim.HELLO = True
        assert victim.check() is True

        Victim.HELLO = False
        assert victim.check() is False

    # PARAMS ----------------------------------------------------------------------------------------------------------
    # def test__param_values(cls):
    #     cls.Victim._RAISE = False
    #     cls.Victim._GETTER = lambda: "Hello"
    #     cls.Victim.HELLO = True
    #     victim = cls.Victim()
    #
    #     assert victim.check() is True
    #     assert victim.check("hellO") is True
    #     assert victim.check(["hellO", ]) is True
    #
    #     assert victim.check("hell") is False
    #     assert victim.check(["hell", ]) is False

    # IS/ISNOT -------------------------------------------------------------------------------------------------------
    def test__check(self):
        self.Victim._RAISE = False
        self.Victim._GETTER = lambda: "Hello"
        victim = self.Victim()

        assert victim.check("hellO999") is False
        assert victim.check("hellO") is True
        assert victim.check(["hellO", ]) is True
        assert victim.check(["hellO", "hellO999"]) is True

        assert victim.check("hellO999", _reverse=True) is True
        assert victim.check("hellO", _reverse=True) is False
        assert victim.check(["hellO", ], _reverse=True) is False
        assert victim.check(["hellO", "hellO999"], _reverse=True) is False

        # getattr -------
        assert victim.bool_if__HELLO() is True
        assert victim.bool_if__HELLO999() is False
        assert self.Victim.bool_if__HELLO() is True
        assert self.Victim.bool_if__HELLO999() is False

        assert victim.bool_if_not__HELLO() is False
        assert victim.bool_if_not__HELLO999() is True
        assert self.Victim.bool_if_not__HELLO() is False
        assert self.Victim.bool_if_not__HELLO999() is True

        try:
            self.Victim.raise_if__HELLO()
        except:
            pass
        else:
            assert False

        assert self.Victim.raise_if_not__HELLO() is None

        assert self.Victim.raise_if__HELLO999() is None

        try:
            self.Victim.raise_if_not__HELLO999()
        except:
            pass
        else:
            assert False


# =====================================================================================================================
