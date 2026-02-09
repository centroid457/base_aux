import pytest


# ---------------------------------------------------------------------------------------------------------------------
class TestRased:
    @staticmethod
    def test__exc_not_specified__failed():
        # with pytest.raises(None):  # FAILED [100%] TypeError: Expected a BaseException type, but got None
        # with pytest.raises([]):  # FAILED [100%] TypeError: Expected a BaseException type, but got 'list'
        with pytest.raises():  # FAILED [100%] ValueError: You must specify at least one parameter to match on.
            1 / 0

        # with pytest.raises(Exception):  # PASSED [100%]

    @staticmethod
    def test__esc_specified_parent__passed():
        with pytest.raises(ZeroDivisionError):  # PASSED [100%]
            1 / 0

    @staticmethod
    def test__exc_specified_child__passed():
        with pytest.raises(Exception):  # PASSED [100%]
            1 / 0

    @staticmethod
    def test__exc_not_raised__failed():
        with pytest.raises(ZeroDivisionError):  # FAILED [100%] ZeroDivisionError: division by zero
            1 / 1

    @staticmethod
    def test__exc_wrong_child__failed():
        with pytest.raises(KeyError):  # FAILED [100%] Failed: DID NOT RAISE <class 'ZeroDivisionError'>
            1 / 0


# ---------------------------------------------------------------------------------------------------------------------
def test__exact_exc_type__failed():
    def foo():
        raise NotImplementedError

    with pytest.raises(RuntimeError) as excinfo:
        foo()
    assert excinfo.type is RuntimeError


# ---------------------------------------------------------------------------------------------------------------------
def myfunc():
    raise ValueError("Exception 123 raised")


def test__match_exc_msg__passed():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()


# ---------------------------------------------------------------------------------------------------------------------
