import pytest

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.objects import *


# =====================================================================================================================
def base_test__try_convert_to_object(source, _EXPECTED):
    func_link = Text(source).try_convert_to_object
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (None, None),
        (0, 0),
        ([], []),
        ({1: 1}, {1: 1}),
    ]
)
def test__originals(source, _EXPECTED):
    base_test__try_convert_to_object(source, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        # NONES -------------
        (None, None),
        ("None", None),
        ("null", None),

        # ("['None', 1]", [None, 1]),  #JSONDecodeError('Expecting value: line 1 column 2 (char 1)')    # VALUES only DOUBLEQUOTS!!! accepted!!!    # FIXME:
        # ('["None", 1]', [None, 1]),  #FIXME: dont replace None in any quats
        ("[null, 1]", [None, 1]),
        ("[None, 1]", [None, 1]),

        # BOOL -------------
        (True, True),
        (False, False),

        ("True", True),
        ("False", False),

        ("true", True),
        ("false", False),
    ]
)
def test__bools(source, _EXPECTED):
    base_test__try_convert_to_object(source, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        (0, 0),
        ("0", 0),
        ("00", "00"),
        ("01", "01"),
        ("10", 10),

        ("1.0", 1.0),
        ("1.000", 1.0),

        ("1,000", "1,000"),
    ]
)
def test__nums(source, _EXPECTED):
    base_test__try_convert_to_object(source, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ("[]", []),
        # ("()", ()),     #JSONDecodeError('Expecting value: line 1 column 1 (char 0)'
        ("{}", {}),
        # ("{1: 1}", {1: 1}), #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
        # ("{'1': 1}", {'1': 1}),   #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
        ('{"1": 1}', {'1': 1}),   # KEYS ONLY in DOUBLEQUOTS!!!
    ]
)
def test__containers(source, _EXPECTED):
    base_test__try_convert_to_object(source, _EXPECTED)












# =====================================================================================================================
class Test__1:
    # iters -----------------------------------------------------------------------------------------------------------
    def test__dicts(self):
        # INcorrect
        assert self.victim("{1: 1}") != {1: 1}      # FIXME: for dicts - use only string keys even for numbs!
        assert self.victim("{'1': 1}") != {1: 1}    # FIXME: for dicts - use only double quotes!

        # correct
        assert self.victim('{"1": 1}') == {"1": 1}

    @pytest.mark.skip
    def test__iters2(self):
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        pass


# =====================================================================================================================
