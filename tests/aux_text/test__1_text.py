import pytest

from base_aux.aux_expect.m1_expect_aux import ExpectAux
from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.base_statics.m4_enums import *


# =====================================================================================================================
class Test__sub:
    @pytest.mark.parametrize(
        argnames="source, rule, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            ("None123", ("None00"), "None123"),
            ("None123", ("None"), "123"),
            ("None123", ("None", None), "123"),
            ("None123", ("None", "0"), "0123"),

            ("1*3", ("\*", "2"), "123"),
        ]
    )
    def test__regexp(self, source, rule, _EXPECTED):
        func_link = TextAux(source).sub__regexp
        ExpectAux(func_link, rule).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # NOT ACCEPTED -------------
            ("None123", "None123"),
            ("None_123", "None_123"),

            # ACCEPTED -------------
            ("null", "null"),
            ("None", "null"),
            ("None-123", "null-123"),

            # CONTAINERS -------------
            ("[null]", "[null]"),
            ("[None]", "[null]"),
            ("[None, ]", "[null, ]"),

            (" None, 123", " null, 123"),
            ("[None, null, 123]", "[null, null, 123]"),
        ]
    )
    def test__words(self, source, _EXPECTED):
        func_link = TextAux(source).sub__words(("None", "null"))
        ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__Edit:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (" " * 2, ""),
            (" " * 3, ""),
            ("line   line", "lineline"),

            (" \n ", "\n"),

            (" 1, _\n\n  \n \t  \r  ()", '1,_\n\n\n\t\r()'),
        ]
    )
    def test__spaces_all(self, source, _EXPECTED):
        func_link = TextAux(source).clear__spaces_all
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (" " * 2, " "),
            (" " * 3, " "),
            ("line   line", "line line"),

            (" \n  ", " \n "),

            (" 1, _\n\n  \n \t  \r  ()", ' 1, _\n\n \n \t \r ()'),
        ]
    )
    def test__spaces_double(self, source, _EXPECTED):
        func_link = TextAux(source).clear__spaces_double
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # BLANK -----
            ("\n", ""),
            (" \n ", ""),

            # EDGES -----
            ("\n line1", " line1"),
            (" \n line1", " line1"),
            (" line1 \n ", " line1 "),

            # MIDDLE -----
            (" line1 \n\n \nline2 ", " line1 \nline2 "),

            # OTHER -----
            (" line1 \n \n line3 ", " line1 \n line3 "),
            (" line1 \n \t\r\n line3 ", " line1 \n line3 "),
        ]
    )
    def test__blank_lines(self, source, _EXPECTED):
        func_link = TextAux(source).clear__blank_lines
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            # ZERO -----
            ("line1 ", "line1 "),

            # SEPARATED -----
            ("#cmt #", ""),
            ("##cmt #", ""),

            ("#cmt ", ""),
            ("  # cmt 1 ", ""),

            # INLINE -----
            ("line  # cmt 1 ", "line"),

            # SEVERAL LINES ====
            ("line1  # cmt1 \n line2 ", "line1\n line2 "),
            ("line1  # cmt1 \n line2 #cmt2", "line1\n line2"),
            ("line1  # cmt1 \n #cmt \n line2 #cmt2", "line1\n line2"),
        ]
    )
    def test__clear__cmts(self, source, _EXPECTED):
        func_link = TextAux(source).clear__cmts
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            ("  ", ("", "", "")),
            ("line1  ", ("line1", "line1  ", "line1")),
            ("  line1 ", ("line1", "line1 ", "  line1")),

            ("line1  \n  line2", ("line1\nline2", "line1  \nline2", "line1\n  line2")),
            ("line1  \n  \n  line2", ("line1\nline2", "line1  \nline2", "line1\n  line2")),
        ]
    )
    def test__strip__lines(self, source, _EXPECTED):
        ExpectAux(TextAux(source).strip__lines).check_assert(_EXPECTED[0])
        ExpectAux(TextAux(source).lstrip__lines).check_assert(_EXPECTED[1])
        ExpectAux(TextAux(source).rstrip__lines).check_assert(_EXPECTED[2])


