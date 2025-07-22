from typing import *

from base_aux.base_nest_dunders.m1_init1_source import *
from base_aux.aux_attr.m4_kits import *
from base_aux.base_nest_dunders.m3_calls import *
from base_aux.loggers.m1_print import *


# =====================================================================================================================
class ChainResolve(NestInit_Source, NestCall_Resolve, Base_AttrKit):
    """
    GOAL
    ----
    get cumulated result from several resolvers

    SPECIALLY CREATED FOR
    ---------------------
    HtmlTag to find text by chain
    """
    SOURCE: Any = None
    CHAINS: tuple[Callable | NestCall_Resolve, ...] = ()

    ON_RAISE: EnumAdj_ReturnOnRaise = EnumAdj_ReturnOnRaise.NONE

    def __init__(self, *chains, source: Any = None, **kwargs):
        if chains:
            self.CHAINS = chains
        super().__init__(source=source, **kwargs)

    def resolve(self, source: Any = None, **kwargs) -> Any | NoReturn:
        if source in [None, NoValue]:
            source = self.SOURCE

        for chain in self.CHAINS:
            try:
                source = chain(source)
            except Exception as exx:
                Warn(f"{source=}/{exx!r}")

                if self.ON_RAISE == EnumAdj_ReturnOnRaise.NONE:
                    return None
                elif self.ON_RAISE == EnumAdj_ReturnOnRaise.RAISE:
                    raise exx
                elif self.ON_RAISE == EnumAdj_ReturnOnRaise.EXX:    # NOTE: dont use it! just as variant
                    return exx

        return source


# =====================================================================================================================
