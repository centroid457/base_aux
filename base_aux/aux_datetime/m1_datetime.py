from typing import *
import datetime

from base_aux.base_inits.m1_source import *


# =====================================================================================================================
@final
class DateTimeAux(InitSource):
    SOURCE: datetime.datetime = datetime.datetime.now

    def init_post(self) -> None | NoReturn:
        # FIXME: finish!!! int/float/td/str??? parser???
        if isinstance(self.SOURCE, datetime.datetime):
            return
        elif False:
            pass
        else:
            pass

    def get_str(self, add_ms: bool = None, pattern: str = "%Y%m%d_%H%M%S") -> str:
        """
        GOAL
        ----
        use for filenames like dumps/reservations/logs

        SPECIALLY CREATED FOR
        ---------------------

        EXAMPLES
        --------
        %Y%m%d_%H%M%S -> 20241203_114845
        add_ms -> 20241203_114934.805854
        """
        if add_ms:
            pattern += f".%f"

        result = self.SOURCE.strftime(pattern)
        return result

    def get_str__date(self, add_weekday: bool = None, pattern: str = "%Y.%m.%d") -> str:
        """
        EXAMPLES
        --------
        %Y.%m.%d -> 2024.12.03.Tue
        """
        if add_weekday:
            pattern += ".%a"
        result = self.get_str(pattern=pattern)
        return result

    def get_str__time(self, add_ms: bool = None, pattern: str = "%H:%M:%S") -> str:
        """

        EXAMPLES
        --------
        12:09:53
        12:11:53.855764
        """
        result = self.get_str(pattern=pattern, add_ms=add_ms)
        return result

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return self.get_str()

    def __repr__(self):
        return str(self)


# =====================================================================================================================
if __name__ == '__main__':
    print(DateTimeAux().get_str__time(True))


# =====================================================================================================================
