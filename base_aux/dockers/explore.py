import os
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

from typing import *
from testcontainers.rabbitmq import RabbitMqContainer
import pika
import time

from base_aux.base_types.m2_info import ObjectInfo


# =====================================================================================================================
def mq_testing_simple_direct():
    """
    GOAL
    ----
    show example usage simple testing
    """
    with RabbitMqContainer(
            image="rabbitmq:3-management",  # версия с веб-интерфейсом

            ports=[5672, "15672"],
            # Container[int | str]
            #   явное указание какие внутренние порты используются и что их нужно пробрасывать!
            #   внешний ответный порт создастся динамически!
            #   если не указать то проброса не последует!
    ) as rabbitmq:
        # ObjectInfo(rabbitmq).print()

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
        channel.queue_declare(queue=QUEUE_TESTING_NAME, durable=True)
        print(f"\t{QUEUE_TESTING_NAME=}")

        index = 0
        while True:
            index += 1
            msg_out = f'TestContainers {index=}'

            # 1=WRITE -------------
            channel.basic_publish(
                exchange='',
                routing_key=QUEUE_TESTING_NAME,
                body=msg_out
            )
            print(msg_out)

            # 2=READ --------------
            method_frame, header_frame, body = channel.basic_get(queue=QUEUE_TESTING_NAME)

            msg_in = body.decode()
            print(f"\t{msg_in == msg_out}/{msg_in=}")

            time.sleep(1)

        connection.close()


# =====================================================================================================================
if __name__ == "__main__":
    mq_testing_simple_direct()


# =====================================================================================================================
