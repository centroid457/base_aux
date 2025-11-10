from typing import *


# =====================================================================================================================
class Base_AttrDumped:
    """
    SPECIALLY CREATED FOR
    ---------------------
    make obj with independent __annotations__
    """
    pass

    # TODO: how to add DumpStrPretty here without mess attr names???


@final
class AttrDumped(Base_AttrDumped):
    """
    GOAL
    ----
    just use static bare class for dumping any set of attrs!

    WHY NOT - AttrsKit
    ------------------
    cause sometimes it makes circular recursion exc!
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

    # print(Cls().__annotations__)    # inst first - exc
    print(Cls.__annotations__)
    print()

    class Cls:
        pass

    victim = Cls()
    try:
        print(victim.__annotations__)
    except:
        pass
    else:
        assert False
    victim.__class__.__annotations__
    print(victim.__annotations__)

    victim.__class__.__annotations__.update(attr=1)
    assert victim.__annotations__ != victim.__class__.__annotations__


# =====================================================================================================================
