from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.aux_attr.m4_kits import *
from base_aux.base_nest_dunders.m3_calls import *


# =====================================================================================================================
class ChainResolve(NestInit_Source, NestCall_Resolve, Base_AttrKit):
    """
    GOAL
    ----
    get cumulated result from several resolvers

    SPECIALLY CREATED FOR
    ---------------------
    HtmlTag
    """
    SOURCE: Any = None
    CHAINS: Iterable[Callable | NestCall_Resolve] = ()

    def __init__(self, *chains, source: Any = None, **kwargs):
        if chains:
            self.CHAINS = chains
        super().__init__(source=source, **kwargs)

    def resolve(self, *args, source: Any = None, **kwargs) -> Any | NoReturn:
        if source is None:
            source = self.SOURCE

        for chain in self.CHAINS:
            source = chain.resolve(*args, source=source, **kwargs)

        return source


# =====================================================================================================================
