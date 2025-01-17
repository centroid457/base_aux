from base_aux.valid.m2_valid_base import *

from base_aux.buses.m1_serial3_server import *


# =====================================================================================================================
# FIXME: this is just an attempt to replace simple dict!!!
class CmdSchema:
    NAME: str
    SCHEMA: Any | Valid | NoValue = NoValue
    TIMEOUT: float = 0
    DEFAULT: Any | NoValue = NoValue

    __value: Any = NoValue

    # todo: add init

    @property
    def value(self) -> Any:
        pass
        # if self.__value == NoValue:
        #     result = self.

        # return result

    @value.setter
    def value(self, other) -> None:
        self.__value = other

    def __init__(self, name):
        pass

    def __str__(self) -> str:
        return self.output()

    def output(self, value: Any | NoValue = NoValue) -> str:
        if value == NoValue:
            value = self.DEFAULT

        if self.SCHEMA == NoValue:
            return str(value)
        else:
            result = CallableAux(self.SCHEMA, value).resolve_exx()
            return str(result)


class CmdsSchema:
    """
    CREATED SPECIALLY FOR
    ---------------------
    serialClient - to keep default timeouts
    serialServer - to replace simple dictSchema my full needs about schemas
    """
    # default cmds
    # CMD1: CmdSchema = CmdSchema("CMD1", )

    # todo: add getattr by anyRegister
    # todo: add iterate

    def __init__(self, *schemas: tuple | CmdSchema) -> None:
        self.update(*schemas)

    def update(self, *schemas: tuple | CmdSchema) -> None:
        """
        overwrite existed schemas!
        """
        for schema in schemas:
            if not isinstance(schema, CmdSchema):
                schema = CmdSchema(*schema)

            setattr(self, schema.NAME, schema)


# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
# =====================================================================================================================
class SerialServer_Example(SerialServer_Base):
    PARAMS = {
        "VAR": "",

        "STR": "str",
        "QUOTE": "str'",

        "BLANC": "",
        "ZERO": 0,

        "NONE": None,
        "TRUE": True,
        "FALSE": False,

        "INT": 1,
        "FLOAT": 1.1,

        "CALL": time.time,
        "EXX": time.strftime,

        "LIST": [0, 1, 2],
        "LIST_2": [[11]],
        "_SET": {0, 1, 2},
        "DICT_SHORT": {1: 11},
        "DICT_SHORT_2": {"HEllo": {1: 11}},
        "DICT": {
            1: 111,
            "2": 222,
            3: {
                1: 31,
                2: 32,
            },
        },
        "UNIT": ValueUnit(1, unit="V"),
        "VARIANT": ValueVariants(220, variants=[220, 380]),
    }

    def cmd__upper(self, line_parsed: CmdArgsKwargsParser) -> TYPE__CMD_RESULT:
        # usefull for tests
        return line_parsed.SOURCE.upper()

    def cmd__lower(self, line_parsed: CmdArgsKwargsParser) -> TYPE__CMD_RESULT:
        return line_parsed.SOURCE.lower()

    def cmd__cmd(self, line_parsed: CmdArgsKwargsParser) -> TYPE__CMD_RESULT:
        # NOTE: NONE is equivalent for SUCCESS
        # do smth
        pass

    def cmd__cmd_no_line(self) -> TYPE__CMD_RESULT:
        # NOTE: NONE is equivalent for SUCCESS
        # do smth
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def script__script1(self, line_parsed: CmdArgsKwargsParser) -> TYPE__CMD_RESULT:
        # do smth
        pass


# =====================================================================================================================
if __name__ == "__main__":
    SerialServer_Example().run()


# =====================================================================================================================
