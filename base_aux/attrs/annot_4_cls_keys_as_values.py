from typing import *

from .annot_1_aux import AnnotsAux


# =====================================================================================================================
class AnnotClsKeysAsValues_Meta(type):
    """
    return from class just name of annotation as string value.
    if no corresponding annotation - raise!
    """
    def __getattr__(cls, item: str) -> str | NoReturn:
        annots = AnnotsAux(cls).get_nested__dict_types()
        if item in annots:
            return item
        else:
            msg = f"[ERROR] META:'{cls.__name__}' CLASS has no annotation for '{item=}'"
            raise AttributeError(msg)

    def __iter__(cls) -> Iterable[str]:
        annots = AnnotsAux(cls).get_nested__dict_types()
        yield from annots

    def __len__(cls) -> int:
        annots = AnnotsAux(cls).get_nested__dict_types()
        return len(annots)

    def __contains__(cls, item: str) -> bool:
        annots = AnnotsAux(cls).get_nested__dict_types()
        return item in annots

    def __getitem__(cls, item: int) -> str | NoReturn:
        annots = AnnotsAux(cls).get_nested__dict_types()
        return list(annots)[item]

    def __str__(cls) -> str:
        annots = AnnotsAux(cls).get_nested__dict_types()
        return str(tuple(annots))

    def __repr__(cls) -> str:
        annots = AnnotsAux(cls).get_nested__dict_types()
        return f"{cls.__name__}{tuple(annots)}"


# ---------------------------------------------------------------------------------------------------------------------
class AnnotClsKeysAsValues(metaclass=AnnotClsKeysAsValues_Meta):
    """
    used as simple string data container, same as OneWordStringsList with access to values by dot.
    ATTEMPT to get rid of bare data like list[str] ot tuple[str]!

    BEST EXAMPLE (Designed specially for this case)
    -----------------------------------------------
    Suppose you have
        States = ("ON", "OFF")
    next you think it would be better using it over DOT access, so you create class
        class States:
            ON = "ON"
            OFF = "OFF"

    just replace it for
        class States(AnnotClsKeysAsValues):
            ON: str
            OFF: str

    ADVANTAGES
    ----------
    1. DRY

    USAGE
    -----
    1. USE ANNOTATED ATTRIBUTES!
        class MyValues(AnnotClsKeysAsValues):
            VALUE1: str
            VALUE2: str

        print(MyValues.value1)  # AttributeError(...)
        print(MyValues.VALUE1)  # "VALUE1"
        print(MyValues.VALUE2)  # "VALUE2"
        print(MyValues.VALUE3)  # AttributeError(...)

    2. DONT SET VALUES! it would break the main idea! (but maybe you want it).
        class MyValues(AnnotClsKeysAsValues):
            VALUE1: str
            VALUE2: str = 123

        print(MyValues.VALUE1)  # "VALUE1"
        print(MyValues.VALUE2)  # 123

    3. ANNOTATING TYPE IS NOT IMPORTANT! cause of no values exists!
        class MyValues(AnnotClsKeysAsValues):
            VALUE1: Any
            VALUE2: Any

        print(MyValues.VALUE1)  # "VALUE1"
        print(MyValues.VALUE2)  # "VALUE2"

    4. CANT USE INSTANCES!
        class MyValues(AnnotClsKeysAsValues):
            VALUE1: str
            VALUE2: str

        print(MyValues.VALUE1)      # "VALUE1"
        print(MyValues().VALUE1)    #AttributeError: 'MyValues' object has no attribute 'VALUE1'

    WHY NOT ENUM?
    -------------
    0. enum is the next level but we need previous one.
    1. sometimes Enum is OverComplicated just for simple string values.
    2. usually enum use int value for name and you can change value and dont understand what it was before according for value=1
    3. in enum you will get key/value name by unnecessary attributes like *.name/value
    4. if we need only value and value is already equal to name so why we need value with name?
    5. enum keep instances, not the final results.
    6. in enum values are abstract (not valuable)! so why we need to use them if we dont care? and why we need to create not used extra data?
    FINALLY: so here you can directly accessing to exact string values by class attributes.

    WHY NOT NAMEDTUPLE?
    -------------------
    1. its again!.. why we need duplicating values if we already have it in names?
    all we want - access by '*.attribute' to the value,
    so minimum we need is using annotations, that's enough for IDE checker and return string values!
    """
    pass


# =====================================================================================================================
