# REASON: try to create clear separated classes!

from serial import Serial, SerialException

from base_aux.aux_eq.m4_eq_valid3_derivatives import *
from base_aux.clients.m1_client_0__base import ClientBase


# ======================================================================================================================
class ClientSerial(ClientBase):
    """
    CONSTRAINTS
    1/ work with string for user!
        all unusual packages in bytes (CtrlC ...) send by special method!
    2/ history is not used usually! may be need to delete it!
        all you need - take result as read lines or line
        maybe keep history in device? not in this connection object
    3/

    REFACTOR NOTE
    -------------
    Класс теперь содержит ТОЛЬКО транспортную логику (pyserial).
    Терминальная логика (read_bytes/write_bytes/EOL/ANSI) — в ClientBase.
    """
    # SETTINGS ------------------------------------------------
    BAUDRATE: int = 9600  # 115200

    # INIT =============================================================================================================
    def __init__(
            self,
            # MULTITON KEY ID ------------
            address: str,

            # PORT SETTINGS --------------
            baudrate: int = None,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,

            # OTHERS ---------------------
            history_enable: bool = False,
            _raise_if_occupied: bool = True,

            **kwargs,
    ):
        # freely create new instance with new settings if not occupied
        self._conn: Optional[Serial] = None

        super().__init__(
            address=address,
            history_enable=history_enable,
            _raise_if_occupied=_raise_if_occupied,
            **kwargs,
        )

        self.init_settings(
            baudrate=baudrate,
            timeout_read_initial=timeout_read_initial,
            timeout_read_continue=timeout_read_continue,
            eol__send=eol__send,
            encoding=encoding,
            _raise_if_occupied=_raise_if_occupied,
        )

    # ------------------------------------------------------------------
    def init_settings(
            self,
            baudrate: int = None,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,

            _raise_if_occupied: bool = True,
    ) -> None | NoReturn:
        if self.check__occupied():
            msg = f"[ERROR] cant change settings for already occupied {self}"
            if _raise_if_occupied:
                raise Exception(msg)
            return

        self.baudrate = baudrate or self.BAUDRATE
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        if self.check__connected():
            return True
        try:
            self._conn = Serial(
                port=self.ADDRESS,
                baudrate=self.baudrate,
                timeout=self.timeout_read_initial,
                write_timeout=None,
            )
            return True
        except SerialException as e:
            cause = e.__cause__ or e.__context__
            if cause and isinstance(cause, FileNotFoundError):
                print(f"Port {self.ADDRESS} does not exist")
            elif cause and isinstance(cause, PermissionError):
                print(f"Permission denied for {self.ADDRESS} (maybe open)")
            else:
                # fallback на текст
                msg = str(e).lower()
                if "file not found" in msg or "no such file" in msg:
                    print(f"Port {self.ADDRESS} does not exist")
                elif "permission denied" in msg or "access denied" in msg:
                    print(f"Permission denied for {self.ADDRESS}")
                else:
                    print(f"Serial error on {self.ADDRESS}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def disconnect(self) -> None:
        try:
            self._conn.close()
        except:
            pass

    def check__connected(self) -> bool:
        try:
            return self._conn.is_open
        except:
            return False

    # ==================================================================================================================
    # TRANSPORT PRIMITIVES
    # ==================================================================================================================
    def _transport__read(self, size: int = 1) -> bytes:
        return self._conn.read(size)

    def _transport__write(self, data: bytes) -> int:
        return self._conn.write(data)

    def _transport__set_timeout(self, timeout: float | None) -> float | None:
        old = self._conn.timeout
        self._conn.timeout = timeout
        return old

    def _transport__restore_timeout(self, old_timeout: float | None) -> None:
        self._conn.timeout = old_timeout

    def _transport__flush_input(self) -> None:
        # сбрасываем оба буфера, как было в старом buffers_clear
        self._conn.reset_input_buffer()
        self._conn.reset_output_buffer()

    def _transport__pending(self) -> int:
        return self._conn.in_waiting

    # W=SPECIAL --------------------------------------------------------------------------------------------------------
    def send__break(self, duration: float = 0.25) -> None:
        """Send a BREAK condition."""
        self._conn.send_break(duration)

    def send__ctrl_c(self) -> None:
        """Send the Ctrl+C character (0x03)."""
        self.write_bytes(b'\x03', eol=b"")
        time.sleep(0.2)


# ======================================================================================================================
def _explore1():
    pass


# ======================================================================================================================
if __name__ == "__main__":
    _explore1()
    pass


# ======================================================================================================================