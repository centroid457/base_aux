import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory

from base_aux.base_statics.m2_exceptions import *

from base_aux.privates.m1_env import PrivateEnv
from base_aux.privates.m3_ini import PrivateIni
from base_aux.privates.m4_json import PrivateJson
from base_aux.privates.m5_auto import PrivateAuto


# =====================================================================================================================
# TODO: merge Csv/Ini/Json tests via parametrisation + SEPARATE TESTS ON FILES


# =====================================================================================================================
class Test__Auto:
    VICTIM: type[PrivateAuto] = type("Victim", (PrivateAuto,), {})
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
        self.VICTIM = type("Victim", (PrivateAuto,), {})
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
        except Exx__NotExists:
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
            assert False
        except:
            pass


# =====================================================================================================================
