from typing import *

from base_aux.base_values.m3_exceptions import Exc__Incompatible


# =====================================================================================================================
class TableObj:
    """
    GOAL
    ----
    create table of objects (lines+columns)
    all lines are same len
    """
    schema: dict[str, list[Any] | Collection]   # Collection if for universal

    def __init__(
            self,
            **schema: list[Any],
    ) -> None | NoReturn:
        if not self._validate_schema(schema):
            msg = f"[{self.__class__.__name__}]countColumns/{schema=}"
            raise Exc__Incompatible(msg)

        self.schema = schema
        self.__count_columns: int = len(list(self.schema.values())[0])

    @classmethod
    def _validate_schema(cls, schema: dict[str, list[Any]]) -> bool:
        """
        GOAL
        ----
        just check the schema is correct!
        mainly by counts!
        """
        len_expect = None
        for name, line in schema.items():
            if not isinstance(name, str):
                # just in case!
                msg = f"[{cls.__name__}]/{name=}"
                print(msg)
                return False

            try:
                len_cur = len(line)
            except Exception as exc:
                print(f"{exc!r}")
                return False

            # init expected
            if len_expect is None:
                len_expect = len_cur

            if len_expect != len_cur:
                msg = f"[{cls.__name__}]/{name=}/{len_expect=}/{len_cur=}"
                print(msg)
                return False

        return True

    def count_lines(self) -> int:
        return len(self.schema)

    def count_columns(self) -> int:
        return self.__count_columns

    def __getitem__(self, item: str) -> list[Any] | NoReturn:
        return self.schema[item]


# =====================================================================================================================
