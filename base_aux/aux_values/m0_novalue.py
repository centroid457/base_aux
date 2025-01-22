# =====================================================================================================================
class NoValue:
    """
    TODO: DEPRECATE???=NO! used in valid/value
    ---------
    use direct ArgsEmpty???/ArgsKwargs()

    GOAL
    ----
    it is different from Default!
    there is no value!
    used when we need to change logic with not passed value!

    SPECIALLY CREATED FOR
    ---------------------
    Valid as universal validation object under cmp other aux_types!

    USAGE
    -----
    class Cls:
        def __init__(self, value: Any | type[NoValue] | NoValue = NoValue):
            self.value = value

        def __eq__(self, other):
            if self.value is NoValue:
                return other is True
                # or
                return self.__class__(other).run()
            else:
                return other == self.value

        def run(self):
            return bool(self.value)
    """

    def __bool__(self):
        return False


# =====================================================================================================================
TYPE__NOVALUE = type[NoValue] | NoValue


# =====================================================================================================================
