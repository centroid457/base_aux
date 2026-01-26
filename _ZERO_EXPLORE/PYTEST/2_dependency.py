import pytest


# =====================================================================================================================
@pytest.mark.dependency
@pytest.mark.skipif(True, reason="skip")
def test_base__skip():
    pass

@pytest.mark.dependency
def test_base__ok():
    pass


# =====================================================================================================================
@pytest.mark.dependency(depends=["test_base__skip", ])
def test__skipped():
    pass

@pytest.mark.dependency(depends=["test_base__ok", ])
def test__started():
    pass


@pytest.mark.dependency(depends=["test_base__skip", ])
class TestCls_Skipped:
    def test_skipped(self):
        pass


@pytest.mark.dependency(depends=["test_ok", ])
class TestCls_Started:
    @pytest.mark.dependency(depends=["test_base__skip", ])
    def test_skipped(self):
        assert False

    @pytest.mark.dependency(depends=["test_base__ok", ])
    def test_ok(self):
        pass


# =====================================================================================================================
import pytest


class TestCls_InternalDep:
    @pytest.mark.dependency
    @pytest.mark.skipif(True, reason="skip")
    def test_cls_base__skip(self):
        pass

    @pytest.mark.dependency
    def test_cls_base__ok(self):
        pass

    @pytest.mark.dependency(depends=["TestCls_InternalDep::test_cls_base__skip", ])
    def test_cls__skipped(self):
        pass

    @pytest.mark.dependency(depends=["TestCls_InternalDep::test_cls_base__ok", ])
    def test_cls__ok(self):
        pass


# =====================================================================================================================
