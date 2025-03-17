from typing import *

from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.base_statics.m1_types import *
from base_aux.threads.m1_item import *
from base_aux.aux_callable.m2_lambdas import *


# =====================================================================================================================
class ThreadLambdaChain(ThreadItem):
    SOURCE: list[Lambda | Callable | type | Any]
    ARGS: TYPING.ARGS_FINAL
    KWARGS: TYPING.KWARGS_FINAL

    result: list[Lambda] = None
    exx: Optional[Exception] = None


# =====================================================================================================================
