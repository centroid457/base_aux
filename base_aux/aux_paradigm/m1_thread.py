import threading
from typing import final, NoReturn

from base_aux.base_nest_dunders.m1_init1_source import NestInit_Source
from base_aux.base_types.m1_type_aux import TypeAux
from base_aux.base_values.m3_exceptions import Exc__WrongUsage


# =====================================================================================================================
@final
class ThreadAux(NestInit_Source):
    SOURCE: threading.Thread

    def ensure_thread(self) -> threading.Thread | NoReturn:
        thread = None
        if TypeAux(self.SOURCE).check__thread():
            thread = self.SOURCE
        elif callable(self.SOURCE):
            thread = threading.Thread(target=self.SOURCE, daemon=True)
        else:
            msg = f"not thread-able={self.SOURCE!r}"
            raise Exc__WrongUsage(msg)

        return thread


# =====================================================================================================================
