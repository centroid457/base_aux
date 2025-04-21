import random
import json
import string
import time


# Генерация случайного серийного номера
def generate_sn():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    sn = random.choice(letters) + ''.join(random.choice(digits) for _ in range(5))
    return sn


# Генерация случайной записи о первичной производственной площадке
def generate_factory_record():
    factory = {
        "name": "Factory A",
        "stand_number": random.randint(1, 10),
        "shift_number": random.randint(1, 3)
    }
    return factory


# Генерация случайного результата теста
def generate_test_result():
    results = ["PASS", "FAIL"]
    return random.choice(results)


# Генерация случайной ссылки на базу компонент в составе изделия
def generate_components():
    components = {
        "component1": f"Component {random.choice(string.ascii_letters)}",
        "component2": f"Component {random.choice(string.ascii_letters)}"
    }
    return components


# Генерация случайных версий плат и прошивок в составе изделия
def generate_versions():
    versions = {
        "board_version": f"Version {random.randint(1, 5)}",
        "firmware_version": f"Version {random.randint(1, 10)}"
    }
    return versions


# Генерация случайного лога теста
def generate_test_log():
    log = {
        "test_name": "Test A",
        "test_result": generate_test_result(),
        "parameters": {
            "param1": random.randint(1, 100),
            "param2": random.randint(1, 100)
        },
        "log_file": "test_log.txt"
    }
    return log


# Генерация случайной записи истории изделия
def generate_history_record():
    history = {
        "status": random.choice(["Shipped", "Sent for repair", "Rejected", "In stock"]),
        "other_databases": {
            "database1": "Database A",
            "database2": "Database B"
        }
    }
    return history


def generate_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            "sn": generate_sn(),
            "timestamp": int(time.time()),
            "factory_record": generate_factory_record(),
            "test_result": generate_test_result(),
            "components": generate_components(),
            "versions": generate_versions(),
            "test_log": generate_test_log(),
            "history_record": generate_history_record()
        }
        data.append(record)
    return data


# ======================================================
def generate_data_1():
    record = {
        "sn": generate_sn(),
        "timestamp": int(time.time()),
        "factory_record": generate_factory_record(),
        "test_result": generate_test_result(),
        "components": generate_components(),
        "versions": generate_versions(),
        "test_log": generate_test_log(),
        "history_record": generate_history_record()
    }
    return record


# ======================================================
# for name, value in generate_data_1().items():
#     print(f"{name}: {value}")

