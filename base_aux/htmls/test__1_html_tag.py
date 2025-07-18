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
    <a class="link1" href="http://example.com/link1" id="link1">TextLink1</a>
  </body>
</html>
"""


# =====================================================================================================================
# TODO: FINISH!!!
@pytest.mark.parametrize(
    argnames="source, chains, _EXPECTED",
    argvalues=[
        # (EXAMPLE_HTML, (lambda x: x+1, ), 2),
    ]
)
def test__chains(source, chains, _EXPECTED):
    Lambda(HtmlTagParser(source=source).resolve).expect__check_assert(_EXPECTED)


def test__1():
    victim = HtmlTagParser(source=EXAMPLE_HTML, name="p")
    print(victim.resolve())

    body = HtmlTagParser(source=EXAMPLE_HTML, name="body").resolve()
    print(f"{body=}")
    p = HtmlTagParser(source=body, name="p").resolve()
    assert p == "TextP1"


    # Lambda(victim.resolve).expect__check_assert("TextP1")
    # pass


# =====================================================================================================================
