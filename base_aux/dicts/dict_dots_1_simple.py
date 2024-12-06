from typing import *
# from base_aux.funcs import Iterables
from base_aux.funcs import IterAux, Explicit
from base_aux.attrs import *
from base_aux.objects import ObjectInfo


# =====================================================================================================================
class DictCaseinsense(dict):
    """
    just a Caseinsense dict
    """
    # __getattr__ = dict.get
    # __setattr__ = dict.__setitem__
    # __delattr__ = dict.__delitem__
    # __iter__ = dict.__iter__
    # __copy__ = dict.copy

    # __repr__ = dict.__repr__  # и так работает!
    # __str__ = dict.__str__    # и так работает!
    # __len__ = dict.__len__    # и так работает!

    # -----------------------------------------------------------------------------------------------------------------
    # GENERIC CLASSES LIKE DICT MUST APPLIED LAST IN MRO!!!
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # -----------------------------------------------------------------------------------------------------------------
    def _getitem_original(self, item: Any) -> Explicit | None:
        return IterAux.item__get_original__case_insensitive(item, self)

    def pop(self, item: Any) -> None:
        item_original = self._getitem_original(item)
        if item_original is None:
            item_original = item
        else:
            item_original = item_original()

        super().pop(item_original)

    def get(self, item: Any) -> Any:    # | NoReturn:
        """
        always get value or None!
        if you need check real contain key - check contain)))) [assert key in self] or [self._getitem_original]
        """
        key_original = self._getitem_original(item)
        if key_original is None:
            return None
            # key_original = item
            # msg = f"{item=}"
            # raise KeyError(msg)
        else:
            key_original = key_original()  # EXPLICIT get value

        return super().get(key_original)

    # def set(self, item: Any, value: Any) -> None:

    def update(self, m, /, **kwargs) -> None:
        for item, value in m.items():
            key_original = self._getitem_original(item)
            if key_original is None:
                key_original = item
            else:
                key_original = key_original()  # EXPLICIT get value

            super().update({key_original: value})

    def __contains__(self, item: Any) -> bool:
        if self._getitem_original(item) is not None:
            return True

    # -----------------------------------------------------------------------------------------------------------------
    # ITEM is universal!
    def __getitem__(self, item: Any) -> Any | NoReturn:
        return self.get(item)

    def __setitem__(self, item: Any, value: Any) -> None | NoReturn:
        self.update({item: value})

    def __delitem__(self, item: Any) -> None:
        self.pop(item)


