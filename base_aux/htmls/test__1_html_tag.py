import pytest
from base_aux.base_lambdas.m1_lambda import *
from base_aux.base_types.m2_info import *

from base_aux.htmls.m1_html_tag import *


# =====================================================================================================================
EXAMPLE_HTML = """
<!doctype html>
<html lang="en-US">
  <head>
    <meta charset="utf-8" />
    <title>TITLE</title>
  </head>
  <body>
    <p>TextP1</p>
    <p>TextP2</p>
    <a href="http://example.com/">LinkText<i>Italic</i></a>
    <a cls="cls1" href="http://example.com/link1" id="link1">TextLink1</a>
  </body>
</html>
"""


# =====================================================================================================================
@pytest.mark.parametrize(
    argnames="source, address, _EXPECTED",
    argvalues=[
        (EXAMPLE_HTML, dict(name="p"), "TextP1"),
        (EXAMPLE_HTML, dict(name="p", index=0), "TextP1"),
        (EXAMPLE_HTML, dict(name="p", index=1), "TextP2"),
        (EXAMPLE_HTML, dict(name="a", attrs=dict(cls="cls1")), "TextLink1"),
        (EXAMPLE_HTML, dict(name="a", attrs=dict(id="link1")), "TextLink1"),
        (EXAMPLE_HTML, dict(name="a123", attrs=dict(id="link1")), None),
    ]
)
def test__tags(source, address, _EXPECTED):
    Lambda(HtmlTagParser(source, **address).resolve).expect__check_assert(_EXPECTED)


# =====================================================================================================================
def test__1():
    victim = HtmlTagParser(source=EXAMPLE_HTML, name="p")
    print(victim.resolve())

    body = HtmlTagParser(source=EXAMPLE_HTML, name="body").resolve()
    print(f"{body=}")

    assert HtmlTagParser(source=body, name="p").resolve() == "TextP1"

    # Lambda(victim.resolve).expect__check_assert("TextP1")
    # pass


# =====================================================================================================================
