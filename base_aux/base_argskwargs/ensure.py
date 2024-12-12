from base_aux.base_argskwargs.argskwargs import *
from base_aux.base_objects import TypeChecker

from base_aux.funcs.value_0_explicit import Default


# =====================================================================================================================
def args__ensure_tuple(args: TYPE__VALID_ARGS = (), none_as_empty: bool | None = None) -> tuple:
    """
    GOAL
    ----
    used in methods which handle with *args/args (like in funcs.Valid)
    when we want to apply singular value without tuple

    CREATED SPECIALLY FOR
    ---------------------
    Valid
    but can be used in any funcs!

    NOTE
    ----
    dont disclose iterables!!!

    USAGE
    -----
        def func1(*args):
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

    :param none_as_empty:
        use carefully!

    """
    # TODO: move to object-info or funcsAux???

    # None --------------------------
    if args is None and none_as_empty:
        return ()

    # APPLY DEFAULT --------------------------
    if args is Default:
        args = ()
    elif isinstance(args, Default):
        args = args()

    # ENSURE TUPLE --------------------------
    if not TypeChecker.check__elementary_collection(args):
        result = (args, )
    else:
        result = tuple(args)
    return result


# =====================================================================================================================
