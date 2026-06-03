from typing import *
import asyncio
import aio_pika
import aiormq
import logging
import time
import json
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
    AbstractRobustQueue,
    ConsumerTag,
    AbstractIncomingMessage,
)

from m1_connection_manager import MqConnectionManager


# =====================================================================================================================
logging.basicConfig(
    level=logging.INFO
    # level=logging.DEBUG
)
logger = logging.getLogger(__name__)


# =====================================================================================================================
class Base_Multiton:
    """
    GOAL
    ----
    used only as template
    and show affiliation in nesting chain order
    """
    _multiton: dict[Any, Self]      # ={}    DONT ADD HERE in Base_ any value! but pase it in final!

    # ----------
    # NOTE: DONT USE! CAUSE in final class start super()!!!! and exact this method with raise will call!
    # def __new__(cls, *args, **kwargs):
    #     raise NotImplementedError("[Multiton] redefine __new__ method!")
    # ----------

    def __init__(self, *args, **kwargs):
        # DONT USE!!! in multitons!!!
        # instead use ONLY _init_params!!!
        pass

    def _init_params(
            self,
            *args,  # dont delete! we could use both mandatory/required args and optional kwargs!!!
            **kwargs,
    ) -> None:
        """
        GOAL
        ----
        create params in self by args/kwargs
        in cases where
        """
        pass


