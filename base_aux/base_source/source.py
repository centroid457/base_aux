from typing import *
# from base_aux.lambdas.lambdas import Lambda     # CIRCULAR IMPORT


# =====================================================================================================================
class InitSource:
    """
    GOAL
    ----
    just show that class uses init with source - one param
    means inside instance all methods will work on it!
    and all params for methods belong to methods! not about new source!

    SPECIALLY CREATED FOR
    ---------------------
    apply in AttrAux and same others

    :ivar SOURCE: use Lambda or even simple Callable to make a callableGenerate default value! like dict or other user class.
        main Idea for Callable Source is generate independent value in instances.
        it keeps callable type only in class attribute! in instance it will be resolved by calling!

    BEST USAGE
    ----------
        class ClsAux(InitSource):
            SOURCE = MyClass
            SOURCE = Lambda(dict)
            SOURCE = dict
            SOURCE = dict
    """
    # SOURCE: dict = Lambda(dict)     # for callable
    # SOURCE: Any | Lambda = Lambda(None)     # generic final value
    SOURCE: Any = None                      # generic final value

    @classmethod
    @property
    def SOURCE_DEF(cls) -> Any:
        # if isinstance(cls.SOURCE, Lambda):
        if callable(cls.SOURCE):
            result = cls.SOURCE()
        else:
            result = cls.SOURCE
        return result

    def __init__(self, source: Any = None) -> None:
        self.init_source(source)

    def init_source(self, source: Any = None) -> None:
        if source is not None:
            self.SOURCE = source
        else:
            self.SOURCE = self.SOURCE_DEF


# =====================================================================================================================
