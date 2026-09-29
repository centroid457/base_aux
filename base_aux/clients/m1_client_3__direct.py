import os
import pty
import select
import subprocess
import time
from typing import *

from base_aux.clients.m1_client_0__base import ClientBase


# ======================================================================================================================
class ClientDirect(ClientBase):
    """
    GOAL
    Прямая работа на ОС устройства (тесты запускаются на самом Linux-хосте).

    Транспорт = долгоживущий subprocess с псевдо-терминалом (pty.openpty).
    Это даёт:
        - честное эхо (как в Serial через picocom/putty);
        - ANSI-последовательности (terminal capabilities как в Serial);
        - поведение read(1) с таймаутами через select;
        - совместимость с termинал-логикой ClientBase (read_bytes/write_bytes
          работают точно так же, как на Serial).

    Соответственно, Harvest и все тесты работают на ClientDirect БЕЗ изменений.

    REFACTOR NOTE
    -------------
    Раньше класс был наброском с subprocess.Popen на stdin/stdout пайпах.
    Это плохо работает: bash -i при non-tty буферизует, recv(1) на pipe
    блокируется, ANSI/echo ведут себя иначе, prompt не детектируется
    штатным stop_line. Поэтому переписан на pty.openpty() — теперь
    транспорт по поведению эквивалентен ClientSerial(pyserial).
    """
    # SETTINGS ------------------------------------------------
    SHELL: str = "/bin/bash"
    # Обычно берём bash -i, чтобы получить интерактивный prompt root@host:~#
    # Как в Serial. Если понадобится другой shell — переопределяется в классе-наследнике.
    SHELL_ARGS: list[str] = ["-i"]

    # INIT =============================================================================================================
    def __init__(
            self,
            # MULTITON KEY ID ------------
            address: str = "localhost",

            # TERMINAL SETTINGS ---------
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,
            shell: str = None,
            shell_args: list[str] | None = None,

            # OTHERS ---------------------
            history_enable: bool = False,
            _raise_if_occupied: bool = True,

            **kwargs,
    ):
        # freely create new instance with new settings if not occupied
        self._proc: Optional[subprocess.Popen] = None
        self._master_fd: Optional[int] = None
        self._slave_fd: Optional[int] = None

        super().__init__(
            address=address,
            history_enable=history_enable,
            _raise_if_occupied=_raise_if_occupied,
            **kwargs,
        )

        self.init_settings(
            timeout_read_initial=timeout_read_initial,
            timeout_read_continue=timeout_read_continue,
            eol__send=eol__send,
            encoding=encoding,
            shell=shell,
            shell_args=shell_args,
            _raise_if_occupied=_raise_if_occupied,
        )

    # ------------------------------------------------------------------
    def init_settings(
            self,
            timeout_read_initial: Optional[float] = None,
            timeout_read_continue: Optional[float] = None,
            eol__send: bytes = None,
            encoding: str = None,
            shell: str = None,
            shell_args: list[str] | None = None,

            _raise_if_occupied: bool = True,
    ) -> None | NoReturn:
        if self.check__occupied():
            msg = f"[ERROR] cant change settings for already occupied {self}"
            if _raise_if_occupied:
                raise Exception(msg)
            return

        self.shell = shell or self.SHELL
        self.shell_args = shell_args if shell_args is not None else list(self.SHELL_ARGS)
        self.encoding = encoding or self.ENCODING
        self.timeout_read_initial = timeout_read_initial or self.TIMEOUT_READ_INITIAL
        self.timeout_read_continue = timeout_read_continue or self.TIMEOUT_READ_CONTINUE
        self.eol__send = eol__send or self.EOL__SEND

    # CONNECT ==========================================================================================================
    def connect(self) -> bool:
        if self.check__connected():
            return True
        try:
            # 1=PTY --------------------
            # pty.openpty() возвращает (master_fd, slave_fd).
            # slave_fd передаём дочернему процессу как stdin/stdout/stderr,
            # master_fd держим у себя — читаем/пишем через него.
            master_fd, slave_fd = pty.openpty()
            self._master_fd = master_fd
            self._slave_fd = slave_fd

            # 2=PROCESS ----------------
            self._proc = subprocess.Popen(
                [self.shell, *self.shell_args],
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                close_fds=True,
                preexec_fn=os.setsid,   # отдельная сессия, чтобы shell был session leader на tty
            )

            # 3=CLOSE SLAVE in PARENT ---
            # Родительский процесс slave_fd больше не нужен — держит только дочерний.
            os.close(slave_fd)
            self._slave_fd = None

            # 4=NONBLOCKING master -----
            # Читаем через select(), а не через blocking read.
            os.set_blocking(self._master_fd, False)

            # 5=WARMUP -----------------
            # Даём bash -i время напечатать первый prompt.
            # Без этой паузы первый read_bytes может ничего не увидеть.
            time.sleep(self.timeout_read_initial)

            return True
        except Exception as e:
            print(f"Direct connect error: {e!r}")
            self._cleanup()
            return False

    def disconnect(self) -> None:
        self._cleanup()

    def _cleanup(self) -> None:
        """Закрыть всё, что могло открыться — идемпотентно."""
        # 1=PROC -----------------------
        try:
            if self._proc is not None:
                # убиваем всю группу процессов (shell + потомки)
                try:
                    os.killpg(os.getpgid(self._proc.pid), 15)  # SIGTERM
                    self._proc.wait(timeout=1)
                except Exception:
                    try:
                        os.killpg(os.getpgid(self._proc.pid), 9)  # SIGKILL
                    except Exception:
                        pass
        except Exception:
            pass
        self._proc = None

        # 2=MASTER FD ------------------
        try:
            if self._master_fd is not None:
                os.close(self._master_fd)
        except Exception:
            pass
        self._master_fd = None

        # 3=SLAVE FD (если не закрылся ранее) ------
        try:
            if self._slave_fd is not None:
                os.close(self._slave_fd)
        except Exception:
            pass
        self._slave_fd = None

    def check__connected(self) -> bool:
        try:
            return self._proc is not None and self._proc.poll() is None and self._master_fd is not None
        except:
            return False

    # ==================================================================================================================
    # TRANSPORT PRIMITIVES
    # ==================================================================================================================
    def _transport__read(self, size: int = 1) -> bytes:
        """
        Прочитать до `size` байт с текущим таймаутом.
        Возвращает b"" при таймауте.

        Таймаут хранится в self._current_timeout — его ставит ClientBase через
        _transport__set_timeout() перед каждым read.
        """
        timeout = getattr(self, "_current_timeout", None)
        if timeout is None:
            timeout = self.timeout_read_initial

        try:
            # select с timeout — ждём, пока master_fd станет читаемым
            ready, _, _ = select.select([self._master_fd], [], [], timeout)
            if not ready:
                return b""

            try:
                data = os.read(self._master_fd, size)
            except BlockingIOError:
                return b""
            except OSError:
                # OSError (в т.ч. EIO) обычно означает, что slave закрыт — процесс умер
                return b""

            return data or b""
        except Exception:
            return b""

    def _transport__write(self, data: bytes) -> int:
        try:
            return os.write(self._master_fd, data)
        except Exception as exc:
            # Не роняем — ClientBase сам обработает written=0 как failure
            print(f"[ClientDirect] write error: {exc!r}")
            return 0

    def _transport__set_timeout(self, timeout: float | None) -> float | None:
        """
        У нас нет «встроенного» таймаута, как у pyserial. Просто запоминаем
        текущее значение и возвращаем старое для restore.
        """
        old = getattr(self, "_current_timeout", None)
        self._current_timeout = timeout
        return old

    def _transport__restore_timeout(self, old_timeout: float | None) -> None:
        self._current_timeout = old_timeout

    def _transport__flush_input(self) -> None:
        """
        Слить всё, что накопилось в master_fd (в неблокирующем режиме).
        """
        if self._master_fd is None:
            return
        try:
            while True:
                ready, _, _ = select.select([self._master_fd], [], [], 0)
                if not ready:
                    break
                try:
                    chunk = os.read(self._master_fd, 4096)
                except (BlockingIOError, OSError):
                    break
                if not chunk:
                    break
        except Exception:
            pass

    def _transport__pending(self) -> int:
        """
        Сколько байт доступно для чтения без блокировки.
        Через select с timeout=0 узнаём «есть ли данные», но точное число
        байт в PTY-буфере нам недоступно — вернём 1/0.
        Для ClientBase::write_bytes этого достаточно (там нужно только
        «есть/нет» перед сбросом).
        """
        if self._master_fd is None:
            return 0
        try:
            ready, _, _ = select.select([self._master_fd], [], [], 0)
            return 1 if ready else 0
        except Exception:
            return 0

    # W=SPECIAL --------------------------------------------------------------------------------------------------------
    def send__break(self, duration: float = 0.25) -> None:
        """
        Send a BREAK condition.
        На PTY прямого аналога BREAK нет. Эмулируем через tcsendbreak,
        если возможно; иначе — no-op (как и на SSH).
        """
        try:
            import termios
            if self._master_fd is not None:
                termios.tcsendbreak(self._master_fd, 0)
                return
        except Exception:
            pass
        # fallback — Ctrl+C, как на SSH
        self.send__ctrl_c()

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