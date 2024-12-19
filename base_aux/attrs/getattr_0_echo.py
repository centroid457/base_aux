from typing import *


# =====================================================================================================================
class GetattrClsEcho_Meta(type):
    """
    GOAL
    ----
    for any not existed attribute return attr-name!

    CREATED SPECIALLY FOR
    ---------------------
    here is GetattrClsEcho
    """
    def __getattr__(cls, item: str) -> str:
        """if no exists attr/meth
        """
        if getattr(cls, "_UNDERSCORE_AS_SPACE"):
            item = item.replace("_", " ")
        return item


# =====================================================================================================================
class GetattrClsEcho(metaclass=GetattrClsEcho_Meta):
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
    assert GetattrClsEcho.hello == "hello"
    assert GetattrClsEcho.hello_world == "hello_world"
    print(GetattrClsEcho.Hello)   # "Hello"
    """
    _UNDERSCORE_AS_SPACE: bool | None = None


class GetattrClsEchoSpace(GetattrClsEcho):
    """
    GOAL
    ----
    SAME AS: base parent class GetattrClsEcho! see all there!
    DIFFERENCE: just replaced all UNDERSCORE-signs by Space!
    """
    _UNDERSCORE_AS_SPACE = True


# =====================================================================================================================
