import asyncio
import logging
from typing import Callable, Dict, Optional, Any
from aio_pika import connect, Message, Channel
from aio_pika.abc import AbstractRobustConnection, AbstractIncomingMessage
from aio_pika.pool import Pool
from contextlib import asynccontextmanager
import aio_pika


# =====================================================================================================================
logging.basicConfig(
    level=logging.INFO
    # level=logging.DEBUG
)
logger = logging.getLogger(__name__)


# =====================================================================================================================
class RabbitMQService:
    def __init__(self, url: str, max_connections: int = 2, max_channels: int = 10):
        self.url = url
        self.max_connections = max_connections
        self.max_channels = max_channels

        # Pools for connections and channels
        self.connection_pool: Optional[Pool] = None
        self.channel_pool: Optional[Pool] = None

        # Storage for consumers and producers
        self.consumers: Dict[str, asyncio.Task] = {}
        self.consumer_callbacks: Dict[str, Callable] = {}
        self.producer_queues: Dict[str, asyncio.Queue] = {}
        self.producer_tasks: Dict[str, asyncio.Task] = {}

        # Main connection and flags
        self._main_connection: Optional[AbstractRobustConnection] = None
        self._is_running = False
        self._reconnect_task: Optional[asyncio.Task] = None

    # -----------------------------------------------------------------------------------------------------------------
    async def connect(self) -> None:
        """Establish connection with reconnection support"""
        self._is_running = True

        # Create connection pool
        self.connection_pool = Pool(
            self._get_connection,
            max_size=self.max_connections
        )

        # Create channel pool
        self.channel_pool = Pool(
            self._get_channel,
            max_size=self.max_channels
        )

        # Start reconnection monitoring
        self._reconnect_task = asyncio.create_task(self._reconnect_worker())

    async def _get_connection(self) -> AbstractRobustConnection:
        """Get single connection instance"""
        connection = await connect(self.url)
        self._main_connection = connection
        logger.info("Connected to RabbitMQ")
        return connection

    async def _get_channel(self) -> Channel:
        """Get channel from connection pool"""
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def _reconnect_worker(self) -> None:
        """Monitor connection and reconnect if needed"""
        while self._is_running:
            try:
                if (self._main_connection and
                        self._main_connection.is_closed):
                    logger.warning("RabbitMQ connection lost, reconnecting...")
                    await self._reconnect()

                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Reconnection monitor error: {e}")
                await asyncio.sleep(5)

    async def _reconnect(self) -> None:
        """Reconnect and restart all consumers/producers"""
        # Close existing pools
        if self.connection_pool:
            await self.connection_pool.close()
        if self.channel_pool:
            await self.channel_pool.close()

        # Recreate pools
        self.connection_pool = Pool(
            self._get_connection,
            max_size=self.max_connections
        )
        self.channel_pool = Pool(
            self._get_channel,
            max_size=self.max_channels
        )

        # Restart producers
        for queue_name in list(self.producer_tasks.keys()):
            await self._start_producer(queue_name)

        # Restart consumers
        for queue_name, callback in self.consumer_callbacks.items():
            await self._start_consumer(queue_name, callback)

    # -----------------------------------------------------------------------------------------------------------------
    async def add_consumer(
            self,
            queue_name: str,
            callback: Callable[[AbstractIncomingMessage], Any],
            auto_delete: bool = False
    ) -> None:
        """Add consumer with automatic queue creation"""
        self.consumer_callbacks[queue_name] = callback
        await self._start_consumer(queue_name, callback, auto_delete)

    async def _start_consumer(
            self,
            queue_name: str,
            callback: Callable[[AbstractIncomingMessage], Any],
            auto_delete: bool = False
    ) -> None:
        """Start consumer task"""
        # Cancel existing consumer if any
        if queue_name in self.consumers:
            self.consumers[queue_name].cancel()
            try:
                await self.consumers[queue_name]
            except asyncio.CancelledError:
                pass

        # Start new consumer
        self.consumers[queue_name] = asyncio.create_task(
            self._consume_messages(queue_name, callback, auto_delete)
        )

    async def _consume_messages(
            self,
            queue_name: str,
            callback: Callable[[AbstractIncomingMessage], Any],
            auto_delete: bool = False
    ) -> None:
        """Consume messages from queue"""
        while self._is_running:
            try:
                async with self.channel_pool.acquire() as channel:
                    # Declare queue
                    queue = await channel.declare_queue(
                        queue_name,
                        auto_delete=auto_delete,
                        durable=not auto_delete
                    )

                    logger.info(f"Started consuming from queue: {queue_name}")

                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:
                            try:
                                await callback(message)
                            except Exception as e:
                                logger.error(f"Message processing error: {e}")
                                await message.nack(requeue=False)

            except Exception as e:
                logger.error(f"Consumer error for {queue_name}: {e}")
                if self._is_running:
                    await asyncio.sleep(5)  # Wait before reconnection

    # -----------------------------------------------------------------------------------------------------------------
    async def publish(self, queue_name: str, data: bytes) -> None:
        """Publish message to queue (with buffering)"""
        if queue_name not in self.producer_queues:
            self.producer_queues[queue_name] = asyncio.Queue(maxsize=1000)
            await self._start_producer(queue_name)

        await self.producer_queues[queue_name].put(data)

    async def _start_producer(self, queue_name: str) -> None:
        """Start producer task for specific queue"""
        if queue_name in self.producer_tasks:
            self.producer_tasks[queue_name].cancel()
            try:
                await self.producer_tasks[queue_name]
            except asyncio.CancelledError:
                pass

        self.producer_tasks[queue_name] = asyncio.create_task(
            self._produce_messages(queue_name)
        )

    async def _produce_messages(self, queue_name: str) -> None:
        """Produce messages from buffer queue"""
        while self._is_running:
            try:
                async with self.channel_pool.acquire() as channel:
                    # Declare queue
                    await channel.declare_queue(queue_name, durable=True)

                    logger.info(f"Started producer for queue: {queue_name}")

                    while self._is_running:
                        try:
                            # Get message from buffer with timeout
                            data = await asyncio.wait_for(
                                self.producer_queues[queue_name].get(),
                                timeout=1.0
                            )

                            # Create and publish message
                            message = Message(
                                body=data,
                                delivery_mode=2  # persistent
                            )

                            await channel.default_exchange.publish(
                                message,
                                routing_key=queue_name
                            )

                            self.producer_queues[queue_name].task_done()
                            logger.debug(f"Message published to {queue_name}")

                        except asyncio.TimeoutError:
                            continue

            except Exception as e:
                logger.error(f"Producer error for {queue_name}: {e}")
                if self._is_running:
                    await asyncio.sleep(5)  # Wait before reconnection

    # -----------------------------------------------------------------------------------------------------------------
    async def close(self) -> None:
        """Graceful shutdown"""
        logger.info("Shutting down RabbitMQ service...")
        self._is_running = False

        # Stop reconnection monitor
        if self._reconnect_task:
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass

        # Stop all consumers
        for queue_name, task in self.consumers.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self.consumers.clear()

        # Stop all producers and wait for queues to empty
        for queue_name, task in self.producer_tasks.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Wait for all producer queues to empty
        for queue_name, queue in self.producer_queues.items():
            await queue.join()

        self.producer_tasks.clear()
        self.producer_queues.clear()
        self.consumer_callbacks.clear()

        # Close pools
        if self.channel_pool:
            await self.channel_pool.close()
        if self.connection_pool:
            await self.connection_pool.close()

        logger.info("RabbitMQ service shutdown complete")

    @asynccontextmanager
    async def get_channel(self):
        """Context manager for getting channel from pool"""
        async with self.channel_pool.acquire() as channel:
            yield channel


# =====================================================================================================================
