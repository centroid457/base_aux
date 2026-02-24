import time
from typing import Any, Callable, Never

import uvicorn
from PyQt5.QtCore import QThread
from fastapi import FastAPI

from base_aux.loggers.m2_logger import Logger
from base_aux.webs.d0_url.m0_url import Url
from base_aux.webs.d3_fastapi.d1_templates.m2_responces import create_app__FastApi_on_object


# =====================================================================================================================
class ServerFastApi_Thread(Logger, QThread):
    """
    WORK IN both LINUX/Win!!!
    """
    PORT: int = 80
    HOST: str = "0.0.0.0"
    # HOST: str = "localhost"
    """
    HOST SETTINGS RULES
    localhost - CANT ACCESS BY HOST_IP! only
        http://localhost/ - OK!
        http://127.0.0.1/ - OK!
        http://192.168.75.140/ - FAIL!!!
    
    0.0.0.0 - ALL ARE OK!!!
        http://localhost/ - OK!
        http://127.0.0.1/ - OK!
        http://192.168.75.140/ - OK!!!
    """

    data: Any = None
    create_app: Callable[[Any], FastAPI] = create_app__FastApi_on_object

    @property
    def ROOT(self) -> str:
        return Url().resolve(host=self.HOST, port=self.PORT)

    def __init__(self, app: FastAPI = None, data: Any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if data is None:
            data = self.data

        if app is None:
            app = self.create_app(data=data)
        self.app = app
        self.data = app.data

    def run(self):
        self.LOGGER.debug("run")
        uvicorn.run(self.app, host=self.HOST, port=self.PORT)

    def start(self, *args, **kwargs):
        super().start()
        time.sleep(1)


# =====================================================================================================================
def start_2__by_thread(app: FastAPI = None) -> Never:
    server = ServerFastApi_Thread(app)
    # server.run()
    server.start()
    server.wait()


# =====================================================================================================================
if __name__ == "__main__":
    start_2__by_thread()


# =====================================================================================================================
