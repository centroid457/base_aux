import pytest

from _DEPRECATED.m1_strings import *


# =====================================================================================================================
class Test__Cls:
    Victim: type[Base_ReqCheckStr]
    @classmethod
    def setup_class(cls):
        pass

        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "true"
            TRUE = True
            FALSE = False
            NONE = None
            NOT_EXIST: Any

            bool_if__TRUE: TYPING.CALLABLE__BOOL_NONE
            bool_if_not__TRUE: TYPING.CALLABLE__BOOL_NONE
            # ...
            raise_if__TRUE: TYPING.CALLABLE__RAISE_NONE
            raise_if_not__TRUE: TYPING.CALLABLE__RAISE_NONE
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
        except:
            pass
        else:
            assert False

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
        except:
            pass
        else:
            assert False

        self.Victim.raise_if__FALSE()
        self.Victim.raise_if__NONE()
        self.Victim.raise_if__NOT_EXIST()

        self.Victim.raise_if_not__TRUE()
        try:
            self.Victim.raise_if_not__FALSE()
        except:
            pass
        else:
            assert False

        try:
            self.Victim.raise_if_not__NONE()
        except:
            pass
        else:
            assert False

        try:
            self.Victim.raise_if_not__NOT_EXIST()
        except:
            pass
        else:
            assert False


# =====================================================================================================================
class Test__Instance:
    Victim: type[Base_ReqCheckStr]
    # @classmethod
    # def setup_class(cls):
    #     pass
    #
    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()

    def setup_method(self, method):
        pass

        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "true"
            TRUE = True
            FALSE = False
            NONE = None
            NOT_EXIST: Any

            bool_if__TRUE: TYPING.CALLABLE__BOOL_NONE
            bool_if_not__TRUE: TYPING.CALLABLE__BOOL_NONE
            # ...
            raise_if__TRUE: TYPING.CALLABLE__RAISE_NONE
            raise_if_not__TRUE: TYPING.CALLABLE__RAISE_NONE
            # ...

        self.Victim = Victim

    # def teardown_method(self, method):
    #     pass

    # TRIVIAL CASES ---------------------------------------------------------------------------------------------------
    def test__no_getter(self):
        class Victim(Base_ReqCheckStr):
            _GETTER = None
            _RAISE = False

        try:
            victim = Victim()
        except:
            pass
        else:
            assert False

        # -----------------------
        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "true"
            _RAISE = False

        victim = Victim()

    def test__no_reqs(self):
        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "true"
            _RAISE = False

        victim = Victim()

        assert victim.check__wo_raise() is False
        assert victim._value_actual == "true"

        # -----------------------
        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "true"
            _RAISE = False
            FALSE = False

        victim = Victim()

        assert victim.check__wo_raise() is False
        assert victim._value_actual == "true"

    @pytest.mark.skip
    def test__inits(self):
        assert self.Victim(_getter=lambda: "hello", _meet_true=True).check__w_raise() is False
        assert self.Victim(_getter=lambda: "hello", _meet_true=False).check__w_raise() is True

        assert self.Victim(_getter=lambda: "hello").check__w_raise("HELLO") is True
        assert self.Victim(_getter=lambda: "hello").bool_if__HELLO() is True

        assert self.Victim.bool_if__HELLO() is True

    # ACCEPTANCE VARIANTS ---------------------------------------------------------------------------------------------
    def test__req_met_true(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello = True
        victim = self.Victim()

        assert victim.check__w_raise() is True

    def test__req_met_true__several_variants(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello1 = False
        self.Victim.hello = True
        self.Victim.hello2 = False
        victim = self.Victim()

        assert victim.check__w_raise() is True

    def test__req_met_false(self):
        self.Victim._GETTER = lambda: "Hello"
        self.Victim.hello = False
        try:
            victim = self.Victim().check__w_raise()
            assert False
        except Exx__Expected:
            assert True

    # SETTINGS ATTRIBUTES ---------------------------------------------------------------------------------------------
    def test__set_raise(self):
        # _RAISE = True
        self.Victim._GETTER = lambda: "Hello"
        self.Victim._RAISE = True
        self.Victim.hello = False
        try:
            victim = self.Victim().check__w_raise()
            assert False
        except Exx__Expected:
            assert True

        # _RAISE = False
        self.Victim._RAISE = False
        victim = self.Victim()
        assert victim.check__wo_raise() is False

    def test__set_part(self):
        self.Victim._RAISE = False
        self.Victim._GETTER = lambda: "Hello"

        # _VALIDATOR = True
        self.Victim._VALIDATOR = True
        self.Victim.hell = True

        victim = self.Victim()
        # victim.hello
        assert victim.check__wo_raise() is False

    def test__set_meet_true(self):
        class Victim(Base_ReqCheckStr):
            _GETTER = lambda: "Hello"
            _MEET_TRUE = True

            HELLO = True

        victim = Victim()
        assert victim.check__wo_raise() is True

        Victim.HELLO = False
        assert victim.check__wo_raise() is False

        Victim._RAISE = True
        try:
            victim.check__w_raise()
        except:
            pass
        else:
            assert False

        # _MEET_TRUE = False
        Victim._RAISE = False
        Victim._MEET_TRUE = False
        Victim.HELLO = True
        assert victim.check__wo_raise() is True

        Victim.HELLO = False
        assert victim.check__wo_raise() is False

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

        assert victim.check__wo_raise("hellO999") is False
        assert victim.check__wo_raise("heLLO") is True
        assert victim.check__wo_raise(["hellO", ]) is True
        assert victim.check__wo_raise(["hellO", "hellO999"]) is True

        assert victim.check__wo_raise("hellO999", _reverse=True) is True
        assert victim.check__wo_raise("hellO", _reverse=True) is False
        assert victim.check__wo_raise(["hellO", ], _reverse=True) is False
        assert victim.check__wo_raise(["hellO", "hellO999"], _reverse=True) is False

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
