from base_aux.loggers.m2_logger import *
from base_aux.base_types.m2_info import ObjectInfo


# USAGE-1=DIRECT ===================================
logger0 = Logger(log_enable=True)
# ObjectInfo(logger0.LOGGER).print()

# logger0.LOGGER.debug()    # TypeError: Logger.debug() missing 1 required positional argument: 'msg'
logger0.LOGGER.debug(None)  # OK
logger0.LOGGER.debug(True)  # OK
logger0.LOGGER.debug("")    # OK
logger0.LOGGER.debug("hello0-1")

logger1 = Logger("logger_first", log_enable=True)
logger1.LOGGER.debug("hello1-1")

logger2 = Logger("logger_second", log_enable=True)
logger2.LOGGER.debug("hello2-1")

logger0.LOGGER.debug("hello0-2")
logger1.LOGGER.debug("hello1-2")
logger2.LOGGER.debug("hello2-2")

# LOG_DIRPATH -----------------------
logger_dir = Logger("logger_dir", "c:\\1", log_enable=True)
logger_dir.LOGGER.debug("hello_dir")

print(f"{logger_dir.LOG_DIRPATH=}")
print(f"{logger_dir.LOG_FILEPATH=}")


# USAGE-2=NESTING ===================================
class Example(Logger):
    LOG_ENABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def meth(self):
        self.LOGGER.debug("hello123")


Example().meth()

# ObjectInfo(logger0.LOGGER).print()
