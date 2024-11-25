# GOAL
# KEEP STATIC OBJECTS like TYPE__* and Exx__* in separated file.
# make clear importing by resolving circular imports!


# =====================================================================================================================
class Exx__Valid(Exception):
    pass


class Exx__ValueNotValidated(Exx__Valid):
    pass


# =====================================================================================================================
