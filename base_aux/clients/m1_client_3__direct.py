import subprocess
from base_aux.clients.m1_client_0__base import ClientBase


class ClientDirect(ClientBase):
    """
    GOAL
    Прямая работа на ОС устройства (тесты запускаются на самом Linux-хосте).
    Транспорт = subprocess с постоянной shell-сессией.
    """
    SHELL: str = "/bin/bash"

    def __init__(self, address: str = "localhost", **kwargs):
        self._proc: subprocess.Popen | None = None
        super().__init__(address=address, **kwargs)

    def connect(self) -> bool:
        if self.check__connected():
            return True
        try:
            self._proc = subprocess.Popen(
                [self.SHELL, "-i"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
            )
            return True
        except Exception as e:
            print(f"Direct connect error: {e}")
            return False

    def disconnect(self) -> None:
        try:
            self._proc.terminate()
            self._proc.wait(timeout=1)
        except Exception:
            pass

    def check__connected(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    # TRANSPORT PRIMITIVES — через select/nonblocking
    ...