# =====================================================================================================================
class DictDots(DictCaseinsense):
    """
    dot.notation access to dictionary keys.
    RULES
    ------
    1. Levels
        first level - WriteRead
        all other nested levels - ReadOnly for root level! but no errors when set new!
    2. caseInsensitive
    3. when object created it create new copy dict - so it not the same as dict link!




    # FIXME: below is old!
    CANT CREATE SINGLETON!
    cant create singleton!!! i was trying!!! even by typical def __***

    typical usage:
        my_dict = {'param1': 'GOOD'}
        nested_dict = {'param1': 'nested GOOD too'}
        print(my_dict)  # {'param1': 'GOOD'}

        # EXECUTE
        my_dict = DictDotAttrAccess(my_dict)

        # READING
        print(my_dict)  # {'param1': 'GOOD'}
        print(my_dict.param1)  # 'GOOD'
        print(my_dict["param1"])  # 'GOOD'

        # CHANGE
        my_dict.param1 = 123
        print(my_dict)  # {'param1': 123}
        print(my_dict.param1)  # 123
        my_dict["param1"] = 1000
        print(my_dict)  # {'param1': 1000}
        print(my_dict.param1)  # 1000

        # NESTED
        my_dict.nested = nested_dict
        print(my_dict)  # {'param1': 1000, 'nested': {'param1': 'nested GOOD too'}}
        # print(my_dict.nested.param1)  # AttributeError: 'dict' object has no attribute 'param1'

        my_dict.nested = DictDotAttrAccess(nested_dict)
        print(my_dict)  # {'param1': 1000, 'nested': {'param1': 'nested GOOD too'}}
        print(my_dict.nested.param1)  # 'nested GOOD too'

    ОСОБЕННОСТИ:
        +++И ТАК РАБОТАЛО
            1. +BLANK
                my_dict = DictDotAttrAccess()
                print(my_dict)  # {}

            2. +BOOL
                my_dict = DictDotAttrAccess()
                print(bool(my_dict))  # False

                my_dict = DictDotAttrAccess({'p1': '111'})
                print(my_dict)  # {'p1': '111'}
                print(bool(my_dict))  # True

            3. +IN LIST
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                print("p1" in my_dict)  # True

            5. +при обращении к НЕCУЩЕСТВУЮЩЕМУ - выдает None! без добавления параметра, а после присвоения - параметр создается
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                print(my_dict.p2)  #None
                print(my_dict)  #{'p1': '111'}
                my_dict.p2 = 222
                print(my_dict)  #{'p1': '111', 'p2': 222}

            6. +UPDATE
                my_dict= DictDotAttrAccess()
                print(my_dict)  # {}

                my_dict.update({1:1})
                print(my_dict)  # {1: 1}

            6. +POP
                my_dict = DictDotAttrAccess({1:1})

                my_dict.pop(1)
                print(my_dict)  # {}

            8. +ITEMS()
                my_dict = DictDotAttrAccess({'p1': '111'})
                print(my_dict.items())  #dict_items([('p1', '111')])

            10. +ИТЕРИРОВАТЬ
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                for i in my_dict:
                    print(i, my_dict.get(i))    # p1 111

            11. +КОПИЮ
                my_dict = {'p1': '111'}
                my_dict = DictDotAttrAccess(my_dict)
                print(my_dict)  # {'p1': '111'}

                my_dict2 = copy.copy(my_dict)
                print(my_dict2)  # {'p1': '111'}


        ---НЕ ПОЛУЧИЛОСЬ РЕАЛИЗОВАТЬ
            20. замену для __MISSING__
                def __missing__(self, key):
                    return "HELLO"

                __missing__ = lambda: "HELLO"
                __missing__ = FUNC_LINK_LAMBDA_REPEATER
    """
    # -----------------------------------------------------------------------------------------------------------------
    def __getitem__(self, item: Any) -> Any | NoReturn:
        result = self.get(item)         # thats wrong with NESTING! not will working with saving results!!!
        if isinstance(result, dict):
            result = DictDots(result)

        return result

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Any | None:
        return self[item]

    def __setattr__(self, item: str, value: Any) -> None | NoReturn:
        self[item] = value

    def __delattr__(self, item: str | Any) -> None:
        del self[item]


# =====================================================================================================================
class DictDotsAnnotRequired(DictDots, AnnotRequired):
    """
    its a derivative for DictDots with applying AnnotRequired

    WHY NOT 1=just simple nesting AnnotRequired?
    --------------------------------------------
    in this case
    first we need apply DICT inition
    and only secondary we could check any by AnnotRequired.
    BUT DICT is a stopping/last class!!!

    so we cant just call init with super()
    """
    def __init__(self, *args, **kwargs) -> None | NoReturn:
        super().__init__(*args, **kwargs)
        # super(AnnotRequired, self).__init__()
        # annot_types = self.annot__get_nested__dict_types()
        # print(f"{annot_types=}")
        not_def_list = self.annot__get_not_defined()
        # FIXME: here I cant handle i parent methods order! i messed out! and break it by redefine by this not ideal solvation
        # print(f"{not_def_list=}")
        if not_def_list:
            msg = f"{not_def_list=}"
            raise Exception(msg)

    def annot__get_not_defined(self) -> list[str]:
        result = []
        nested = self.annot__get_nested__dict_types()
        for key in nested:
            if key not in self:
                result.append(key)
        return result


# =====================================================================================================================
if __name__ == '__main__':
    class Cls(DictDotsAnnotRequired):
        ATTR1: str

    victim = Cls()
    ObjectInfo(victim).print()


# =====================================================================================================================
