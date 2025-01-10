from typing import *


# =====================================================================================================================
def check_name__buildin(name: str) -> bool:
    return name.startswith("__") and name.endswith("__") and len(name) > 4


# =====================================================================================================================
@final
class AttrsDump:
    """
    GOAL
    ----
    just an initial blank class with would be loaded by attrs!
    used further as template or dumped values for dynamic values like properties

    WHY NOT-1: simple DICT?
    cause i just want have dotAccess to values
    """
    pass
    # def __contains__(self, item):     # cant do this here!!!! DONT ADD ANY meth!??? it must be clear?


# =====================================================================================================================
class AnnotsTemplate:
    """
    GOAL
    ----
    use object as template
    notify exact type of object by purpose

    USING
    -----
    see _examples

    NOTE
    ----
    dont use amy methods! no need
    """
    pass


# ---------------------------------------------------------------------------------------------------------------------
def _examples():
    class TemplNested(AnnotsTemplate):
        attr1: None
        attr2: None

    class TemplNotNested:
        attr1: None
        attr2: None


# =====================================================================================================================
