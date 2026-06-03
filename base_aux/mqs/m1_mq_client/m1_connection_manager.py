import asyncio
from typing import *
import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
import aiormq
import logging
from contextlib import asynccontextmanager


# =====================================================================================================================
logging.basicConfig(
    level=logging.INFO
    # level=logging.DEBUG
)
logger = logging.getLogger(__name__)


# =====================================================================================================================
async def callback__on_reconnect_success(connection: AbstractRobustConnection) -> None:
    """
    GOAL
    ----
    callback успешного ПЕРЕподключения! здесь просто для логгирования!
    то есть только после успешного подключения с ПРЕДШЕСТВУЮЩЕЙ потерей связи!

    BEHAVIOUR
    =========
1=ON FIRST CONNECT
------------------
not calling!

2=ON EVERY RETRY - with FAIL
----------------------------
not calling

3=ON EVERY RETRY - with SUCCESS
-------------------------------
[callback__on_reconnect]call on success FINISHED!
[callback__on_reconnect]connection=<RobustConnection: "amqp://guest:******@localhost:5672/" 1 channels>
    """
    logger.info(
        msg=f"[callback__on_reconnect]call on success RECONNECTION! {connection!r}",
        extra={"connection": str(connection)}
    )


async def callback__on_close(connection: AbstractRobustConnection, exc: Exception | None = None) -> None:
    """
    GOAL
    ----
    callback кадлой попытки соединения и потери связи!!
    то есть всегда при потере успешного соединения, и всегда при прекращении попытки неуспешного соединения!

    BEHAVIOUR
    =========
1=ON FIRST STOP MQ
------------------
Unexpected connection close from remote "amqp://guest:******@localhost:5672/", Connection.Close(reply_code=320, reply_text="CONNECTION_FORCED - broker forced connection closure with reason 'shutdown'")
NoneType: None
Connection attempt to "amqp://guest:******@localhost:5672/" failed: Server connection unexpectedly closed. Read 0 bytes but 1 bytes expected. Reconnecting after 5 seconds.
[callback__on_close]FINISHED on every try
[callback__on_close]connection=<RobustConnection: "amqp://guest:******@localhost:5672/" 1 channels>

2=ON EVERY RETRY
----------------
[callback__on_close]FINISHED on every try
[callback__on_close]connection=<RobustConnection: "amqp://guest:******@localhost:5672/" 1 channels>
[callback__on_close]exc=TimeoutError()
    """
    extra = {
        "connection": None,
        "exception": str(exc) if exc else None,
    }
    try:
        extra["connection"] = str(connection)
    except:
        pass

    logger.info(
        msg="[callback__on_close]FINISHED on every try",
        extra=extra,
    )


# =====================================================================================================================
class MqConnectionManager:
    """
    GOAL
    ----
    manager for connecting with several servers,
    so for URL_server we can get all correspond objects or create if not exists

    DEMAND
    ------
    1. you want
        - connect to several MqServers
        - access for they objects by UrlName!
        - use Lock object by name.
    """
    _connections: dict[str, AbstractRobustConnection] = {}
    _locks: dict[str, asyncio.Lock] = {}
    _connection_count: dict[str, int] = {}  # Для отслеживания использования / для WITH!!!

    def __init__(self) -> NoReturn:
        raise Exception(f"use always by class! do not instantiate!")

    @classmethod
    async def get_connection(cls, mq_url: str) -> AbstractRobustConnection | Never:
        """
        GOAL
        ----
        create or get already created connection Obj by url
        MAIN meth
        """
        already_exists = mq_url in cls._locks

        if already_exists:
            lock = cls._locks[mq_url]
        else:
            lock = asyncio.Lock()

        async with lock:
            if not already_exists:
                # do smth
                cls._connection_count[mq_url] = 0
                pass

            connection = cls._connections.get(mq_url)
            if connection is None or connection.is_closed:
                count_retry = 0
                while True:
                    count_retry += 1
                    try:
                        connection_new = await aio_pika.connect_robust(
                            url=mq_url,
                            timeout=1,
                            # reconnect_interval=1, # не подходит!!! [FAIL]connection exc=TypeError("argument of type 'int' is not iterable")
                        )
                        logger.info(f"[RabbitMQ.connection_new]{mq_url=}/{count_retry=}")

                        cls._connections[mq_url] = connection_new

                        # Добавляем обработчики событий
                        connection_new.reconnect_callbacks.add(callback__on_reconnect_success)
                        connection_new.close_callbacks.add(callback__on_close)

                        break
                    except aiormq.exceptions.AMQPConnectionError as exc:
                        #             """
                        # ERROR:__main__:[RabbitMQ.connect][WinError 1225] Удаленный компьютер отклонил это сетевое подключение
                        #
                        logger.error(f"[RabbitMQ.connect]server Started but NOT ACCESSIBLE={mq_url=}/{count_retry=}/{exc!r}")
                        await asyncio.sleep(1)

                    except Exception as exc:
                        # print(f"{type(exc)=}")
                        logger.error(f"[RabbitMQ.connect]server NotStarted and so NOT ACCESSIBLE={mq_url=}/{count_retry=}/{exc!r}")
                        await asyncio.sleep(1)

                    except BaseException as exc:
                        logger.error(f"[RabbitMQ.connect]Unexpected={exc!r}")
                        await asyncio.sleep(1)

            cls._connection_count[mq_url] += 1

        return cls._connections[mq_url]

    @classmethod
    async def close_connection(cls, mq_url: str) -> None:
        if mq_url not in cls._connection_count:
            return

        cls._connection_count[mq_url] -= 1
        if cls._connection_count[mq_url] <= 0:
            async with cls._locks[mq_url]:
                if mq_url in cls._connections and not cls._connections[mq_url].is_closed:
                    await cls._connections[mq_url].close()
                cls._connections.pop(mq_url, None)
                cls._locks.pop(mq_url, None)
                cls._connection_count.pop(mq_url, None)

    @classmethod
    async def close_all(cls):
        for url in list(cls._connections.keys()):
            await cls.close_connection(url)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    @asynccontextmanager
    async def connection(cls, mq_url: str):
        """asynccontextmanager"""
        connection = await cls.get_connection(mq_url)
        try:
            yield connection
        finally:
            await cls.close_connection(mq_url)


# =====================================================================================================================
async def main():
    """
    usage example
    """
    url_server = "amqp://guest:guest@localhost:5672/"
    connection = await MqConnectionManager.get_connection(url_server)
    async with connection:
        channel = await connection.channel()

        msg = f"TEST_MSG"
        msg_bytes = bytes(msg, encoding="utf-8")

        await channel.default_exchange.publish(
            aio_pika.Message(body=msg_bytes),
            routing_key="test_queue"
        )
        print(f"\tСообщение отправлено {msg=}")


# =====================================================================================================================
if __name__ == "__main__":
    asyncio.run(main())


# =====================================================================================================================
