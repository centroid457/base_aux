import asyncio
from aio_pika import IncomingMessage
from mq_client import RabbitMQService


async def message_handler(message: IncomingMessage) -> None:
    async with message.process():
        print(f"Received: {message.body.decode()}")
        # Process your message here


async def main():
    rabbitmq = RabbitMQService("amqp://guest:guest@localhost:5672/")

    try:
        # Connect to RabbitMQ
        await rabbitmq.connect()

        # Add consumer
        await rabbitmq.add_consumer("test_queue", message_handler)

        # Publish messages
        for i in range(10):
            await rabbitmq.publish("test_queue", f"Message {i}".encode())
            await asyncio.sleep(1)

        # Keep running
        await asyncio.sleep(60)

    finally:
        await rabbitmq.close()


if __name__ == "__main__":
    asyncio.run(main())