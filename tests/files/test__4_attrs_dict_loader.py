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


class Test__PV:
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
