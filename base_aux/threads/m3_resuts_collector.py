from typing import *

from base_aux.base_nest_dunders.m1_init1_source2_kwargs import *
from base_aux.base_statics.m1_types import *


# =====================================================================================================================
obj = create()
[threadItem(connect, ), threadItem(cal1, args1, kwargs1), threadItem(2), ]
# call all in sequence!!!


class ThreadChain(ThreadItem):
    SOURCE: list[ThreadItem]

    result: dict

    def init_post(self):
        self.result = {}

    def run(self):
        for item in self.SOURCE:
            item.run()

            self.result.update()


# =====================================================================================================================
