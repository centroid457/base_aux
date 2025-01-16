from base_aux.base_argskwargs.m1_argskwargs import *
from base_aux.base_objects.obj_types import TypeCheck


# =====================================================================================================================
def args__ensure_tuple(args: Any = ()) -> tuple:
    """
    GOAL
    ----
    used in methods which handle with *args/args (like in funcs.Valid)
    when we want to apply singular value without tuple

    SO IT ONLY ONE DIRECTION
    1/ IF SINGLE - MAKE TUPLE!
    2/ IF ANY COLLECTION - KEEP ORIGINAL!

    CREATED SPECIALLY FOR
    ---------------------
    Valid
    but can be used in any funcs!

    NOTE
    ----
    dont disclose iterables!!!

    USAGE
    -----
        def func1(var, args):
            args = ensure_tuple(args)

        def func2(link: Callable, args):
            args = ensure_tuple(args)
            result = link(*args)

    :param args:
        NONE - is equivalent to SingleElement! so None -> (None, )
        any elementaryCollection - will convert to tuple!
        for others (classes/instances/irerables/generators/...) will assumed as single Object!!! and applied in tuple!!!

        unpacked iterables/generators - if need unpack it manually!!! its not difficult and so clear!
        elementary collection would unpack!
    """
    # TODO: move to object-info or funcsAux???

    # ENSURE TUPLE --------------------------
    if TypeCheck(args).check__elementary_collection():
        result = tuple(args)
    else:
        result = (args,)
    return result


# =====================================================================================================================
