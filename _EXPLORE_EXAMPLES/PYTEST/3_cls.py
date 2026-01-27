import pytest


# =====================================================================================================================
@pytest.mark.skipif
class TestCls_Skipped:
    def test__group1(self):
        assert True
    def test__group2(self):
        assert True


# =====================================================================================================================
class TestCls:
    @classmethod
    def setup_class(cls):
        # запустится только один раз! на старте обьекта класса!!!
        # BUT all internal tests would seen as FAILED with same cause result!
        print()
        print()
        print(999999999)
        # pytest.fail("Группа отключена")
        # assert False
        raise AssertionError("Группа отключена")

    def test__1(self):
        print()
        print()
        print(111)
        assert True

    def test__2(self):
        print()
        print()
        print(222)
        assert True


# =====================================================================================================================
