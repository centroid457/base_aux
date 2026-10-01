import time
from typing import *

from base_aux.aux_eq.m4_eq_valid1_base import Base_EqValid
from base_aux.clients.m1_client_0__base import ClientBase


# ======================================================================================================================
class ClientSsh(ClientBase):
    """
    SSH client implementation that follows the same interface as ClientSerial.
    Uses paramiko for SSH connections.

    REFACTOR NOTE
    -------------
    Класс реализует ТОЛЬКО транспортную логику (paramiko).
    Терминальная логика (read_bytes/write_bytes/EOL/ANSI) — в ClientBase.

    Ключ мультитона — address + username + port, чтобы два SSH-подключения
    к одному хосту под разными учётками не конфликтовали.
    """
    # SETTINGS ------------------------------------------------
    PORT: int = 22

    # INIT =============================================================================================================
    def __init__(
            self,
            # MULTITON KEY ID ------------
            address: str,

            # SSH SETTINGS --------------
            username: str = None,
            password: str = None,
            port: int = None,
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
        self._ssh_client = None
        self._channel = None

        super().__init__(
            address=address,
            history_enable=history_enable,
            _raise_if_occupied=_raise_if_occupied,
            **kwargs,
        )

        self.init_settings(
            username=username,
            password=password,
            port=port,
            timeout_read_initial=timeout_read_initial,
            timeout_read_continue=timeout_read_continue,
            eol__send=eol__send,
            encoding=encoding,
            _raise_if_occupied=_raise_if_occupied,
        )

    # ------------------------------------------------------------------
    @classmethod
    def _multiton_key(cls, address: str, **kwargs) -> str:
        username = kwargs.get("username", None) or "default"
        port = kwargs.get("port", None) or cls.PORT
        return f"{address}:{port}@{username}"

    # ------------------------------------------------------------------
    def init_settings(
            self,
            username: str = None,
            password: str = None,
            port: int = None,
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

        self.username = username
        self.password = password
        self.port = port or self.PORT
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        if self.check__connected():
            return True

        # Закрываем хвосты предыдущего connect (если были) —
        # чтобы не накапливать висячие каналы.
        self.disconnect()

        try:
            import paramiko
        except ImportError:
            print(f"paramiko module is required for SSH connections")
            return False

        try:
            self._ssh_client = paramiko.SSHClient()
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(
                hostname=self.ADDRESS,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout_read_initial,
                allow_agent=False,
                look_for_keys=False,
            )

            self._channel = self._ssh_client.invoke_shell()
            self._channel.settimeout(self.timeout_read_initial)
            # combine stderr в тот же поток — как в Serial
            self._channel.set_combine_stderr(True)

            return True
        except Exception as e:
            print(f"SSH connection error to {self.ADDRESS}: {e}")
            # закрываем всё, что могло открыться
            try:
                if self._channel:
                    self._channel.close()
            except:
                pass
            try:
                if self._ssh_client:
                    self._ssh_client.close()
            except:
                pass
            self._channel = None
            self._ssh_client = None
            return False

    def disconnect(self) -> None:
        try:
            if self._channel:
                self._channel.close()
        except:
            pass
        try:
            if self._ssh_client:
                self._ssh_client.close()
        except:
            pass

    def check__connected(self) -> bool:
        try:
            return self._channel is not None and not self._channel.closed
        except:
            return False

    # ==================================================================================================================
    # TRANSPORT PRIMITIVES
    # ==================================================================================================================
    def _transport__read(self, size: int = 1) -> bytes:
        try:
            # recv возвращает b"" при таймауте
            return self._channel.recv(size)
        except Exception:
            return b""

    def _transport__write(self, data: bytes) -> int:
        return self._channel.send(data)

    def _transport__set_timeout(self, timeout: float | None) -> float | None:
        old = self._channel.gettimeout()
        self._channel.settimeout(timeout)
        return old

    def _transport__restore_timeout(self, old_timeout: float | None) -> None:
        self._channel.settimeout(old_timeout)

    def _transport__flush_input(self) -> None:
        try:
            while self._channel.recv_ready():
                self._channel.recv(4096)
        except Exception:
            pass

    def _transport__pending(self) -> int:
        try:
            # recv_ready() -> bool; приводим к int (0/1)
            return 1 if self._channel.recv_ready() else 0
        except Exception:
            return 0

    # W=SPECIAL --------------------------------------------------------------------------------------------------------
    def send__break(self, duration: float = 0.25) -> None:
        """Send a BREAK condition."""
        # SSH doesn't have a native break signal, send Ctrl+C as alternative
        self.send__ctrl_c()

    def send__ctrl_c(self) -> None:
        """Send the Ctrl+C character (0x03)."""
        self.write_bytes(b'\x03', eol=b"")
        time.sleep(0.2)


# ======================================================================================================================