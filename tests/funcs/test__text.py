import pytest

from base_aux.funcs import *
from base_aux.classes import *
from base_aux.objects import *


# =====================================================================================================================
class Test__sub:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            ("None123", 'None123'),
            ("None_123", 'None_123'),

            # ACCEPTED -------------
            ("null", 'null'),
            ("None", 'null'),
            ("None-123", 'null-123'),

            # CONTAINERS -------------
            ("[null]", '[null]'),
            ("[None]", '[null]'),
            ("[None, ]", '[null, ]'),

            (" None, 123", " null, 123"),
            ("[None, null, 123]", "[null, null, 123]"),
        ]
    )
    def test__1(self, source, _EXPECTED):
        func_link = Text(source).sub__word
        pytest_func_tester__no_kwargs(func_link, ("None", "null"), _EXPECTED)


# =====================================================================================================================
class Test__find:
    @pytest.mark.parametrize(
        argnames="source, pats, _EXPECTED",
        argvalues=[
            ("None123", r"\w*", ["None123", ]),
            ("None123", r"\w+(?#*.*)", ["None123", ]),
            ("None123  #cmt", r"\w+", ["None123", "cmt"]),
            ("   None123  #cmt", r"\w+", ["None123", "cmt"]),
        ]
    )
    def test__1(self, source, pats, _EXPECTED):
        func_link = Text(source).find_by_pats
        pytest_func_tester__no_kwargs(func_link, pats, _EXPECTED)


# =====================================================================================================================

# TODO: FINISH
class Test__try_convert_to_object:
    # -----------------------------------------------------------------------------------------------------------------
    def base_test__try_convert_to_object(self, source, _EXPECTED):
        func_link = Text(source).try_convert_to_object
        pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, None),
            (True, True),
            (False, False),
            (0, 0),
            ([], []),
            ({1: 1}, {1: 1}),
        ]
    )
    def test__originals(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("null", None),
            ("true", True),
            ("false", False),

            ("None", None),

            # ("['None', 1]", [None, 1]),  #JSONDecodeError('Expecting value: line 1 column 2 (char 1)')    # VALUES only DOUBLEQUOTS!!! accepted!!!    # FIXME:
            # ('["None", 1]', [None, 1]),  #FIXME: dont replace None in any quats
            ("[null, 1]", [None, 1]),
            ("[None, 1]", [None, 1]),

            ("True", True),
            ("False", False),
        ]
    )
    def test__bools(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
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
    def test__nums(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("[]", []),
            # ("()", ()),     #JSONDecodeError('Expecting value: line 1 column 1 (char 0)'
            ("{}", {}),
            # ("{1: 1}", {1: 1}), #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
            # ("{'1': 1}", {'1': 1}),   #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 2 (char 1)'
            ('{"1": 1}', {'1': 1}),  # KEYS ONLY in DOUBLEQUOTS!!!
        ]
    )
    def test__containers(self, source, _EXPECTED):
        self.base_test__try_convert_to_object(source, _EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, _EXPECTED",
    argvalues=[
        ("None1", ["None1", ]),
        ("None1   #cmt", ["None1", ]),
        ("   None1   #cmt", ["None1", ]),
        ("#cmt      None2", []),
        ("#cmt \n \n None1 #cmt   hello \n   None2", ["None1", "None2", ]),

        ("None>=1.1", ["None>=1.1", ]),
        ("None>=1.1 #cmt \n None=[1.2, ]", ["None>=1.1", "None=[1.2, ]"]),
    ]
)
def test__requirements__get_list(source, _EXPECTED):
    func_link = Text(source).requirements__get_list
    pytest_func_tester__no_args_kwargs(func_link, _EXPECTED)


# =====================================================================================================================
