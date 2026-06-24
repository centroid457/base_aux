from base_aux.cmds.m5_terminal0_abc3_paradigm import AbcParadigm_CmdTerminal


# =====================================================================================================================
class Base_CmdTerminal_Serial(AbcParadigm_CmdTerminal):
    """
    GOAL
    ----
    access to SERIAL ports with continuous connection - keeping state!
    """
    def __init__(
            self,
            port: str,

            baudrate: int = 9600,
            bytesize: int = 8,
            parity: str = 'N',
            stopbits: int = 1,

            **kwargs,

            # eol_send: str = "\n",      # already existed! self.EOL_SEND in KWARGS
    ):
        self._serial_port = port

        self._serial_baudrate = baudrate
        self._serial_bytesize = bytesize
        self._serial_parity = parity
        self._serial_stopbits = stopbits

        super().__init__(**kwargs)

    def set_id(self, *args, **kwargs) -> None:
        self.idn = self._serial_port


# =====================================================================================================================
