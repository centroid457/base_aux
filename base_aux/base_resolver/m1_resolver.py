from typing import *


# =====================================================================================================================
class Resolver:
    """
    GOAL
    ----
    just show that nested class used basically for main purpose which will returned by .resolve() method
    its like an aux-function but with better handling

    NOTE
    ----
    dont use it as type!
    dont keep in attributes!
    resolve ti inline!

    SPECIALLY CREATED FOR
    ---------------------
    files.filepath
    """

    def __call__(self, *args, **kwargs):
        return self.resolve()

    def resolve(self) -> Any:
        pass


# =====================================================================================================================
