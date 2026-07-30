# ---------------------------------------------------------------------------
# 45.4 Пример полной интеграции FastAPI + pytest (упрощённый)
# ---------------------------------------------------------------------------
# Файл: test_server.py (запускается как сервер)

import asyncio
from fastapi import FastAPI, BackgroundTasks
import pytest
import uvicorn

import test__harvest  # модуль с тестами


app = FastAPI()
stop_flag = asyncio.Event()
current_test_task = None


def run_pytest():
    """Фоновый запуск pytest."""
    # Передаём stop_flag в pytest через конфигурацию или глобальную переменную
    test__harvest.stop_flag = stop_flag
    pytest.main(["-v", "test__harvest.py"])

@app.post("/start")
async def start_tests(background_tasks: BackgroundTasks):
    if stop_flag.is_set():
        stop_flag.clear()
    background_tasks.add_task(run_pytest)
    return {"status": "started"}

@app.post("/stop")
async def stop_tests():
    stop_flag.set()
    # Если есть активная асинхронная задача, отменяем её
    if current_test_task and not current_test_task.done():
        current_test_task.cancel()
    return {"status": "stopping"}

# ---------------------------------------------------------------------------
# 45.5 Итоговая стратегия для промышленного тестирования
# ---------------------------------------------------------------------------
# 1. Все тесты, которые могут длиться долго, делать асинхронными
#    и поддерживать отмену (CancelledError).
# 2. Для межтестовой остановки использовать флаг + autouse фикстуру.
# 3. Для экстренных случаев держать скрипт сброса оборудования (вне pytest).
# 4. Не пытаться принудительно прерывать синхронные заблокированные тесты
#    извне – либо переписать их, либо изолировать в отдельные процессы
#    с автоматическим сбросом устройства после завершения процесса.


# =====================================================================================================================
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=80,

        ws_ping_interval=20,  # каждые 20 секунд сервер шлёт ping
        ws_ping_timeout=10  # если pong не пришёл за 10 сек – разрыв
    )


# =====================================================================================================================
