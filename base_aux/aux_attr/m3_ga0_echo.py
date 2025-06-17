from typing import *


# =====================================================================================================================
class Meta_GaClsEcho(type):
    """
    GOAL
    ----
    for any not existed attribute return attr-name!

    CREATED SPECIALLY FOR
    ---------------------
    here is NestGaCls_Echo
    """
    def __getattr__(cls, item: str) -> str:
        """if no exists attr/meth
        """
        if getattr(cls, "_UNDERSCORE_AS_SPACE"):
            item = item.replace("_", " ")
        return item


# =====================================================================================================================
class NestGaCls_Echo(metaclass=Meta_GaClsEcho):
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
    assert NestGaCls_Echo.hello == "hello"
    assert NestGaCls_Echo.hello_world == "hello_world"
    print(NestGaCls_Echo.Hello)   # "Hello"
    """
    _UNDERSCORE_AS_SPACE: bool | None = None


class NestGaCls_EchoSpace(NestGaCls_Echo):
    """
    GOAL
    ----
    SAME AS: base parent class NestGaCls_Echo! see all there!
    DIFFERENCE: just replaced all UNDERSCORE-signs by Space!
    """
    _UNDERSCORE_AS_SPACE = True


# =====================================================================================================================
