import os
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

from typing import *
from testcontainers.rabbitmq import RabbitMqContainer
import pika
import time

with RabbitMqContainer(
        image="rabbitmq:3-management",  # версия с веб-интерфейсом

        ports=[5672, "15672"],
        # Container[int | str]
        #   явное указание какие внутренние порты используются и что их нужно пробрасывать!
        #   внешний ответный порт создастся динамически!
        #   если не указать то проброса не последует!
) as rabbitmq:
    QUEUE_TESTING_NAME = "queue_testing"

    # 1=получение актуальных данных --------
    host = rabbitmq.get_container_host_ip()
    amqp_port = rabbitmq.get_exposed_port(5672)
    http_port = rabbitmq.get_exposed_port(15672)

    print(f"RabbitMQ запущен:")
    print(f"\t{amqp_port=}")
    print(f"\t{http_port=}")
    print(f"\tВеб-интерфейс: http://{host}:{http_port}")
    print(f"\tЛогин/пароль: guest/guest")

    # 2=использование сервиса --------------
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=amqp_port)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_TESTING_NAME)
    print(f"\t{QUEUE_TESTING_NAME=}")

    index = 0
    while True:
        index += 1
        msg = f'TestContainers {index=}'
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_TESTING_NAME,
            body=msg
        )
        print(msg)
        time.sleep(1)

    connection.close()
