import json
import pika
from datetime import datetime


# =====================================================================================================================
def test_rabbitmq_connection(rabbitmq_connection):
    """Тест подключения к RabbitMQ"""
    assert rabbitmq_connection.is_open
    assert not rabbitmq_connection.is_closed


def test_queue_creation(rabbitmq_channel):
    """Тест создания очереди"""
    queue_name = "test_queue"

    # Создаем очередь
    result = rabbitmq_channel.queue_declare(
        queue=queue_name,
        durable=True,
        exclusive=False,
        auto_delete=False
    )

    # Проверяем, что очередь создана
    assert result.method.queue == queue_name

    # Проверяем количество сообщений в очереди
    queue_info = rabbitmq_channel.queue_declare(queue=queue_name, passive=True)
    assert queue_info.method.message_count == 0


def test_message_publish_consume(rabbitmq_channel):
    """Тест публикации и потребления сообщений"""
    queue_name = "messages_test"
    test_message = {"id": 1, "data": "test", "timestamp": datetime.now().isoformat()}

    # Создаем очередь
    rabbitmq_channel.queue_declare(queue=queue_name)

    # Публикуем сообщение
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(test_message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Сохраняем сообщение на диске
            content_type='application/json'
        )
    )

    # Получаем сообщение
    method_frame, header_frame, body = rabbitmq_channel.basic_get(
        queue=queue_name,
        auto_ack=True
    )

    # Проверяем полученное сообщение
    assert method_frame is not None
    assert json.loads(body) == test_message


def test_multiple_messages(rabbitmq_channel):
    """Тест с несколькими сообщениями"""
    queue_name = "bulk_messages"

    # Создаем очередь
    rabbitmq_channel.queue_declare(queue=queue_name)

    # Публикуем 10 сообщений
    messages = []
    for i in range(10):
        message = {"id": i, "text": f"Message {i}"}
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message)
        )
        messages.append(message)

    # Получаем все сообщения
    received_messages = []
    while True:
        method_frame, _, body = rabbitmq_channel.basic_get(
            queue=queue_name,
            auto_ack=True
        )
        if method_frame is None:
            break
        received_messages.append(json.loads(body))

    # Проверяем, что все сообщения получены
    assert len(received_messages) == 10
    assert all(msg in received_messages for msg in messages)


def test_exchanges_and_bindings(rabbitmq_channel):
    """Тест обменников и привязок"""
    exchange_name = "test_exchange"
    queue_name = "bound_queue"
    routing_key = "test.route"

    # Создаем обменник
    rabbitmq_channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='topic',
        durable=True
    )

    # Создаем очередь и привязываем ее
    rabbitmq_channel.queue_declare(queue=queue_name)
    rabbitmq_channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=routing_key
    )

    # Публикуем сообщение через обменник
    test_message = {"event": "user.created"}
    rabbitmq_channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps(test_message)
    )

    # Проверяем, что сообщение получено
    method_frame, _, body = rabbitmq_channel.basic_get(
        queue=queue_name,
        auto_ack=True
    )

    assert method_frame is not None
    assert json.loads(body) == test_message


def test_consumer_with_callback(rabbitmq_channel):
    """Тест потребителя с callback-функцией"""
    queue_name = "callback_queue"
    received_messages = []

    def callback(ch, method, properties, body):
        """Callback-функция для обработки сообщений"""
        received_messages.append(json.loads(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Создаем очередь
    rabbitmq_channel.queue_declare(queue=queue_name)

    # Настраиваем потребителя
    rabbitmq_channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )

    # Публикуем сообщения
    for i in range(3):
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps({"id": i})
        )

    # Обрабатываем сообщения
    for _ in range(3):
        rabbitmq_channel.connection.process_data_events(time_limit=1)

    assert len(received_messages) == 3
    assert all(isinstance(msg, dict) for msg in received_messages)


# =====================================================================================================================
