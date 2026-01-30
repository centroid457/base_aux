import pika
import pytest
from testcontainers.rabbitmq import RabbitMqContainer
from base_aux.dockers.m1_docker import DockerMan

import os
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"


# =====================================================================================================================
@pytest.fixture(scope="session")    # scope=SESSION - одно подключение на все тесты одного запуска тестового окружения! экономит время на создание и подключение!!!
def rabbitmq_container():
    assert DockerMan.docker__check_ready_os()

    with RabbitMqContainer("rabbitmq:3-management") as container:
        yield container


@pytest.fixture
def rabbitmq_connection(rabbitmq_container):
    """Фикстура подключения к RabbitMQ"""
    _conn_params = pika.ConnectionParameters(
        host=rabbitmq_container.get_container_host_ip(),
        port=rabbitmq_container.get_exposed_port(5672),
        credentials=pika.PlainCredentials(
            username=rabbitmq_container.username,
            password=rabbitmq_container.password
        )
    )
    connection = pika.BlockingConnection(_conn_params)
    yield connection
    connection.close()


@pytest.fixture
def rabbitmq_channel(rabbitmq_connection):
    """Фикстура канала RabbitMQ"""
    channel = rabbitmq_connection.channel()
    yield channel
    channel.close()


# =====================================================================================================================
