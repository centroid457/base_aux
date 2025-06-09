from base_aux.aux_eq.m1_eq_args import *


# =====================================================================================================================
class DictDiff(NestCall_Resolve):
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
    DICTS: tuple[TYPING.DICT_ANY_ANY, ...]

    def __init__(self, *dicts: TYPING.DICT_ANY_ANY):
        self.DICTS = dicts

    def resolve(self) -> dict[Any, tuple[Any, ...]]:
        keys: list[Any] = [key for DICT in self.DICTS for key in DICT]
        keys = sorted(keys)

        result = {}
        for key in keys:
            # values collect -------
            values = []
            for DICT in self.DICTS:
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

        return result

    def __bool__(self) -> bool | NoReturn:
        """
        GOAL
        ----
        answer the question - "Are dicts have diffs?":
            TRUE - if Diffs exists! (it looks from class name!)
            False - if NO Diffs!
        """
        return bool(self.resolve())


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
