from typing import *

from dataclasses import dataclass, field


# =====================================================================================================================
class ItemKeyValue(NamedTuple):
    KEY: str
    VALUE: str


# =====================================================================================================================
@dataclass
class ObjectState:
    """
    GOAL
    ----
    keep final results for obj attributes (call if callable)
    """
    # TODO: add sort method!!!???
    SKIPPED_BUILDIN: list[str] = field(default_factory=list)
    SKIPPED_FULLNAMES: list[str] = field(default_factory=list)
    SKIPPED_PARTNAMES: list[str] = field(default_factory=list)

    PROPERTIES__ELEMENTARY_SINGLE: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__ELEMENTARY_COLLECTION: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__OBJECTS: dict[str, Any] = field(default_factory=dict)
    PROPERTIES__EXX: dict[str, Exception] = field(default_factory=dict)

    METHODS__ELEMENTARY_SINGLE: dict[str, Any] = field(default_factory=dict)
    METHODS__ELEMENTARY_COLLECTION: dict[str, Any] = field(default_factory=dict)
    METHODS__OBJECTS: dict[str, Any] = field(default_factory=dict)
    METHODS__EXX: dict[str, Exception] = field(default_factory=dict)

    def items(self) -> Iterable[tuple[str, Union[list[str],  dict[str, Any]]]]:
        for group_name, group_values in self.__getstate__().items():
            yield group_name, group_values


# =====================================================================================================================