# =====================================================================================================================
class Test__find:
    @pytest.mark.parametrize(
        argnames="source, patts, _EXPECTED",
        argvalues=[
            ("None123", r"\w*", ["None123", ]),
            ("None123", r"\w+(?#*.*)", ["None123", ]),
            ("None123  #cmt", r"\w+", ["None123", "cmt"]),
            ("   None123  #cmt", r"\w+", ["None123", "cmt"]),
        ]
    )
    def test__1(self, source, patts, _EXPECTED):
        func_link = TextAux(source).find__by_pats
        ExpectAux(func_link, patts).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__shortcut:
    @pytest.mark.parametrize(
        argnames="p1,p2,p3,p4,_EXPECTED",
        argvalues=[
            (None, 5, "...", Where3.LAST, "None"),
            ("", 5, "...", Where3.LAST, ""),
            ("123456", 3, "...", Where3.LAST, "..."),

            ("123", 3, "#", Where3.LAST, "123"),

            ("1223", 3, "#", Where3.FIRST, "#23"),
            ("1223", 3, "#", Where3.MIDDLE, "1#3"),
            ("1223", 3, "#", Where3.LAST, "12#"),

            ("1223", 3, "##", Where3.FIRST, "##3"),
            ("1223", 3, "##", Where3.MIDDLE, "##3"),
            ("1223", 3, "##", Where3.LAST, "1##"),

            ("1223", 3, "###", Where3.FIRST, "###"),
            ("1223", 3, "###", Where3.MIDDLE, "###"),
            ("1223", 3, "###", Where3.LAST, "###"),

            ("1223", 1, "###", Where3.FIRST, "#"),
            ("1223", 1, "###", Where3.MIDDLE, "#"),
            ("1223", 1, "###", Where3.LAST, "#"),

            #
            ("123", 1, "##", Where3.FIRST, "#"),
            ("123", 2, "##", Where3.FIRST, "##"),
            ("123", 3, "##", Where3.FIRST, "123"),
            ("123", 4, "##", Where3.FIRST, "123"),
            ("123", 5, "##", Where3.FIRST, "123"),
        ]
    )
    def test__1(self, p1,p2,p3,p4,_EXPECTED):
        func_link = TextAux(p1).shortcut
        ExpectAux(func_link, kwargs=dict(maxlen=p2, sub=p3, where=p4)).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__try_convert_to_object:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source",
        argvalues=[
            0,
            1,
            10,
            1.0,
            1.1,
            -1.1,
            "",
            '',
            "hello",
            None,
            True,
            False,
            [None, True, 1, -1.1, "hello", "", ''],
            # [None, True, 1, -1.1, "hello", [], {1:1}],  #JSONDecodeError('Expecting property name enclosed in double quotes: line 1 column 37 (char 36)')=KEYS IS ONLY STRINGS
            [None, True, 1, -1.1, "hello", [], {"1": 1, "hello": []}],

            [],
            # (),     # JSONDecodeError('Expecting value: line 1 column 1 (char 0)') - НЕСУЩЕСТВУЕТ TUPLE???
            {},
        ]
    )
    def test__MAIN_GOAL__string_source(self, source):
        func_link = TextAux(str(source)).parse__object  # DONT DELETE STR!!!
        ExpectAux(func_link).check_assert(source)

    # =================================================================================================================
    def base_test__try_convert_to_object(self, source, _EXPECTED):
        func_link = TextAux(source).parse__object
        ExpectAux(func_link).check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, None),
            (True, True),
            (False, False),
            (0, 0),
            ([], []),
            ({"1": 1}, {"1": 1}),   # FIXME: need ref to use always ints in keys!
            # ({1: 1}, {1: 1}),   # FIXME: need ref to use always ints in keys!
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
    func_link = TextAux(source).parse__requirements
    ExpectAux(func_link).check_assert(_EXPECTED)


# =====================================================================================================================
class Test__ParseNum:
    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, fpoint, _EXPECTED",
        argvalues=[
            (0, None, 0),
            ("   0   ", None, 0),
            ("   000   ", None, 0),
            ("-aa001cc", None, 1),
            ("-aa001.000cc", None, 1.0),
            ("-aa001,000cc", None, 1.0),
            ("   -aa001.200cc   ", None, 1.2),
            ("   -aa001.200cc   ", ",", None),
            ("   -aa001,200cc   ", ",", 1.2),
            ("   -aa--001,200cc   ", ",", -1.2),
        ]
    )
    def test__num(self, source, fpoint, _EXPECTED):
        func_link = TextAux(source).parse__number_single
        ExpectAux(func_link, fpoint).check_assert(_EXPECTED)


# =====================================================================================================================
