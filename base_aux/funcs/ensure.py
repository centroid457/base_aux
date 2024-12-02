from typing import *
from base_aux.objects import TypeChecker


# =====================================================================================================================
def ensure_class(source: Any) -> type:
    """
    GOAL
    ----
    get class from any object

    CREATED SPECIALLY FOR
    ---------------------
    classes.ClsMiddleGroup
    """
    if TypeChecker.check__class(source):
        return source
    else:
        return source.__class__


# =====================================================================================================================
