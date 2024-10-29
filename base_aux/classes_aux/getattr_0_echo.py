import pathlib
from typing import *
from object_info import *


# =====================================================================================================================
class GetattrCls_Meta__Echo(type):
    """
    GOAL
    ----
    for any not existed attribute return attr-name!

    CREATED SPECIALLY FOR
    ---------------------
    here is GetattrEcho
    """
    def __getattr__(cls, item: str) -> str:
        """if no exists attr/meth
        """
        if getattr(cls, "_UNDERSCORE_AS_SPACE"):
            item = item.replace("_", " ")
        return item


# =====================================================================================================================
class GetattrEcho(metaclass=GetattrCls_Meta__Echo):
    """
    GOAL
    ----
    just use class as string values over attributes.
    If you dont want to keep original strings in code.
    just to see maybe it will be pretty convenient.

    CREATED SPECIALLY FOR
    ---------------------
    everyday usage

    NOTE
    ----
    of cause you cant apply any chars (like punctuation) here except Literals cause of name constraints.

    WHY NOT: just using direct strings?
    -----------------------------------

    BEST USAGE
    ----------
    assert GetattrEcho.hello == "hello"
    assert GetattrEcho.hello_world == "hello_world"
    print(GetattrEcho.Hello)   # "Hello"
    """
    _UNDERSCORE_AS_SPACE: bool | None = None


class GetattrEchoSpace(GetattrEcho):
    """
    GOAL
    ----
    SAME AS: base parent class GetattrEcho! see all there!
    DIFFERENCE: just replaced all UNDERSCORE-signs by Space!
    """
    _UNDERSCORE_AS_SPACE = True


# =====================================================================================================================
