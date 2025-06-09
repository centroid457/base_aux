from typing import *


# =====================================================================================================================
class Meta_StrCls_ClsName(type):
    """
    GOAL
    ----
    return cls name from str(Class or inst.__class__)!

    NOTE
    ----
    dont work on instance! - for this purpose add same instance method!!!
    """
    def __str__(cls) -> str:
        return cls.__name__

    def __repr__(cls) -> str:
        return str(cls)


class NestStRCls_ClsName(metaclass=Meta_StrCls_ClsName):
    pass


# =====================================================================================================================
def _examples() -> None:
    class Cls:
        pass

    print(Cls)      # <class '__main__.Cls'>

    # ============================
    class Meta(type):
        def __str__(cls) -> str:
            return cls.__name__

    class Cls(metaclass=Meta):
        pass

    print(Cls)      # Cls
    print(Cls())    # <__main__.Cls object at 0x0000029303138080>

    # ============================
    class Cls(metaclass=Meta):
        def __str__(self) -> str:
            return "inst"

    print(Cls)      # Cls
    print(Cls())    # inst


# =====================================================================================================================
if __name__ == "__main__":
    _examples()


# =====================================================================================================================
