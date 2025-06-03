from typing import *


# =====================================================================================================================
class Base_AttrDumped:
    """
    SPECIALLY CREATED FOR
    ---------------------
    make obj with independent __annotations__
    """
    pass


@final
class AttrDumped(Base_AttrDumped):
    """
    GOAL
    ----
    just use static bare class for dumping any set of attrs!

    WHY NOT - AttrsKit
    ------------------
    cause sometimes it makes circular recursion exx!
    """


# =====================================================================================================================
if __name__ == "__main__":
    # OK
    class Cls:
        pass

    print(Cls.__annotations__)      # class first - ok! like touch!
    print(Cls().__annotations__)
    print()

    # FAIL
    class Cls:
        pass

    # print(Cls().__annotations__)    # inst first - exx
    print(Cls.__annotations__)
    print()

    class Cls:
        pass

    victim = Cls()
    try:
        print(victim.__annotations__)
        assert False
    except:
        pass
    victim.__class__.__annotations__
    print(victim.__annotations__)

    victim.__class__.__annotations__.update(attr=1)
    assert victim.__annotations__ != victim.__class__.__annotations__


# =====================================================================================================================
