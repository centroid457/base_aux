from typing import *


# =====================================================================================================================
class NestInit_Post:
    """
    GOAL
    ----
    use in all variants - show explicitly
    """
    def __init__(self, *args, **kwargs) -> None | NoReturn:
        super().__init__(*args, **kwargs)

        self._init_post()    # call always last!!!

    def _init_post(self) -> None | NoReturn:     # call always last!!!
        """
        GOAL
        ----
        user initions and checks

        TYPICAL USAGE
        -------------
        make some conversations for source, like str for text
        or
        make initial tests/checks for source, like typecheck
        """
        return NotImplemented


# =====================================================================================================================
