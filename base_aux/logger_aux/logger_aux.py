from typing import *
import pathlib
import logging
from logging.handlers import RotatingFileHandler


# =====================================================================================================================
def _example_zero():
    LEVEL = logging.DEBUG
    PATTERN = '%(asctime)s[%(levelname)s](%(name)s(%(filename)s).%(funcName)s/thread%(thread)s(line%(lineno)d))%(msg)s'
    formatter = logging.Formatter(PATTERN)

    logger = logging.getLogger()
    logger.setLevel(LEVEL)

    handler_file = logging.FileHandler(f"SerialServer_Base.log")
    handler_file.setLevel(LEVEL)
    handler_file.setFormatter(formatter)
    logger.addHandler(handler_file)

    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(LEVEL)
    handler_stream.setFormatter(formatter)
    logger.addHandler(handler_stream)

    # logger.log(10, 'ЛОГ10')   #DEBUG=ЛОГ10
    # logger.log(11, 'ЛОГ11')   #Level 11=ЛОГ11
    logger.warning('MSG_DEFAULT')     # 2024-03-19 15:27:21,644[WARNING](root(t001.py).<module>/thread18536(line21))MSG_DEFAULT


# =====================================================================================================================
class Logger:
    """
    NOTES:
        DONT use directly root as secondary logger - use it only as first or it would be applyed automatically!
    """

    # SETTINGS ---------------------------------------
    LOG_NAME: None | str = None  # None=self "root"="root", if not StrNone=get ClassName!

    LOG_LEVEL: int = logging.DEBUG
    LOG_PATTERN: str = '%(asctime)s[%(levelname)s]%(name)s(%(filename)s).%(funcName)s(line%(lineno)d)/thread%(thread)s::%(msg)s'

    LOG_DIRPATH: None | pathlib.Path = None

    LOG_FILE_STARTWITH: None | str = None
    LOG_FILE_EXTENTION: None | str = None
    LOG_FILE_MAXBYTES: int = 1024 * 1024 * 10
    LOG_FILE_BACKUPCOUNT: int = 3

    LOG_ENABLE: None | bool = False     # you need to turnON if you need it!
    LOG_USE_STREAM: bool = True
    LOG_USE_FILE: bool = False

    # AUX ---------------------------------------
    _formatter: logging.Formatter
    LOGGER: logging.Logger | None = None

    _handler_stream: logging.StreamHandler | None = None
    _handler_file: logging.FileHandler | None = None

    @property
    def LOG_FILENAME(self) -> str:
        return f"{self.LOG_FILE_STARTWITH or 'logger'}__{self.LOG_NAME or 'root'}.{self.LOG_FILE_EXTENTION or 'log'}"

    @property
    def LOG_FILEPATH(self) -> pathlib.Path:
        if self.LOG_DIRPATH is None:
            return pathlib.Path(self.LOG_FILENAME)
        else:
            return self.LOG_DIRPATH.joinpath(self.LOG_FILENAME)

    def __init__(
            self,
            log_name: None | str | Any = None,
            log_dirpath: None | str | pathlib.Path = None,
            log_level: None | int = None,
            log_use_stream: None | bool = None,
            log_use_file: None | bool = None,
            log_enable: None | bool = None,

            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # PARAMS ------------------------------------------
        if log_name is not None:
            self.LOG_NAME = log_name

        if log_dirpath is not None:
            self.LOG_DIRPATH = pathlib.Path(log_dirpath)

        if log_level is not None:
            self.LOG_LEVEL = log_level

        if log_use_stream is not None:
            self.LOG_USE_STREAM = log_use_stream

        if log_use_file is not None:
            self.LOG_USE_FILE = log_use_file

        if log_enable is not None:
            self.LOG_ENABLE = log_enable

        # PREPARE ------------------------------------------
        # if log_name as istance!
        if self.LOG_NAME is None:
            class_name = self.__class__.__name__
            if class_name == "Logger":
                self.LOG_NAME = "root"
            else:
                self.LOG_NAME = class_name
        elif not isinstance(self.LOG_NAME, str):
            # if set name by passing object
            self.LOG_NAME = self.LOG_NAME.__class__.__name__

        # if not self.__class__.LOGGER:
        #     # place here MRO name??? for classmethods???
        #     # useful for methods starts after inited first instance
        #     self.__class__.LOGGER = logging.getLogger(self.LOG_NAME)

        self.LOGGER = logging.getLogger(self.LOG_NAME)

        # DISABLE ------------------------------------------
        if self.LOG_NAME == "root" and log_enable:
            pass

        elif not self.LOG_ENABLE:
            return

        if self.LOGGER.handlers:  # already created logger from previous inition
            return

        # --------------------------------------------------
        # TODO: create not exists LOG_DIRPATH

        # INIT ---------------------------------------------
        self.LOGGER.setLevel(self.LOG_LEVEL)

        self._formatter = logging.Formatter(self.LOG_PATTERN)

        # CONNECT -------------------------------------------
        if self.LOG_USE_STREAM:
            self.__class__._handler_stream = logging.StreamHandler()
            # self.__class__._handler_stream.setLevel(self.LOG_LEVEL)
            self.__class__._handler_stream.setFormatter(self._formatter)
            self.LOGGER.addHandler(self.__class__._handler_stream)

        if self.LOG_USE_FILE:
            self._handler_file = RotatingFileHandler(self.LOG_FILEPATH, maxBytes=self.LOG_FILE_MAXBYTES, backupCount=self.LOG_FILE_BACKUPCOUNT)
            # self._handler_file.setLevel(self.LOG_LEVEL)
            self._handler_file.setFormatter(self._formatter)
            self.LOGGER.addHandler(self._handler_file)

        # INIT ROOT -----------------------------------------
        # run always after connects!
        self._log_init_root()

        # INITIAL MSG ---------------------------------------
        self.LOGGER.debug("="*100)

        if self.LOG_USE_STREAM:
            self.LOGGER.debug(f"[Logger.{self.LOG_NAME}] start STREAM")

        if self.LOG_USE_FILE:
            self.LOGGER.debug(f"[Logger.{self.LOG_NAME}] start FILE=[{self._handler_file.baseFilename}]")

    @staticmethod
    def _log_init_root(log_enable: bool = None) -> None:
        """
        DONT USE IT DIRECTLY!!!
        it would used always automated!!!
        """
        if not log_enable:
            return
        logger_root = logging.getLogger()
        if not logger_root.hasHandlers():
            Logger(log_enable=log_enable)  # DONT USE cls()!!!


# =====================================================================================================================
if __name__ == "__main__":
    pass


# =====================================================================================================================
