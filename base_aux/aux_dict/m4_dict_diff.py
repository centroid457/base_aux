from base_aux.aux_eq.m1_eq_args import *
from base_aux.aux_dict.m1_dict_aux import *
from base_aux.aux_types.m0_static_typing import *


# =====================================================================================================================
class Base_DiffResolve(NestInit_Args_Implicit, NestCall_Resolve):
    """
    GOAL
    ----
    get diffs from several states,
    dicts assumed like AttrDumped objects - so keys are STR.

    NOTE
    ----
    if values is ExceptionNested - apply only class!!! for both cls and inst - so next cmparing would cmp only exact classes!
    and same classes will be equal

    SPECIALLY CREATED FOR
    ---------------------
    cmp two objects by attr values
    """
    ARGS: tuple[Any, ...]
    DIFF: TYPING.DICT_ANY_TUPLE_ANY
    __diff: TYPING.DICT_ANY_TUPLE_ANY = {}

    def resolve(self) -> TYPING.DICT_ANY_TUPLE_ANY:
        """

        """
        return NotImplemented

    # -----------------------------------------------------------------------------------------------------------------
    def __bool__(self) -> bool:
        """
        GOAL
        ----
        answer the question - "Are dicts have diffs?":
            TRUE - if Diffs exists! (it looks from class name!)
            False - if NO Diffs!
        """
        return bool(self.DIFF)

    @property
    def DIFF(self) -> TYPING.DICT_ANY_TUPLE_ANY:
        """
        GOAL
        ----
        if not exists __diff value - resolve it!
        """
        if not self.__diff:
            self.resolve()
        return self.__diff

    def __str__(self) -> str:
        """
        GOAL
        ----
        print pretty result
        """
        return DictAuxInline(self.DIFF).pretty_str()


# =====================================================================================================================
class DictDiff(Base_DiffResolve):
    ARGS: tuple[TYPING.DICT_ANY_ANY, ...]

    def resolve(self) -> TYPING.DICT_ANY_TUPLE_ANY:
        keys: list[Any] = [key for DICT in self.ARGS for key in DICT]
        keys = sorted(keys)

        result = {}
        for key in keys:
            # values collect -------
            values = []
            for DICT in self.ARGS:
                if key not in DICT:
                    value = VALUE_SPECIAL.NOVALUE
                else:
                    value = DICT[key]

                if isinstance(value, Exception):    # in case of Exx() as dumped value
                    value = value.__class__

                values.append(value)

            # values check eq -------
            if not EqArgs(*values):
                result.update({key: tuple(values)})

        self.__diff = result
        return result


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
