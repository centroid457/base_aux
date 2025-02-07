import pathlib
import pytest
import abc
import shutil
from tempfile import TemporaryDirectory

from base_aux.base_exceptions.m1_exceptions import *

from base_aux.privates.m4_json import *


# =====================================================================================================================
class Test__Json:
    VICTIM: type[PrivateJson] = type("Victim", (PrivateJson,), {})
    VICTIM2_FILENAME: str = f"{PrivateJson.FILENAME}2"
    VICTIM2: type[PrivateJson] = type("VICTIM2", (PrivateJson,), {"FILENAME": VICTIM2_FILENAME})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT1: str = """
{
"SEC1": {
    "name1": "value1",
    "name2": "value11"
    },
"SEC2": {
    "name1": "value2",
    "name2": "value22"
    },
"AUTH": {
    "USER": "NAME1",
    "PWD": "PWD1"
    }
}
    """
    TEXT2: str = """
{
"SEC1": {
    "name1": "value1*",
    "name2": "value11*"
    },
"SEC2": {
    "name1": "value2*",
    "name2": "value22*"
    }
}
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
        self.VICTIM = type("Victim", (PrivateJson,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateJson,), {"FILENAME": self.VICTIM2_FILENAME})

        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

        self.VICTIM.SECTION = "SEC1"
        self.VICTIM2.SECTION = "SEC1"

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
        try:
            self.VICTIM().name999
        except AttributeError:
            pass
        else:
            assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().name1 == "value1"
        assert self.VICTIM().name2 == "value11"
        try:
            self.VICTIM().name3
        except AttributeError:
            pass
        else:
            assert False

        assert self.VICTIM(_section="SEC2").name1 == "value2"
        assert self.VICTIM(_section="SEC2").name2 == "value22"
        try:
            self.VICTIM(_section="SEC2").name3
        except AttributeError:
            pass
        else:
            assert False

        try:
            self.VICTIM(_section="SEC3").name1
        except AttributeError:
            pass
        else:
            assert False

        # VICTIM2
        assert self.VICTIM2().name1 == "value1*"
        assert self.VICTIM2().name2 == "value11*"
        try:
            self.VICTIM2().name3
        except AttributeError:
            pass
        else:
            assert False

    def test__use_init(self):
        assert self.VICTIM().name1 == "value1"
        assert self.VICTIM(_filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)).name1 == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME).name1 == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").name1 == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").name2 == "value11*"

        VICTIM_obj = self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1")
        assert VICTIM_obj.name1 == "value1*"

    def test__case_sense(self):
        assert self.VICTIM().name1 == "value1"
        assert self.VICTIM().NAME1 == "value1"
        assert self.VICTIM().NamE1 == "value1"

        assert getattr(self.VICTIM(), "name1") == "value1"
        assert getattr(self.VICTIM(), "NamE1") == "value1"

        assert hasattr(self.VICTIM(), "name1")
        assert hasattr(self.VICTIM(), "Name1")

    def test__get_section(self):
        VICTIM_obj = self.VICTIM()
        assert VICTIM_obj.name1 == "value1"
        assert VICTIM_obj.name2 == "value11"

    def test__PrivateAuthJson(self):
        VICTIM_obj = PrivateAuthJson(_filepath=self.VICTIM().filepath, _section="AUTH")
        assert VICTIM_obj.USER == "NAME1"
        assert VICTIM_obj.PWD == "PWD1"

        class Cls(PrivateAuthJson):
            PWD2: str

        try:
            Cls(_filepath=self.VICTIM().filepath, _section="AUTH")
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__ABC(self):
        VICTIM_obj = PrivateAuthJson(_filepath=self.VICTIM().filepath, _section="AUTH")
        assert VICTIM_obj.USER == "NAME1"
        assert VICTIM_obj.PWD == "PWD1"

        class Cls(PrivateAuthJson, abc.ABC):
            PWD2: str

            @abc.abstractmethod
            def meth(self):
                pass

        class Cls2(Cls):
            PWD2: str

            def meth(self):
                pass

        try:
            Cls2(_filepath=self.VICTIM().filepath, _section="AUTH")
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__dict_update(self):
        victim = self.VICTIM()
        assert victim.name1 == "value1"
        victim.apply_dict({"hello": 111})

        try:
            assert victim.name1 == "value1"
        except AttributeError:
            pass
        else:
            assert False

        victim = self.VICTIM()
        assert victim.name1 == "value1"
        victim.update_dict({"hello": 111})
        assert victim.name1 == "value1"
        assert victim.hello == 111

    def test__dict_preupdate(self):
        victim = self.VICTIM()
        assert victim.name1 == "value1"
        victim.apply_dict({"hello": 11})

        assert dict(victim.DICT) == {"hello": 11}
        assert victim.hello == 11

        victim.preupdate_dict({"hello1": 2222, "hello": 2222})
        assert dict(victim.DICT) == {"hello1": 2222, "hello": 11}
        assert victim.hello == 11
        assert victim.hello1 == 2222

    def test__dict_in_init(self):
        victim = self.VICTIM(_dict={"hello": 11})
        assert dict(victim.DICT) == {"hello": 11}
        try:
            assert victim.name1 == "value1"
        except AttributeError:
            pass
        else:
            assert False
        assert victim.hello == 11


# =====================================================================================================================
