from typing import final


# =====================================================================================================================
@final
class AttrDump:
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
    class Cls:
        ATTR: int = 1


    print(Cls.__annotations__)
    print(Cls().__annotations__)
    print(Cls().__class__.__annotations__)
    print()


    class Cls:
        ATTR = 1


    print(Cls.__annotations__)
    print(Cls().__annotations__)
    print(Cls().__class__.__annotations__)
    print()


    class Cls:
        pass


    print(Cls.__annotations__)
    print(Cls().__annotations__)
    print(Cls().__class__.__annotations__)
    print()


    @final
    class Cls:
        pass


    print(Cls.__annotations__)
    print(Cls().__annotations__)
    print(Cls().__class__.__annotations__)
    print()


    @final
    class Cls:
        """
        hello
        """


    print(Cls.__annotations__)
    print(Cls().__annotations__)
    print(Cls().__class__.__annotations__)
    print()


# =====================================================================================================================
