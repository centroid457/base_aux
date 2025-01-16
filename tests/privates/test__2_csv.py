import pathlib
import pytest
import shutil

from tempfile import TemporaryDirectory
from base_aux.privates.attr_loader__2_csv import PrivateCsv
from base_aux.privates.static import Exx__FileNotExists


# =====================================================================================================================
class Test__Csv:
    VICTIM: type[PrivateCsv] = type("Victim", (PrivateCsv,), {})
    VICTIM2_FILENAME: str = f"{PrivateCsv.FILENAME}2"
    VICTIM2: type[PrivateCsv] = type("VICTIM2", (PrivateCsv,), {"FILENAME": VICTIM2_FILENAME})
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
        self.VICTIM = type("Victim", (PrivateCsv,), {})
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
        except AttributeError:
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
