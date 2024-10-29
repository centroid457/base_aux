import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
import abc

from annot_attrs import (
    Exx__AnnotNotDefined,
)
from private_values import (
    PrivateAuto,
    PrivateEnv, PrivateCsv, PrivateIni, PrivateJson,
    PrivateAuthIni, PrivateAuthJson,
    Exx__FileNotExists,
)


# =====================================================================================================================
# TODO: merge Csv/Ini/Json tests via parametrisation


# =====================================================================================================================
class Test__Env:
    VICTIM: Type[PrivateEnv] = type("VICTIM", (PrivateEnv,), {})

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
        self.VICTIM = type("VICTIM", (PrivateEnv,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__Exists(self):
        assert self.VICTIM()[self.NAME_Exists] == self.VALUE
        assert getattr(self.VICTIM(), self.NAME_Exists) == self.VALUE

    def test__notExists(self):
        try:
            self.VICTIM()[self.NAME_NotExists]
        except Exx__AnnotNotDefined:
            return
        else:
            assert False

    def test__show(self):
        # uppercase - see docstring for method!
        envs = self.VICTIM().get_dict(self.NAME_Exists)
        print(envs)
        assert envs.get(self.NAME_Exists.upper()) == self.VALUE


# =====================================================================================================================
class Test__Csv:
    VICTIM: Type[PrivateCsv] = type("VICTIM", (PrivateCsv,), {})
    VICTIM2_FILENAME: str = f"{PrivateCsv.FILENAME}2"
    VICTIM2: Type[PrivateCsv] = type("VICTIM2", (PrivateCsv,), {"FILENAME": VICTIM2_FILENAME})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT1: str = f"""
hello

:world
name:111
name1:111
    """
    TEXT2: str = f"""

name:222
name2:222
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
        self.VICTIM = type("VICTIM", (PrivateCsv,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateCsv,), {"FILENAME": self.VICTIM2_FILENAME})
        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

    # -----------------------------------------------------------------------------------------------------------------
    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.csv"

        try:
            self.VICTIM()
        except Exx__FileNotExists:
            pass
        else:
            assert False

    def test__notExist_name(self):
        assert self.VICTIM().nAme == "111"

        try:
            self.VICTIM().name999
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__use_init(self):
        assert self.VICTIM().name == "111"
        assert self.VICTIM(_filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)).name == "222"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME).name == "222"

        assert self.VICTIM(_text="name11:11").name11 == "11"

        self.VICTIM.SEPARATOR = "="
        assert self.VICTIM(_text="name11=11").name11 == "11"


# =====================================================================================================================
class Test__Ini:
    VICTIM: Type[PrivateIni] = type("VICTIM", (PrivateIni,), {})
    VICTIM2_FILENAME: str = f"{PrivateIni.FILENAME}2"
    VICTIM2: Type[PrivateIni] = type("VICTIM2", (PrivateIni,), {"FILENAME": VICTIM2_FILENAME})
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
        self.VICTIM = type("VICTIM", (PrivateIni,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateIni,), {"FILENAME": self.VICTIM2_FILENAME})
        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

    # -----------------------------------------------------------------------------------------------------------------
    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.ini"

        try:
            self.VICTIM()
        except Exx__FileNotExists:
            pass
        else:
            assert False

    def test__notExist_name(self):
        assert self.VICTIM().nAme == "valueDef"

        try:
            self.VICTIM().name999
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().nAme == "valueDef"
        assert self.VICTIM().name0 == "valueDef"
        try:
            self.VICTIM().name1
        except Exx__AnnotNotDefined:
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
        except Exx__AnnotNotDefined:
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
class Test__Json:
    VICTIM: Type[PrivateJson] = type("VICTIM", (PrivateJson,), {})
    VICTIM2_FILENAME: str = f"{PrivateJson.FILENAME}2"
    VICTIM2: Type[PrivateJson] = type("VICTIM2", (PrivateJson,), {"FILENAME": VICTIM2_FILENAME})
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
        self.VICTIM = type("VICTIM", (PrivateJson,), {})
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
        except Exx__FileNotExists:
            pass
        else:
            assert False

    def test__notExist_name(self):
        try:
            self.VICTIM().name999
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().name1 == "value1"
        assert self.VICTIM().name2 == "value11"
        try:
            self.VICTIM().name3
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

        assert self.VICTIM(_section="SEC2").name1 == "value2"
        assert self.VICTIM(_section="SEC2").name2 == "value22"
        try:
            self.VICTIM(_section="SEC2").name3
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

        try:
            self.VICTIM(_section="SEC3").name1
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

        # VICTIM2
        assert self.VICTIM2().name1 == "value1*"
        assert self.VICTIM2().name2 == "value11*"
        try:
            self.VICTIM2().name3
        except Exx__AnnotNotDefined:
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
        except Exx__AnnotNotDefined:
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

        assert dict(victim.dict) == {"hello": 11}
        assert victim.hello == 11

        victim.preupdate_dict({"hello1": 2222, "hello": 2222})
        assert dict(victim.dict) == {"hello1": 2222, "hello": 11}
        assert victim.hello == 11
        assert victim.hello1 == 2222

    def test__dict_in_init(self):
        victim = self.VICTIM(_dict={"hello": 11})
        assert dict(victim.dict) == {"hello": 11}
        try:
            assert victim.name1 == "value1"
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False
        assert victim.hello == 11


# =====================================================================================================================
class Test__Auto:
    VICTIM: Type[PrivateAuto] = type("VICTIM", (PrivateAuto,), {})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT0: str = f"""
name1=ini1
name2=ini2
    """
    TEXT1: str = f"""
[SEC1111]
name1=ini1
name2=ini2

[SEC1110]
name1=ini1
name2=ini2

[SEC1100]
name1=ini1
name2=ini2

[SEC1000]
name1=ini1

[SEC0000]
    """
    TEXT2: str = """
{
"SEC1111": {
    "name1": "json1",
    "name2": "json2"
    },
"SEC0011": {
    "name1": "json1",
    "name2": "json2"
    },
"SEC1110": {
    "name1": "json1"
    },
"SEC0000": {
    }
}
    """

    @classmethod
    def setup_class(cls):
        cls.DIRPATH.mkdir()
        cls.DIRPATH.joinpath(PrivateIni.FILENAME).write_text(cls.TEXT1)
        cls.DIRPATH.joinpath(PrivateJson.FILENAME).write_text(cls.TEXT2)

        os.environ["name1"] = "env1"
        os.environ["name2"] = "env2"

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.DIRPATH)

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (PrivateAuto,), {})
        self.VICTIM.DIRPATH = self.DIRPATH

    # -----------------------------------------------------------------------------------------------------------------
    def test__auto(self):
        class Victim(self.VICTIM):
            name1: str
            name2: str

        assert Victim(_section="SEC1111").name1 == "json1"
        assert Victim(_section="SEC0011").name1 == "json1"

        assert Victim(_section="SEC1110").name1 == "ini1"
        assert Victim(_section="SEC1100").name1 == "ini1"

        assert Victim(_section="SEC1000").name1 == "env1"
        assert Victim(_section="SEC0000").name1 == "env1"

        class Victim(self.VICTIM):
            name1: str
            name200: str
        try:
            Victim(_section="SEC0000")
        except Exx__AnnotNotDefined:
            pass
        else:
            assert False

    def test__str(self):
        class Victim(self.VICTIM):
            name1: str
            name2: str

        obj = Victim(_section="SEC1111")
        assert "pv.ini" not in str(obj)
        assert "pv.json" in str(obj)
        assert "name1" in str(obj)
        assert "json1" in str(obj)


# =====================================================================================================================
class Test__RAISE:

    @pytest.mark.parametrize(argnames="VictimBase", argvalues=[PrivateEnv, PrivateIni, PrivateJson])
    def test__raise(self, VictimBase):

        class Victim1(VictimBase):
            attr1: str

        try:
            Victim1()
        except:
            pass
        else:
            assert False


# =====================================================================================================================
