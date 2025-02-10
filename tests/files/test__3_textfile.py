import pathlib
from base_aux.path2_file.m1_filepath import *
from base_aux.path2_file.m2_file import *


# =====================================================================================================================
text_load = "text_load"


# =====================================================================================================================
class Test_TextFile:
    def test__1(self):
        filepath = Resolve_FilePath(nameext="victim.txt").resolve()
        file = FileAux(filepath=filepath)
        assert file.clear_file() is True
        assert file.read__text() == ""
        assert file.TEXT == ""
        assert file.write__text(text_load) == 9
        assert file.TEXT == text_load
        assert file.delete_file() is True

        assert file.append__lines(1, 2) == 2
        assert file.TEXT == "1\n2"
        assert file.append__lines(3, 4) == 2
        assert file.TEXT == "1\n2\n3\n4"
        assert file.delete_file() is True


# =====================================================================================================================
