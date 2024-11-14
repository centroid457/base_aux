from typing import *
from . import Default


# =====================================================================================================================
"""
HOW to work with ARGS in your funcs
---------------------
usually and maybe often when we passing ARGS it assumed as we will pass tuple/list or direct value
"""


# =====================================================================================================================
class ArgsEmpty(Default):
    """
    THIS IS JUST A PARTIAL CASE FOR ARGS Default

    DEPRECATE ???
    ---------
    USE DIRECTLY THE CONSTANT VALUE ()!!!
    its clear and

    GOAL
    ----
    explicit pass
    resolve not passed parameters in case of None VALUE!

    special object used as VALUE to show that parameter was not passed!
    dont pass it directly! keep it only as default parameter in class and in methods instead of None Value!
    it used only in special cases! not always even in one method!!!

    SAME AS
    -------
    value_explicit.ValueNotExist but just blank collection
    """
    def __init__(self):
        super().__init__(source=())

    # # NOTE: this is not nesessory!!! and even need not to use for sure!
    # @classmethod
    # def __str__(cls):
    #     return "()"
    #
    # @classmethod
    # def __repr__(cls):
    #     return str(cls)
    #
    # @classmethod
    # def __len__(cls):
    #     return 0
    #
    # @classmethod
    # def __bool__(cls):
    #     return False
    #
    # @classmethod
    # def __iter__(cls):
    #     yield from ()


# ---------------------------------------------------------------------------------------------------------------------
TYPE__ARGS_EMPTY = type[ArgsEmpty] | ArgsEmpty


# =====================================================================================================================
if __name__ == '__main__':
    pass
    # CLS ----------------
    print(ArgsEmpty)    # <class '__main__.ArgsEmpty'>
    print(str(ArgsEmpty))   # <class '__main__.ArgsEmpty'>
    # print(len(ArgsEmpty))   #TypeError: object of type 'type' has no len()
    # print(list(ArgsEmpty))  #TypeError: 'type' object is not iterable
    print()

    # INST ---------------
    victim = ArgsEmpty()
    print(victim)
    print(str(victim))
    print(repr(victim))
    print(bool(victim))
    print(len(victim))
    print(list(victim))


# =====================================================================================================================
