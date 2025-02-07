import pathlib
import pytest
import shutil
from tempfile import TemporaryDirectory

from base_aux.base_exceptions.m1_exceptions import *

from base_aux.privates.m3_ini import PrivateIni, PrivateAuthIni


# =====================================================================================================================
class Test__Ini:
    VICTIM: type[PrivateIni] = type("Victim", (PrivateIni,), {})
    VICTIM2_FILENAME: str = f"{PrivateIni.FILENAME}2"
    VICTIM2: type[PrivateIni] = type("VICTIM2", (PrivateIni,), {"FILENAME": VICTIM2_FILENAME})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT1: str = f"""
[DEFAULT]
name=valueDef
name0=valueDef

[SEC1]
name=value1
name1=value1

[AUTH]
USER=NAME1
PWD=PWD1
    """
    TEXT2: str = f"""
[DEFAULT]
name=valueDef2
name0=valueDef2

[SEC1]
name=value12
name1=value12
        """
    @classmethod
    def setup_class(cls):
        cls.DIRPATH.mkdir()
        cls.DIRPATH.joinpath(cls.VICTIM.FILENAME).write_text(cls.TEXT1)
        cls.DIRPATH.joinpath(cls.VICTIM2.FILENAME).write_text(cls.TEXT2)

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.DIRPATH)

    def setup_method(self, method):
        self.VICTIM = type("Victim", (PrivateIni,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateIni,), {"FILENAME": self.VICTIM2_FILENAME})
        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

    # -----------------------------------------------------------------------------------------------------------------
    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.ini"

        try:
            self.VICTIM()
        except FileNotFoundError:
            pass
        else:
            assert False

    def test__notExist_name(self):
        assert self.VICTIM().nAme == "valueDef"

        try:
            self.VICTIM().name999
        except AttributeError:
            pass
        else:
            assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().nAme == "valueDef"
        assert self.VICTIM().name0 == "valueDef"
        try:
            self.VICTIM().name1
        except AttributeError:
            pass
        else:
            assert False

        assert self.VICTIM(_section="SEC1").name == "value1"
        assert self.VICTIM(_section="SEC1").name0 == "valueDef"
        assert self.VICTIM(_section="SEC1").name1 == "value1"

        # VICTIM2
        assert self.VICTIM2().name == "valueDef2"
        assert self.VICTIM2().name0 == "valueDef2"
        try:
            self.VICTIM2().name1
        except AttributeError:
            pass
        else:
            assert False

        assert self.VICTIM2(_section="SEC1").name == "value12"
        assert self.VICTIM2(_section="SEC1").name0 == "valueDef2"
        assert self.VICTIM2(_section="SEC1").name1 == "value12"

    def test__use_init(self):
        assert self.VICTIM().name == "valueDef"
        assert self.VICTIM(_filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)).name == "valueDef2"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME).name == "valueDef2"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").name == "value12"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").name1 == "value12"

        VICTIM_obj = self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1")
        assert VICTIM_obj.name1 == "value12"

    def test__PrivateAuthIni(self):
        VICTIM_obj = PrivateAuthIni(_filepath=self.VICTIM().filepath, _section="AUTH")
        assert VICTIM_obj.USER == "NAME1"
        assert VICTIM_obj.PWD == "PWD1"

        class Cls(PrivateAuthIni):
            PWD2: str

        try:
            Cls(_filepath=self.VICTIM().filepath, _section="AUTH")
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False


# =====================================================================================================================
