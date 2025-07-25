import time
from typing import *
import requests
from collections import deque
from enum import Enum, auto

from PyQt5.QtCore import QThread

from base_aux.loggers.m2_logger import Logger
from base_aux.servers.m0_url import Url


# =====================================================================================================================
TYPE__RESPONSE = Union[None, requests.Response, requests.ConnectTimeout]
TYPE__REQUEST_BODY = Union[str, dict]


class ResponseMethod(Enum):
    POST = auto()
    GET = auto()


# =====================================================================================================================
class Client_RequestItem(Logger, Url, QThread):
    """
    DONT USE IT AS ONE INSTANCE FOR SEVERAL REQUESTS!!!
    You need keep it only to manage results or sent in further time!

    So Only ONE REQUESTITEM FOR ONE Request!

    create object and wait result by wait() or connect slot finished

    :ivar TIMEOUT_SEND: be careful! it is not so clear! timeout for connection is basically 3 sec!

    """
    # SETTINGS -------------------------------------
    START_ON_INIT: bool = None      # DONT DELETE!!! useful for delayed/pending requests
    TIMEOUT_SEND: float = 1

    RETRY_LIMIT: int | None = 1
    RETRY_TIMEOUT: float = 0.5
    retry_index: int = 0
    SUCCESS_IF_FAIL_CODE: bool | None = None    # need to separate timedout and fail statuscode

    METHOD: ResponseMethod = ResponseMethod.POST

    # INIT ------------------------------------------
    BODY: Optional[TYPE__REQUEST_BODY]
    # REQUEST: Optional[requests.Request]
    RESPONSE: Optional[requests.Response]
    EXX: Union[None, requests.ConnectTimeout, Exception]
    TIMESTAMP: float

    # AUX ------------------------------------------
    INDEX: int | None = None

    def __init__(
            self,
            body: Optional[TYPE__REQUEST_BODY] = None,
            method: Optional[ResponseMethod] = None,

            # url: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str] = None,
    ):
        super().__init__()

        # INITS ------------------------------------
        if method is not None:
            self.METHOD = method

        self.BODY = body
        self.RESPONSE = None
        self.EXX = None
        self.TIMESTAMP = 0

        # if url is None:
        #     url = self.HOST
        if host is not None:
            self.HOST = host
        if port is not None:
            self.PORT = port
        if route is not None:
            self.ROUTE = route

        self.index__init()

        # START ------------------------------------
        if self.START_ON_INIT:
            self.start()

    def index__init(self) -> None:
        if self.__class__.INDEX is None:
            self.__class__.INDEX = 0
        else:
            self.__class__.INDEX += 1

        self.INDEX = self.__class__.INDEX

    def check_success(self) -> bool:
        if self.RESPONSE is None:
            return False

        if self.SUCCESS_IF_FAIL_CODE:
            return True
        else:
            return self.RESPONSE.ok

    def __str__(self) -> str:
        return f"[{self.INDEX=}/len={self.__class__.INDEX+1}/{self.retry_index=}/{self.check_success()=}]{self.EXX=}/{self.RESPONSE=}"

    def __repr__(self) -> str:
        return str(self)

    # ------------------------------------------------------------------------------------------------
    def start(self, *args):
        """
        apply only one thread at once (from stack)!
        """
        if not self.isRunning():
            self.LOGGER.debug("start")

            super().start(*args)

    def run(self) -> None:
        self.LOGGER.debug("run")
        while True:
            self._send()

            # CHECK EXIT ----------------------------------------------
            if self.check_success():
                return

            # retry LIMIT ---------------------
            if self.RETRY_LIMIT and self.retry_index == self.RETRY_LIMIT - 1:
                return

            self.retry_index += 1
            time.sleep(self.RETRY_TIMEOUT)

    def _send(self) -> None:
        self.TIMESTAMP = time.time()
        self.RESPONSE = None
        self.EXX = None

        url = self.resolve()

        with requests.Session() as session:
            try:
                if self.METHOD == ResponseMethod.POST:
                    self.RESPONSE = session.post(url=url, json=self.BODY or {}, timeout=self.TIMEOUT_SEND)
                elif self.METHOD == ResponseMethod.GET:
                    self.RESPONSE = session.get(url=url, timeout=self.TIMEOUT_SEND)
            except Exception as exx:
                self.EXX = exx

        self.LOGGER.debug(self)


# =====================================================================================================================
class Client_RequestsStack(Logger, QThread):
    # SETTINGS -------------------------------------
    REQUEST_CLS: type[Client_RequestItem] = Client_RequestItem

    # AUX ------------------------------------------
    __stack: deque

    def __init__(self):
        super().__init__()
        self.__stack = deque()

    @property
    def stack(self) -> deque:
        return self.__stack

    @property
    def request_active(self) -> Optional[Client_RequestItem]:
        if self.stack:
            return self.stack[0]

    # ------------------------------------------------------------------------------------------------
    def start(self, *args):
        """
        apply only one thread at once (from stack)!
        """
        if not self.isRunning():
            self.LOGGER.debug(f"start {self.request_active}")
            super().start(*args)

    # ------------------------------------------------------------------------------------------------
    def run(self):
        self.LOGGER.debug("[STACK]run")

        # WORK -----------------------------------------
        while len(self.stack):
            self.LOGGER.debug(f"[STACK]run cycle with len={len(self.stack)}")
            self.request_active.run()

            if self.request_active.check_success():
                self.stack.popleft()
            else:
                break

        # FINISH -----------------------------------------
        if self.check_success():
            self.LOGGER.info(f"[STACK] is empty")
        else:
            self.LOGGER.warning(f"[STACK] is stopped [at len={len(self.stack)}] by some errors [exx={self.request_active.EXX=}]")

    def send(self, **kwargs) -> None:
        """
        work usually with POST
        """
        item = self.REQUEST_CLS(**kwargs)
        self.stack.append(item)
        self.LOGGER.debug(f"[STACK].APPEND len={len(self.stack)}")
        self.start()

    def check_success(self) -> bool:
        result = self.request_active is None
        self.LOGGER.debug(result)
        return result


# =====================================================================================================================
