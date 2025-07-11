import pytest
from base_aux.base_lambdas.m1_lambda import *
from base_aux.buses.m1_serial1_client import *


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[SerialClient._data_ensure__bytes, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (111, Exception),
        (str, Exception),

        ("", b""),
        ("\r", b"\r"),
        ("\r\n", b"\r\n"),
        ("\n", b"\n"),
        ("str", b"str"),
        ("str\n", b"str\n"),
        ("str\r\n", b"str\r\n"),

        (b"", b""),
        (b"\r", b"\r"),
        (b"\r\n", b"\r\n"),
        (b"\n", b"\n"),
        (b"str", b"str"),
        (b"str\n", b"str\n"),
        (b"str\r\n", b"str\r\n"),
    ]
)
def test__data_ensure__bytes(func_link, args, _EXPECTED):
    Lambda(func_link, args).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(argnames="func_link", argvalues=[SerialClient._data_ensure__string, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (111, "111"),

        ("", ""),
        ("\r", "\r"),
        ("\r\n", "\r\n"),
        ("\n", "\n"),
        ("str", "str"),
        ("str\n", "str\n"),
        ("str\r\n", "str\r\n"),

        (b"", ""),
        (b"\r", "\r"),
        (b"\r\n", "\r\n"),
        (b"\n", "\n"),
        (b"str", "str"),
        (b"str\n", "str\n"),
        (b"str\r\n", "str\r\n"),

        (b'step400\x1d', Exx_SerialRead_FailDecoding)
    ]
)
def test__data_ensure__string(func_link, args, _EXPECTED):
    Lambda(func_link, args).expect__check_assert(_EXPECTED)


# =====================================================================================================================
class Victim(SerialClient):
    EOL__SEND = b"\r\n"


@pytest.mark.parametrize(argnames="func_link", argvalues=[Victim._bytes_eol__ensure, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (111, Exception),
        (str, Exception),

        ("", Exception),
        ("\r", Exception),
        ("\r\n", Exception),
        ("\n", Exception),
        ("str", Exception),
        ("str\n", Exception),
        ("str\r\n", Exception),

        (b"", b"\r\n"),
        (b"\r", b"\r\n"),
        (b"\r\n", b"\r\n"),
        (b"\n", b"\r\n"),
        (b"str", b"str\r\n"),
        (b"str\n", b"str\r\n"),
        (b"str\r\n", b"str\r\n"),
    ]
)
def test__bytes_eol__ensures(func_link, args, _EXPECTED):
    Lambda(func_link, args).expect__check_assert(_EXPECTED)


# ---------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(argnames="func_link", argvalues=[Victim._data_eol__clear, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (111, Exception),
        (str, Exception),

        ("", ""),
        ("\r", ""),
        ("\r\n", ""),
        ("\n", ""),
        ("str", "str"),
        ("str\n", "str"),
        ("str\r\n", "str"),

        (b"", b""),
        (b"\r", b""),
        (b"\r\n", b""),
        (b"\n", b""),
        (b"str", b"str"),
        (b"str\n", b"str"),
        (b"str\r\n", b"str"),
    ]
)
def test__data_eol__clear(func_link, args, _EXPECTED):
    Lambda(func_link, args).expect__check_assert(_EXPECTED)


# =====================================================================================================================
@pytest.mark.parametrize(argnames="func_link", argvalues=[SerialClient()._create_cmd_line, ])
@pytest.mark.parametrize(
    argnames="args, _EXPECTED",
    argvalues=[
        (("", ), ""),
        (("\r", ), ""),
        (("\r\n", ), ''),
        (("\n", ), ""),
        (("str", ), "str"),
        (("str\n", ), "str"),
        (("str\r\n", ), "str"),

        ((b"", ), ""),
        ((b"\r", ), ""),
        ((b"\r\n", ), ""),
        ((b"\n", ), ""),
        ((b"str",), "str"),
        ((b"str\n",), "str"),
        ((b"str\r\n",), "str"),

        (("cmd\r\n", "prefix", (1,2)), "prefixcmd 1 2"),
        (("cmd\r\n", None, (1,2)), "cmd 1 2"),
        (("cmd\r\n", None, (1,2), {11: 22}), "cmd 1 2 11=22"),
    ]
)
def test__create_cmd_line(func_link, args, _EXPECTED):
    Lambda(func_link, *args).expect__check_assert(_EXPECTED)


# =====================================================================================================================
