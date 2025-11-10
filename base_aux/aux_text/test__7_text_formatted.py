from typing import *
import pytest

from base_aux.base_lambdas.m1_lambda import *
from base_aux.aux_text.m7_text_formatted import PatFormat, TextFormatted
from base_aux.versions.m2_version import Version


# =====================================================================================================================
class Test_Formatted:
    def test__pat_groups(self):
        assert PatFormat.SPLIT_STATIC__IN_PAT == r"(?:\{(?:[_a-zA-Z]\w*)?(?:[^{}]*)\})"

    def test__simple(self):
        victim = TextFormatted("{}", 1)
        assert victim.VALUES._0 == 1

        print("{}".format(1))
        print(str(victim))
        assert str(victim) == "1"

    def test__kwargs(self):
        # kwargs preferred ---------------------------------
        victim = TextFormatted("hello {name}={value}", *(1, 2))
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == 1
        print(str(victim))
        assert str(victim) == "hello 1=2"

        victim.VALUES.name = "name"
        assert victim.VALUES.name == "name"
        print(str(victim))
        assert str(victim) == "hello name=2"

        # kwargs preferred ---------------------------------
        victim = TextFormatted("hello {name}={value}", "arg1", name="name", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "name"
        print(str(victim))
        assert str(victim) == "hello name=1"

        victim.VALUES.name = "name2"
        assert victim.VALUES.name == "name2"
        print(str(victim))
        assert str(victim) == "hello name2=1"

        # args ---------------------------------
        victim = TextFormatted("hello {name}={value}", "arg1", value=1)
        # assert victim.VALUES._0 == "arg1"
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "arg1"
        print(str(victim))
        assert str(victim) == "hello arg1=1"

    def test__other(self):
        # OK --------
        victim = TextFormatted("hello {name}={value}", "arg1", value=1)
        # assert victim.VALUES._1 == 1
        assert victim.VALUES.name == "arg1"
        print(str(victim))
        assert str(victim) == "hello arg1=1"

        victim.other("hello name_other=222")
        print(str(victim))
        assert victim.VALUES.name == "name_other"
        assert victim.VALUES.value == 222

        victim.other("hello =222")
        print(str(victim))
        assert victim.VALUES.name == ""
        assert victim.VALUES.value == 222

        victim.other("hello  name_other=222")
        print(str(victim))
        assert victim.VALUES.name == " name_other"
        assert victim.VALUES.value == 222

        # EXC --------
        for wrong_value in ["he name_other=222", "hello name_222", "hello name_other222", ]:
            try:
                victim(wrong_value)
            except:
                pass
            else:
                print(111111, str(victim))
                print(222222, repr(victim))
                assert False

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,_EXPECTED",
        argvalues=[
            ("hello {name}={value}", (), {}, "hello ="),
            ("hello {name}={value}", (), dict(name=1), "hello 1="),
            ("hello {name}={value}", (), dict(name=1, value=2), "hello 1=2"),
            ("hello {name}={value}", (11, 22), dict(name=1, value=2), "hello 1=2"),
            ("hello {name}={value}", (11, 22), dict(), "hello 11=22"),
            ("hello {name}={value}", (11, 22), dict(value=Version("1.2.3")), "hello 11=1.2.3"),

            ("hello\n\n{name}\n{value}", (11, 22), dict(), "hello\n\n11\n22"),

            ("hello {name}={value:3}", (), dict(name=1, value=2), "hello 1=  2"),
        ]
    )
    def test__str(self, pat_format, args, kwargs, _EXPECTED):
        func_link = lambda: str(TextFormatted(pat_format, *args, **kwargs))
        Lambda(func_link).expect__check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,_EXPECTED",
        argvalues=[
            ("hello{name}", (), dict(name=1), [int, 1]),
            ("hello{name}", (), dict(name="1"), [str, "1"]),
            ("hello{name}", (), dict(name=Version("1.2.3")), [Version, Version("1.2.3")]),
        ]
    )
    def test__type_apply(self, pat_format, args, kwargs, _EXPECTED):
        victim = TextFormatted(pat_format, *args, **kwargs)
        func_link = lambda: victim.VALUES.__annotations__["name"]
        Lambda(func_link).expect__check_assert(_EXPECTED[0])

        func_link = lambda: getattr(victim.VALUES, "name")
        Lambda(func_link).expect__check_assert(_EXPECTED[1])

        Lambda(lambda: victim.VALUES.name.__class__).expect__check_assert(_EXPECTED[0])

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="pat_format,args,kwargs,new,_EXPECTED",
        argvalues=[
            ("hello{name}", (), dict(name=1), 1, [True, int, 1]),
            ("hello{name}", (), dict(name=1), "1", [True, int, 1]),
            ("hello{name}", (), dict(name=1), "text", [Exception, int, 1]),
            ("hello{name}", (), dict(name="1"), "text", [True, str, "text"]),
            ("hello{name}", (), dict(name="1"), "1", [True, str, "1"]),
            ("hello{name}", (), dict(name="1"), 1, [True, str, "1"]),
            ("hello{name}", (), dict(name=Version("1.2.3")), "1.2.3", [True, Version, Version("1.2.3")]),
        ]
    )
    def test__value_set(self, pat_format, args, new, kwargs, _EXPECTED):
        victim = TextFormatted(pat_format, *args, raise_types=True, **kwargs)

        # INCORRECT ------------------------------------
        # victim.VALUES.name = str(kwargs["name"])
        # func_link = lambda: victim.VALUES.name
        # Lambda(func_link).check_assert(_EXPECTED[1])
        #
        # Lambda(lambda: victim.VALUES.name.__class__).check_assert(_EXPECTED[0])

        # CORRECT ------------------------------------
        try:
            victim["name"] = new
            Lambda(True).expect__check_assert(_EXPECTED[0])
        except:
            Lambda(Exception).expect__check_assert(_EXPECTED[0])
            victim = TextFormatted(pat_format, *args, raise_types=False, **kwargs)
            victim["name"] = new    # NoRaise here!
            return
            pass

        Lambda(lambda: victim.VALUES.name.__class__).expect__check_assert(_EXPECTED[1])

        func_link = lambda: victim.VALUES.name
        Lambda(func_link).expect__check_assert(_EXPECTED[2])


# =====================================================================================================================
