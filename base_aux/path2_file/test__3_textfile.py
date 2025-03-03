import pathlib
from base_aux.path2_file.m1_filepath import *
from base_aux.path2_file.m2_file import *
from base_aux.path2_file.m3_filetext import *


# =====================================================================================================================
text_load = "text_load"
FILEPATH = Resolve_FilePath(namefull="victim.txt").resolve()


# =====================================================================================================================
class Test__textFile:
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        FileAux(filepath=FILEPATH).delete_file()

    # -----------------------------------------------------------------------------------------------------------------
    def test__File(self):
        self.victim = FileAux(filepath=FILEPATH)

        assert self.victim.clear_file() is True
        assert self.victim.read__text() == ""
        assert self.victim.TEXT == ""
        assert self.victim.write__text(text_load) == 9
        assert self.victim.TEXT == text_load
        assert self.victim.delete_file() is True

        assert self.victim.append__lines(1, 2) == True
        assert self.victim.TEXT == "1\n2"
        assert self.victim.append__lines(3, 4) == True
        assert self.victim.TEXT == "1\n2\n3\n4"
        assert self.victim.delete_file() is True

    def test__textFile(self):
        self.victim = TextFile(filepath=FILEPATH, text=123)
        assert self.victim.write__text() == 3
        assert self.victim.TEXT == "123"
        assert self.victim.delete_file() is True


# =====================================================================================================================
