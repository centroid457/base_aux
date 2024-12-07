from typing import *


# =====================================================================================================================
class AttrInitKwargs:
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for name, value in kwargs.items():
            setattr(self, name, value)


# =====================================================================================================================
