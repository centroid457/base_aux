import time
from typing import *


# =====================================================================================================================
@final
class Sleep:
    """
    GOAL
    ----
    just a primitive func for tests or other purpose!
    """
    SEC: float = 1

    def __init__(self, sec: float = None):
        if sec is not None:
            self.SEC = sec

    def echo(self, echo: Any = None, *args, **kwargs) -> Any:
        time.sleep(self.SEC)
        return echo

    def NONE(self, *args, **kwargs) -> None:
        return self.echo(echo=None, *args, **kwargs)

    def TRUE(self, *args, **kwargs) -> bool:
        return self.echo(echo=True, *args, **kwargs)

    def FALSE(self, *args, **kwargs) -> bool:
        return self.echo(echo=False, *args, **kwargs)

    def EXX(self, *args, **kwargs) -> Exception:
        return self.echo(echo=Exception("Sleep.EXX"), *args, **kwargs)

    def RAISE(self, *args, **kwargs) -> NoReturn:
        time.sleep(self.SEC)
        raise Exception("Sleep.RAISE")


# =====================================================================================================================
