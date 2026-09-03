from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import asyncio
import json
from pathlib import Path
import os

from prj_2_pytest_webui.server.state_manager import StateManager
from prj_2_pytest_webui.server.test_runner import TestRunner
from prj_2_pytest_webui.server.test_collector import TestCollector
from prj_2_pytest_webui.server.config import Config


# Определяем базовую директорию
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()

# Инициализация компонентов
state_manager = StateManager()
test_runner = TestRunner(state_manager)

# Подключение статических файлов
# app.mount("/static", StaticFiles(directory="server/static"), name="static")
# app.mount("/static", StaticFiles(directory=str(Path(__file__).parent.joinpath("static"))), name="static")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    """Главная страница"""
    return FileResponse("server/static/index.html")

@app.get("/api/testplans")
async def get_testplans(root_path: str = "TESTPLANS"):
    """Получение списка тестпланов"""
    try:
        path = Path(root_path)
        if not path.exists():
            raise HTTPException(404, "Directory not found")
        
        testplans = []
        for item in path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                testplans.append({
                    'name': item.name,
                    'path': str(item)
                })
        
        return {'testplans': testplans}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/tests/{testplan}")
async def get_tests(testplan: str, root_path: str = "TESTPLANS"):
    """Получение списка тестов"""
    try:
        tests = await TestCollector.collect_tests(root_path, testplan)
        return {'tests': tests}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/state")
async def get_state():
    """Получение текущего состояния"""
    return state_manager.get_state()

@app.post("/api/run")
async def run_tests(data: Dict[str, str]):
    """Запуск тестов"""
    root_path = data.get('root_path', 'TESTPLANS')
    testplan = data.get('testplan')
    
    if not testplan:
        raise HTTPException(400, "Testplan is required")
    
    # Сохранение выбора
    Config.set_last_selection(root_path, testplan)
    
    # Запуск тестов
    await test_runner.start_tests(root_path, testplan)
    
    return {'status': 'started'}

@app.post("/api/pause")
async def pause_tests():
    """Пауза тестов"""
    await test_runner.pause_tests()
    return {'status': 'paused'}

@app.post("/api/resume")
async def resume_tests():
    """Продолжение тестов"""
    await test_runner.resume_tests()
    return {'status': 'resumed'}

@app.post("/api/stop")
async def stop_tests():
    """Остановка тестов"""
    await test_runner.stop_tests()
    return {'status': 'stopped'}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket для实时 обновлений"""
    await websocket.accept()
    
    async def send_update(data: dict):
        """Отправка обновлений клиенту"""
        await websocket.send_json(data)
    
    # Подписка на обновления
    state_manager.subscribe(send_update)
    
    try:
        while True:
            # Получение сообщений от клиента
            data = await websocket.receive_text()
            # Обработка команд от клиента
            command = json.loads(data)
            
            if command.get('type') == 'get_state':
                await websocket.send_json({
                    'type': 'state',
                    'data': state_manager.get_state()
                })
            elif command.get('type') == 'ping':
                await websocket.send_json({'type': 'pong'})
    
    except WebSocketDisconnect:
        state_manager.unsubscribe(send_update)
    except Exception as e:
        state_manager.unsubscribe(send_update)
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
