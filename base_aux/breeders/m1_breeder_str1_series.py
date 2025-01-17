from typing import *

from base_aux.base_exceptions import *


# =====================================================================================================================
class BreederStrSeries(NamedTuple):
    """
    PATTERN FOR BREEDING ONE TYPE OF TEMPLATE STYLE
    used and created special for BreederStrStack
    """
    START_OUTER: int | None  # None used only for recreation in Stack!!! for auto
    COUNT: int
    TEMPLATE: str = "%s"
    START_INNER: int = 1    # just a starting number in values!

    def _raise_if_start_outer_none(self) -> NoReturn | None:
        if self.START_OUTER is None:
            raise Exx__StartOuterNONE_UsedInStackByRecreation()

    def __contains__(self, item: Union[int, str]) -> Union[bool, NoReturn]:
        """
        :param item: one of: 1=OUTER_INDEX (not self-INNER!!!) or 2=ORIGINAL value_NAME
            couse of we usually need to compare OUTER indexes or original VALUES!
        :return:
        """
        self._raise_if_start_outer_none()

        if isinstance(item, int):
            return self.START_OUTER <= item < (self.START_OUTER + self.COUNT)

        elif isinstance(item, str):
            return item in self.get_dict__outer().values()

    def __getitem__(self, item: Union[int, str]) -> Union[int, str, NoReturn]:
        """

        :param item: INTERNAL INDEX! NOT OUTER!!!
        :return: INTERNAL NAME
        """
        _DATA = self.get_dict__inner()

        if item in _DATA:
            return _DATA[item]

        if item in _DATA.values():
            for key, value in _DATA.items():
                if item == value:
                    return key

        msg = f"{item=}"
        raise Exx__ItemNotExists(msg)

    def get_dict__outer(self) -> dict[int, str] | NoReturn:
        self._raise_if_start_outer_none()

        result_outer_sub = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            index_outer = index + self.START_OUTER
            result_outer_sub.update({index_outer: value})
        return result_outer_sub

    def get_dict__inner(self) -> dict[int, str] | NoReturn:
        self._raise_if_start_outer_none()

        result_inner = {}
        for index in range(self.COUNT):
            pos = index + self.START_INNER
            value = self.TEMPLATE % pos

            result_inner.update({pos: value})
        return result_inner

    def get_listed_index__by_outer(self, index: int) -> int | NoReturn:
        """
        usually we have outer index and need to be able get from other list VALUE according to listed index fom this template!

        :param index:
        :return:
        """
        result = 0
        if index in self:
            for _key in self.get_dict__outer():
                if _key == index:
                    return result
                else:
                    result += 1
        else:
            raise Exx__ItemNotExists()

    def get_listed_index__by_value(self, value: str) -> int | NoReturn:
        result = 0
        if value in self:
            for _value in self.get_dict__outer().values():
                if _value == value:
                    return result
                else:
                    result += 1
        else:
            raise Exx__ItemNotExists()


# =====================================================================================================================