# =====================================================================================================================
class MqClient(Base_Multiton):
    """
    GOAL
    ----
    1/ stable reconnection - auto by connect_robust!
    2/ stable consuming (recover on reconnect) - auto by connect_robust!
    3/ stable producing
        collect all data in internal queues (wait connection/reconnection) - manual code

    NOTE
    ----
    - one object for all servers!
    - one instance for one queue (by name) in one server.
    instance (server+queue) can both publish/consume

    ?CONSUMER or PUBLISHER?
    it depends on logic
    and mainly one is exclude other!
    (but in test cases you can use both!)
    """
    DEF__MQ_URL: str = "amqp://guest:guest@localhost:5672/"
    DEF__QUEUE_NAME: str | None = "queue_name"      # both consume+produce

    mq_url: str
    queue_name: str
    _stopped: bool

    # conn -----------
    _connection_obj: Optional[AbstractRobustConnection] = None    # from ConnManager - one obj for one server!

    # queues -----------
    _channel_obj: Optional[AbstractRobustChannel] = None      # one obj for one queue! so keep it in instance!
    _queue_obj: Optional[AbstractRobustQueue] = None          # [in instance] and only for consumer! not for publisher!

    # workers -----------
    _consumer_tag: ConsumerTag | None = None          # [in instance] (only one) and only if consumer was created

    _produce_task: asyncio.Task | None = None       # [in instance] task is only one!
    push_pending: asyncio.Queue                  # [in instance]

    msg_pushing: Any | None

    # -----------------------------------------------------------------------------------------------------------------
    pass    # MULTITON
    _multiton: dict[
        tuple[str, str],    # mq_url + queue name
        Self                # client obj
    ] = {}

    def __new__(
        cls,
        mq_url: str = None,
        queue_name: str = None,
    ):
        mq_url = mq_url or cls.DEF__MQ_URL
        queue_name = queue_name or cls.DEF__QUEUE_NAME
        key = (mq_url, queue_name)

        if key not in cls._multiton:
            instance = super().__new__(cls)      # kwArgs NOT NEED!!!
            instance._init_params(
                mq_url=mq_url,
                queue_name=queue_name,
            )
            cls._multiton[key] = instance
        return cls._multiton[key]

    # -----------------------------------------------------------------------------------------------------------------
    def _init_params(
            self,
            mq_url: str = None,
            queue_name: str = None,
    ) -> None:
        self.mq_url = mq_url or self.DEF__MQ_URL
        self.queue_name = queue_name or self.DEF__QUEUE_NAME
        self.push_pending = asyncio.Queue()
        self.msg_pushing = None
        self._stopped = False

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def is_consuming(self) -> bool:
        """
        GOAL
        ----
        show if client is set (and not stopped) for consuming
        """
        return self._consumer_tag is not None

    @property
    def is_producing(self) -> bool:
        """
        GOAL
        ----
        show if client is set (and not stopped) for producing
        """
        return self._produce_task is not None

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    async def connect_all(cls, timeout: float | None = 5) -> bool | Never:
        connection_tasks = {}
        for (server, queue), inst in cls._multiton.items():
            if server not in connection_tasks:
                connection_tasks[server] = asyncio.create_task(inst.connect(timeout))

        connection_results = await asyncio.gather(*connection_tasks.values())
        return connection_results

    async def connect(self, timeout: float | None = 5) -> bool | Never:
        """
        GOAL
        ----
        just cover main method
        """
        self._stopped = False

        try:
            result = await asyncio.wait_for(self._connect(), timeout)
            logger.info(f"[MqClient.connect]OK")
            return result
        except:
            logger.error(f"[MqClient.connect]/{timeout=}")
            return False

    async def _connect(self) -> bool:
        """
        GOAL
        ----
        create all objects to start working
        """
        try:
            # 1=connection ------------------------
            if self._connection_obj is None or self._connection_obj.is_closed:
                self._connection_obj = await MqConnectionManager.get_connection(self.mq_url)

            if self._connection_obj is None:
                return False

            # 2=channel ------------------------
            self._channel_obj = await self._connection_obj.channel()
            if self._channel_obj is None:
                return False

            # 3=queue ------------------------
            self._queue_obj = await self._channel_obj.declare_queue(
                name=self.queue_name,
                durable=True,
            )
            if self._queue_obj is None:
                return False
        except Exception as exc:
            pass

        return self.is_connected

    @property
    def is_connected(self) -> bool:
        """
        Проверка, что соединение и канал активны и готовы к работе.

        ПОЧЕМУ НУЖНО ПРОВЕРЯТЬ И CONNECTION И CHANNEL
        ---------------------------------------------
        В RabbitMQ соединение (connection) - это транспортный канал (например, TCP-соединение),
        а канал (channel) - это виртуальное соединение внутри него.
        Может быть такая ситуация, когда соединение есть, но канал закрыт (например, из-за ошибки). В этом случае мы не сможем публиковать/потреблять сообщения.
        Поэтому для полной проверки работоспособности нужно убедиться, что и соединение, и канал (если он уже был создан) открыты.

        в RabbitMQ:
        Соединение (Connection) - это физическое TCP-соединение к серверу
        Канал (Channel) - это виртуальное соединение внутри физического соединения
        Каналы не являются потокобезопасными и каждый должен использоваться в одной корутине!!!
        """
        try:
            # 1=Проверка connection
            if self._connection_obj is None:
                return False

            # надежная проверка состояния соединения
            connection_ok = (
                not self._connection_obj.is_closed
                and
                # connected: asyncio.Event
                hasattr(self._connection_obj, 'connected')
                and
                self._connection_obj.connected
                and
                self._connection_obj.connected.is_set()
            )

            # 2=Проверка channel (если он был создан)
            channel_ok = True
            if self._channel_obj is not None:
                channel_ok = (
                    not self._channel_obj.is_closed
                    # and
                    # not self._channel_obj.closed
                )

            return connection_ok and channel_ok

        except (AttributeError, RuntimeError, ConnectionError) as exc:
            logging.error(f"[MqClient]is_connected {exc}")
            return False

    async def wait_connected(self, timeout: float | None = None) -> None | Never | NoReturn:
        """
        GOAL
        ----
        used specially in outer coros! like _push_loop
        so we cant not to use simple busy loops with sleeps!

        IT WORKS/USEFULL/DESIGNED in cases !!!
        """
        try:
            await asyncio.wait_for(self._connection_obj.connected.wait(), timeout)
        except AttributeError:
            raise Exception(f"Incorrect usage! use ONLY AFTER _connection_obj was created!")
        except Exception as exc:
            msg = f"[MqClient]is_connected {exc}"
            logging.error(msg)
            raise Exception(exc)

    # -----------------------------------------------------------------------------------------------------------------
    async def stop_client(self) -> None:
        logging.warning(f"[MqClient] stop_client")
        self._stopped = True

        await self._stop_consumer()
        await self._stop_producer()
        await self._stop_channel_connection()

        logger.info("[MqClient]stopped correctly")

    async def _stop_consumer(self) -> None:
        try:
            await self._queue_obj.cancel(self._consumer_tag)
        except Exception as exc:
            pass

        self._consumer_tag = None
        self._queue_obj = None

    async def _stop_producer(self) -> None:
        await self.wait_pushed(10)

        try:
            self._produce_task.cancel()  # IS NOT AWS! try is not necessary!
        except Exception as exc:
            pass

        try:
            await self._produce_task
        except Exception as exc:        # asyncio.CancelledError
            pass
        self._produce_task = None

    async def _stop_channel_connection(self) -> None:
        try:
            await self._channel_obj.close()
        except Exception as exc:
            pass

        self._channel_obj = None

        try:
            await self._connection_obj.close()
        except Exception as exc:
            pass

        self._connection_obj = None

    # -----------------------------------------------------------------------------------------------------------------
    async def consumer_add(self, callback: Callable[[AbstractIncomingMessage], Any] | None = None) -> bool | NoReturn:
        """
        Запуск потребления сообщений из очереди

        CONSTRAINTS
        -----------
        consumer is only one! dont add several! - it is illogical!
        """
        if self._stopped:
            logger.debug(f"[MqClient] cant consume {self._stopped=}")
            return False

        if self._consumer_tag is not None:
            raise Exception(f"{self.queue_name=}consumer is already added!")

        # 1=prepare callback
        if callback is None:
            callback = self.callback__consumer
            # callback = lambda msg: self.consume_callback(msg)     # or smhow else) - NO not need!!!

        try:
            self._consumer_tag = await self._queue_obj.consume(callback)
            logger.info(f"[MqClient]start_consuming {self.queue_name=}/{callback=}")
        except Exception as exc:
            logger.error(f"[MqClient]start_consuming {exc}")

        return self._consumer_tag is not None

    @staticmethod
    async def callback__consumer(message: aio_pika.IncomingMessage) -> None:
        """
        GOAL
        ----
        show example and use in tests
        """
        async with message.process():
            try:
                body = message.body.decode()
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    data = body

                logger.info(f"[MqClient]CONSUMED<<<{data=}")
            except Exception as exc:
                logger.error(f"[MqClient]CONSUME {exc}")
                # В реальном приложении здесь может быть логика повторной обработки
                # await message.reject(requeue=False)

        # ------ multy example
        # def callback(ch, method, properties, body):
        #     message = json.loads(body)
        #     task_type = message.get('type')
        #
        #     if task_type == 'send_email':
        #         process_email(message)
        #     elif task_type == 'generate_report':
        #         process_report(message)
        #     elif task_type == 'update_cache':
        #         process_cache(message)
        #     # Добавить новый тип задачи - просто добавить новый elif

    # -----------------------------------------------------------------------------------------------------------------
    async def produce(self, data: Any) -> bool:
        """
        GOAL
        ----
        on first call - start task loop!
        put data in FIFI queue
        """
        if self._stopped:
            logger.error(f"[MqClient] cant produce {self._stopped=}")
            return False

        if self._produce_task is None:
            self._produce_task = asyncio.create_task(self._push_loop())

        await self.push_pending.put(data)
        logger.info(f"[MqClient]push_pending ADD size={self.push_pending.qsize()}/{data=}")
        return True

    def pushing__get_msg_body(self) -> Any | NoReturn:
        """
        GOAL
        ----
        prepare original msg into JSON
        """
        msg_pushing = self.msg_pushing
        if isinstance(msg_pushing, str):
            result = msg_pushing.encode()
        elif isinstance(msg_pushing, bytes):
            result = msg_pushing
        else:
            result = json.dumps(msg_pushing).encode()
        return result

    async def _push_loop(self) -> None:
        logger.info(f"[MqClient]_push__loop.STARTED {self.queue_name=}")
        msg_body = None

        while True:
            if self._stopped:
                logger.debug(f"[MqClient] _push_loop {self._stopped=}")
                return

            try:
                await self.wait_connected()

                if self.msg_pushing is None:
                    self.msg_pushing = await self.push_pending.get()
                    msg_body = self.pushing__get_msg_body()  # TODO: add TRY!

                await self._channel_obj.default_exchange.publish(
                    message=aio_pika.Message(body=msg_body),
                    routing_key=self.queue_name
                )
                self.msg_pushing = None
                logger.info(f"[MqClient]PUSHED pending={self.push_pending.qsize()}/{msg_body=}")

            except asyncio.CancelledError:
                logger.info("[MqClient] _push_loop cancelled")
                break

            except Exception as exc:
                logger.error(f"[MqClient]PUSH {exc}")
                await asyncio.sleep(1)

    async def wait_pushed(self, timeout: float = 3) -> bool:
        """
        GOAL
        ----
        wait ready to finish working
        for tests/explore
        """
        size_last = None
        time_start__last_size_changed = time.time()

        while not self.push_pending.empty():
            # 1=init first step
            if size_last is None:
                size_last = self.push_pending.qsize()

            # 2=update timeStart
            if size_last != self.push_pending.qsize():
                time_start__last_size_changed = time.time()
                await asyncio.sleep(1)
                continue

            # 3=timeout exit
            if time.time() > time_start__last_size_changed + timeout:
                break
            else:
                await asyncio.sleep(1)

        return self.push_pending.empty()


# =====================================================================================================================
async def main():
    """
    usage example
    """
    victim = MqClient(
        mq_url="amqp://guest:guest@localhost:5672/",
        queue_name="test_queue"
    )

    if await victim.connect():
        for index in range(5):
            await victim.produce(f"msg_{index}")

        await asyncio.sleep(1)
        await victim.consumer_add()

        await victim.wait_pushed()
        await victim.stop_client()


# =====================================================================================================================
if __name__ == "__main__":
    asyncio.run(main())


# =====================================================================================================================
