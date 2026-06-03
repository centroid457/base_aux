import asyncio
import aio_pika
import aiormq
import json
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel


async def callback__consume(message: aio_pika.IncomingMessage) -> None:
    async with message.process():
        try:
            body = message.body.decode()
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = body

            print(f"[RabbitMQ.receive]<<<{data=}")
        except Exception as exc:
            print(f"[RabbitMQ.receive]<<<{exc}")


async def callback__on_reconnect_success(connection: AbstractRobustConnection):
    """
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
    print(f"[callback__on_reconnect]call on success RECONNECTION!!")
    print(f"[callback__on_reconnect]{connection=}")


async def callback__on_close(connection: AbstractRobustConnection, exc: Exception | None = None):
    """
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
    print(f"[callback__on_close]FINISHED on every try")
    try:
        print(f"[callback__on_close]{connection=}")
    except:
        pass
    print(f"[callback__on_close]{exc=}")


async def main():
    while True:
        try:
            connection = await aio_pika.connect_robust(
                url="amqp://guest:guest@localhost:5672/",
                timeout=1,
                # reconnect_interval=1, # не подходит!!! [FAIL]connection exc=TypeError("argument of type 'int' is not iterable")
            )
            print(f"[OK]connection")
            break
        except aiormq.exceptions.AMQPConnectionError as exc:
            #             """
            # ERROR:__main__:[RabbitMQ.connect][WinError 1225] Удаленный компьютер отклонил это сетевое подключение
            #
            print(f"[RabbitMQ.connect]server Started but NOT ACCESSIBLE={exc}")
            await asyncio.sleep(1)

        except Exception as exc:
            # print(f"{type(exc)=}")
            print(f"[RabbitMQ.connect]server NotStarted and so NOT ACCESSIBLE={exc}")
            await asyncio.sleep(1)


    # Добавляем обработчики событий
    connection.reconnect_callbacks.add(callback__on_reconnect_success)
    connection.close_callbacks.add(callback__on_close)

    try:
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("test_queue")

            consumer_tag = await queue.consume(callback__consume)
            print("[OK]Ожидание сообщений...")

            counter = 0
            while True:
                counter += 1
                msg = f"{counter=}"
                msg_bytes = bytes(msg, encoding="utf-8")
                asyncio.create_task(
                    channel.default_exchange.publish(
                        aio_pika.Message(body=msg_bytes),
                        routing_key="test_queue"
                    )
                )
                print(f"\tСообщение отправлено {msg=}")
                await asyncio.sleep(2)

            await asyncio.Event().wait()

    except aio_pika.exceptions.AMQPConnectionError:
        print("[FAIL]Соединение разорвано.")
        await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("[EXIT]Завершение работы...")


if __name__ == "__main__":
    asyncio.run(main())