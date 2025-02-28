import pathlib
from base_aux.path2_file.m1_filepath import *
from base_aux.path2_file.m2_file import *
from base_aux.path2_file.m4_attrs_dict_loader import *
from base_aux.aux_text.m0_text_examples import *


# =====================================================================================================================
def test__File():
    data_attrs = AttrsDictTextFileLoader(text=INI_EXAMPLES.NOT_MESHED__TEXT).resolve()
    print(data_attrs)
    assert data_attrs.a0 == "00"

    data_attrs = AttrsDictTextFileLoader(text=INI_EXAMPLES.MESHED__TEXT, keypath=("s1")).resolve()
    print(data_attrs)
    assert data_attrs.a0 == "11"
    assert data_attrs.A0 == "11"


# =====================================================================================================================
