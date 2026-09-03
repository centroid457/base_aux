# conftest.py
import json
import os
import asyncio
from pathlib import Path
import pytest

# Файл для хранения состояния между pytest и сервером
STATE_FILE = Path(".pytest_state.json")

class TestStateManager:
    """Менеджер состояния для коммуникации с сервером"""
    
    @staticmethod
    def write_state(state: dict):
        """Запись состояния в файл"""
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    
    @staticmethod
    def read_state() -> dict:
        """Чтение состояния из файла"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def check_pause() -> bool:
        """Проверка是否需要 пауза"""
        state = TestStateManager.read_state()
        return state.get('paused', False)
    
    @staticmethod
    def check_stop() -> bool:
        """Проверка是否需要 остановка"""
        state = TestStateManager.read_state()
        return state.get('stopped', False)

@pytest.fixture(autouse=True)
def test_state_check():
    """Автоматическая проверка состояния перед каждым тестом"""
    # Ожидание если пауза активна
    while TestStateManager.check_pause():
        if TestStateManager.check_stop():
            pytest.exit("Test run stopped by user")
        asyncio.sleep(0.5)
    
    # Проверка на остановку
    if TestStateManager.check_stop():
        pytest.exit("Test run stopped by user")
    
    yield

def pytest_runtest_logstart(nodeid, location):
    """Хук при старте теста"""
    state = TestStateManager.read_state()
    state['current_test'] = nodeid
    state['status'] = 'running'
    TestStateManager.write_state(state)

def pytest_runtest_logfinish(nodeid, location):
    """Хук при завершении теста"""
    state = TestStateManager.read_state()
    state['current_test'] = None
    TestStateManager.write_state(state)

def pytest_runtest_logreport(report):
    """Хук для получения результатов тестов"""
    state = TestStateManager.read_state()
    
    if report.when == 'call':
        results = state.get('results', {})
        results[report.nodeid] = {
            'status': report.outcome,
            'duration': report.duration,
            'longrepr': str(report.longrepr) if report.failed else None
        }
        state['results'] = results
        TestStateManager.write_state(state)