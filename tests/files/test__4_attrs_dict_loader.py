import pathlib
from base_aux.path2_file.m1_filepath import *
from base_aux.path2_file.m2_file import *
from base_aux.path2_file.m4_attrs_dict_loader import *
from base_aux.aux_text.m0_text_examples import *


# =====================================================================================================================
def test__File():
    data_attrs = AttrsLoader_DictTextFile(text=INI_EXAMPLES.NOT_MESHED__TEXT).resolve()
    print(data_attrs)
    assert data_attrs.a0 == "00"

    data_attrs = AttrsLoader_DictTextFile(text=INI_EXAMPLES.MESHED__TEXT, keypath=["s1", ]).resolve()
    print(data_attrs)
    assert data_attrs.a0 == "11"
    assert data_attrs.A0 == "11"


# =====================================================================================================================
EXAMPLE_PV_INI = """
[AUTH]
name=name1
pwd=pwd1
"""
EXAMPLE_PV_JSON = """
{"AUTH":
    {
        "name": "name1",
        "pwd": "pwd1",
    }
}
"""


class Test__PvFiles:
    VICTIM_INI = pathlib.Path.home().joinpath("test_pv.ini")
    VICTIM_JSON = pathlib.Path.home().joinpath("test_pv.json")
    @classmethod
    def setup_class(cls):
        pass
        FileAux(filepath=cls.VICTIM_INI).write__text(EXAMPLE_PV_INI)
        FileAux(filepath=cls.VICTIM_JSON).write__text(EXAMPLE_PV_JSON)

    @classmethod
    def teardown_class(cls):
        FileAux(filepath=cls.VICTIM_INI).delete_file()
        FileAux(filepath=cls.VICTIM_JSON).delete_file()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__ini(self):
        pv = PvLoaderIni(keypath=["auth", ], filepath=self.VICTIM_INI).resolve()

        assert pv == PvLoaderIni(keypath=["AUTH", ], filepath=self.VICTIM_INI).resolve()
        assert pv != None

        assert pv.name == "name1"
        assert pv.NAME == "name1"

        # print(f"{pv_ini}")
        # print(f"{pv_ini=}")
        # print(str(pv_ini))

    def test__json(self):
        pv = PvLoaderJson(keypath=["auth", ], filepath=self.VICTIM_JSON).resolve()

        assert pv == PvLoaderJson(keypath=["AUTH", ], filepath=self.VICTIM_JSON).resolve()
        assert pv != None

        assert pv.name == "name1"
        assert pv.NAME == "name1"


# =====================================================================================================================
class Test__PvEnv:
    VALUE: str = "VALUE"

    NAME_Exists: str = "pv_Exists"
    NAME_NotExists: str = "pv_NotExists"

    @classmethod
    def setup_class(cls):
        os.environ[cls.NAME_Exists] = cls.VALUE

    @classmethod
    def teardown_class(cls):
        for name in [cls.NAME_Exists, cls.NAME_NotExists]:
            try:
                del os.environ[name]
            except:
                pass

    # def setup_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__Exists(self):
        self.victim = PvLoaderEnv().resolve()

        assert self.victim[self.NAME_Exists.lower()] == self.VALUE
        assert self.victim[self.NAME_Exists.upper()] == self.VALUE

        assert getattr(self.victim, self.NAME_Exists) == self.VALUE
        assert getattr(self.victim, self.NAME_Exists.lower()) == self.VALUE
        assert getattr(self.victim, self.NAME_Exists.upper()) == self.VALUE

    def test__notExists(self):
        self.victim = PvLoaderEnv().resolve()

        try:
            self.victim[self.NAME_NotExists]
        except AttributeError:
            return
        else:
            assert False


# =====================================================================================================================
