import asyncio
import aio_pika


async def publish():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    async with connection:
        channel = await connection.channel()
        async with channel:
            for msg in [
                "Hello World!",
                "12",
            ]:
                msg_bytes = bytes(msg, encoding="utf-8")
                await channel.default_exchange.publish(
                    aio_pika.Message(body=msg_bytes),
                    routing_key="test_queue"
                )
            print("Сообщение отправлено")


asyncio.run(publish())
