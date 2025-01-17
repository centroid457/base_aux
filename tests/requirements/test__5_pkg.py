import pytest

from base_aux.aux_pytester.m1_pytest_aux import PytestAux

from base_aux.requirements.m1_pkgs import *


# =====================================================================================================================
DUMMY_MODULE_NAME = "dummy-module"


# =====================================================================================================================
@pytest.mark.skipif(condition=False, reason="too long")
class Test_Pkg:
    @classmethod
    def setup_class(cls):
        Packages().upgrade_pip()

    def setup_method(self, method):
        self.Victim = type("Victim", (Packages,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__all_methods(self):
        victim = self.Victim()

        victim.uninstall(DUMMY_MODULE_NAME)
        assert victim.version_get_installed(DUMMY_MODULE_NAME) is None
        assert victim.check_installed(DUMMY_MODULE_NAME) is False

        for version in ["0.0.1", "0.0.2", ]:
            assert victim.upgrade(f"{DUMMY_MODULE_NAME}=={version}")
            assert victim.version_get_installed(DUMMY_MODULE_NAME) == version
            assert victim.check_installed(DUMMY_MODULE_NAME) is True


# =====================================================================================================================
@pytest.mark.skipif(condition=False, reason="too long")
class Test_File:
    def setup_method(self, method):
        self.VICTIM = type("Victim", (Packages,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__upgrade(self, tmpdir):
        # print(tmpdir)
        # ObjectInfo(tmpdir).print()

        victim = self.VICTIM()
        victim.uninstall(DUMMY_MODULE_NAME)
        assert victim.check_installed(DUMMY_MODULE_NAME) is False

        filepath = pathlib.Path(tmpdir.strpath).joinpath("../requirements.txt")
        filepath.write_text(DUMMY_MODULE_NAME)
        assert victim.upgrade_file(filepath) is True

        assert victim.check_installed(DUMMY_MODULE_NAME) is True

    def test__print(self, tmpdir):
        """just see printed file content"""
        victim = self.VICTIM()

        filepath = pathlib.Path(tmpdir.strpath).joinpath("../requirements.txt")
        filepath.write_text(DUMMY_MODULE_NAME)
        victim.upgrade_file(filepath)


# =====================================================================================================================
class Test__Parse:
    # @classmethod
    # def setup_class(cls):
    #     pass
    #     cls.Victim = Version
    #
    # @classmethod
    # def teardown_class(cls):
    #     if cls.victim:
    #         cls.victim.disconnect()
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ("import m1 \n   import m1  ", ["m1", ]),
        ]
    )
    def test__same(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            # -----------------------------
            ("import m1", ["m1", ]),
            ("import   m1  ", ["m1", ]),
            ("import   m1.p1  ", ["m1", ]),
            ("import   m1.p1.p11  ", ["m1", ]),

            # -----------------------------
            ("import m1 \n   import m2  ", ["m1", "m2"]),
        ]
    )
    def test__single(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            # -----------------------------
            ("import m1, m2  ", ["m1", "m2"]),
            ("import m1  , m2  ", ["m1", "m2"]),
            ("import m1.p1, m2  ", ["m1", "m2"]),
            ("import m1.p1.p11, m2.p2  ", ["m1", "m2"]),

            # -----------------------------
            ("import m1.p1, m2  \n import m3 , m4.p4", ["m1", "m2", "m3", "m4"]),
        ]
    )
    def test__multy_comma(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ("import (m1.p1, m2)  ", ["m1", "m2"]),
            ("import   (  m1.p1  ,  m2  )  ", ["m1", "m2"]),
            ("import   (m1.p1,\nm2)", ["m1", "m2"]),
            ("import   (  m1.p1  ,  \nm2  )  ", ["m1", "m2"]),

            # -----------------------------
            ("import   (  m1.p1.p11  ,  \n  m2  )  \n \n import (m3 , m4.p4)", ["m1", "m2", "m3", "m4"]),
        ]
    )
    def test__multy_comma_brackets(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            ("from m1.p1 import p11", ["m1", ]),

            # -----------------------------
            ("from m1.p1 import p11 \n \n  from m2.p2.p22 import p222", ["m1", "m2"]),
        ]
    )
    def test__from(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="args, _EXPECTED",
        argvalues=[
            (
                    "import m11.p1, m12\nimport m13, m14.p4\n\n\n\n\nimport (m21.p1.p11, m22)\nimport (m23,\nm24.p4)\n\n\n\n\nfrom m31.p1 import p11 \nfrom m32.p2.p22 import p222",
                    ["m11", "m12", "m13", "m14",    "m21", "m22", "m23", "m24",     "m31", "m32",]
            ),
        ]
    )
    def test__combo(self, args, _EXPECTED):
        func_link = Packages.parse_text__import
        PytestAux(func_link, args).assert_check(_EXPECTED)


# =====================================================================================================================
