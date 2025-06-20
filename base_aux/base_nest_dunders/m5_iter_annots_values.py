from base_aux.base_nest_dunders.m4_gsai_ic__annots import *


# =====================================================================================================================
class NestIter_AnnotValues(NestGAI_AnnotAttrIC):
    """
    GOAL
    ----
    iterate annot defined values in position order(nesting is available)

    USAGE
    -----
        class Item:
            pass

        class Example(NestIter_AnnotValues):
            def meth(self):
                pass

            VALUE1: Item = Item(1)
            VALUE3: Item = Item(3)
            VALUE2: Item = Item(2)
            VALUE20: Item
            VALUE200 = 200

        for i in Example():
            print(i)

        ---> Item(1), Item(3), Item(2)

    SPECIALLY CREATED FOR
    ---------------------
    pyqt.pte_highlights.StylesPython

    WHY NOT - NAMEDTUPLE
    --------------------
    typing.NamedTuple is good as collection! but nesting is not accepted!
    """

    def __iter__(self):
        yield from AttrAux_AnnotsAll(self).iter__annot_values()


# =====================================================================================================================
