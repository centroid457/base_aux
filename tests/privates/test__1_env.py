import os
import pytest
from base_aux.privates.m1_loader1_env import PrivateEnv


# =====================================================================================================================
class Test__Env:
    VALUE: str = "VALUE"
    NAME_Exists: str = "Exists"
    NAME_NotExists: str = "NotExists"

    @classmethod
    def setup_class(cls):
        while cls.NAME_Exists in os.environ:
            cls.NAME_Exists = f"{cls.NAME_Exists}_"

        while cls.NAME_NotExists in os.environ:
            cls.NAME_NotExists = f"{cls.NAME_NotExists}_"

        os.environ[cls.NAME_Exists] = cls.VALUE

        print()
        print()
        print(f"{cls.NAME_Exists=}")
        print(f"{cls.NAME_NotExists=}")
        print()
        print()

    @classmethod
    def teardown_class(cls):
        del os.environ[cls.NAME_Exists]

    def setup_method(self, method):
        self.Victim = PrivateEnv
        self.Victim._RAISE = True

    # -----------------------------------------------------------------------------------------------------------------
    def test__Exists(self):
        assert self.Victim()[self.NAME_Exists] == self.VALUE
        assert getattr(self.Victim(), self.NAME_Exists) == self.VALUE

    def test__notExists(self):
        try:
            self.Victim()[self.NAME_NotExists]
        except AttributeError:
            return
        else:
            assert False

    def test__show(self):
        # uppercase - see docstring for method!
        envs = self.Victim().get_dict(self.NAME_Exists)
        print(envs)
        assert envs.get(self.NAME_Exists.upper()) == self.VALUE


# =====================================================================================================================
