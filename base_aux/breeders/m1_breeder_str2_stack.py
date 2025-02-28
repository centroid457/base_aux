from typing import *

from base_aux.aux_attr.m2_annot1_aux import *
from base_aux.breeders.m1_breeder_str1_series import *
from base_aux.aux_attr.m1_attr2_nest_gsai_anycase import *


# =====================================================================================================================
class BreederStrStack(NestGAI_AttrIC):
    """
    CREATED SPECIALLY FOR
    ---------------------
    applying in Gui tableModels (PyQt5) as header structure

    VULNERABILITIES # FIXME:
    ------------------------
    1. if exists same names cause of patterns - it would return always first index!
        class BreederStrStack_Example2(BreederStrStack):
            TAIL = BreederStrSeries(2, 2, "%s")
            TAIL2 = BreederStrSeries(4, 2, "%s")

        BreederStrStack_Example2()["2"] = 1

    DEFINE
    ------
    !. names (as attributes)
        - dont use underscore as first simble
        - it will be as VALUE for index
    1. dont keep SKIPPED indexes - use all final range!
    2. BreederStrSeries
     - use if need template for some range
     - use any count of such items

    USAGE
    -----
    1. COMPARE BY INDEXES OVER NAME
    if colIndex == MyHeders.attr0:
        pass

    2. GET HEADER NAME BY INDEX or INDEX by NAME!
    headerName = MyHeders[colIndex]
    headerIndex = MyHeders[colName]

    RULES
    -----
    1. use always any ANNOTATIONS for your indexes!!
    2. hide names by using underscore!
    3. use None for AUTOINDEX!!!
    4. indexes follow the order
        class BreederStrStack_Example(BreederStrStack):
            atr1: int
            atr2: int = None


    5. nesting available with correct order!
        class ClsFirst(BreederStrStack):
            atr1: int
            atr3: int = None

        class ClsLast(BreederStrStack):
            atr2: int = None
            atr4: int

        for key, VALUE in ClsLast.annotations__get_nested_list().items():
            print(f"{key}:{VALUE}")

        # atr1:<class 'int'>
        # atr3:<class 'int'>
        # atr2:<class 'int'>
        # atr4:<class 'int'>
    """
    # settings ----------------------
    _INDEX_START: int | None = 0
    _RAISE_IF_INDEX_SKIPPED: bool = True

    # aux ----------------------
    _DATA: dict[int, str] = {}

    def __init__(self):
        if self._INDEX_START is None:
            self._INDEX_START = 0

        index_last = self._INDEX_START -1
        result = {}

        # ATTRS ------------------
        attrs: list[str] = []
        for attr in AnnotsAux(self).get__dict_values():
            if not attr.startswith("_") and not callable(getattr(self, attr)):
                attrs.append(attr)

        # WORK -------------------
        for attr in attrs:
            index = getattr(self, attr)

            # apply AUTO ----------
            if index is None:
                index = index_last + 1
                index_last = index
                setattr(self, attr, index)

            # work INT ----------
            if isinstance(index, int):
                if index in result:
                    msg = f"{index=} from {result=}"
                    raise Exx__IndexOverlayed(msg)
                result.update({index: attr})
                index_last = index

            # work BreederStrSeries ----------
            if isinstance(index, BreederStrSeries):
                # apply AUTO by recreation
                if index.START_OUTER is None:
                    index = BreederStrSeries(index_last + 1, index.COUNT, index.TEMPLATE, index.START_INNER)
                    setattr(self, attr, index)

                # work
                result_sub_dict = index.get_dict__outer()
                for key, value in result_sub_dict.items():
                    if key in result:
                        msg = f"{key=} from {result_sub_dict=}"
                        raise Exx__IndexOverlayed(msg)
                    result.update({key: value})
                    index_last = key

        # RESULT -------------------
        self._DATA = dict(sorted(result.items()))

        # CHECK SKIPPED -----------
        if self._RAISE_IF_INDEX_SKIPPED:
            self.raise_if_index_skipped()

    def __getitem__(self, item: Union[int, str]) -> Union[int, str]:
        if item in self._DATA:
            return self._DATA[item]

        if item in self._DATA.values():
            for name, value in self._DATA.items():
                if item == value:
                    return name

        msg = f"{item=}"
        raise Exx__NotExists(msg)

    def __contains__(self, item: Union[int, str]) -> bool:
        """
        :param item: OUTER INDEX (not self INNER!!!) or inner VALUE NAME
        :return:
        """
        return item in self._DATA or item in self._DATA.values()

    def count(self) -> int:
        return len(self._DATA)

    @classmethod
    def raise_if_index_skipped(cls) -> None | NoReturn:
        index_prev = None
        for index in cls._DATA:
            if index_prev is None:
                index_prev = index
                continue

            if index - index_prev != 1:
                msg = f"index [{index-1}]"
                raise Exx__IndexNotSet(msg)
            index_prev = index


# =====================================================================================================================
class BreederStrStack_Example(BreederStrStack):
    name0: int = 0
    name1: int = 1
    TAIL: BreederStrSeries = BreederStrSeries(2, 2, "%s")


class BreederStrStack_Example__BestUsage(BreederStrStack):
    INDEX: int = 0
    TESTCASE: int = None
    ASYNC: int = None
    STARTUP: int = None
    DUTS: BreederStrSeries = BreederStrSeries(None, 10, "TC_DUT_%s")


# =====================================================================================================================
