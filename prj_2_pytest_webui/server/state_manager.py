import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, Any
import threading
from datetime import datetime

class StateManager:
    """Менеджер глобального состояния"""
    
    def __init__(self):
        self.state = {
            'status': 'idle',  # idle, running, paused, stopping
            'current_test': None,
            'testplan': None,
            'results': {},
            'started_at': None,
            'paused': False,
            'stopped': False
        }
        self.state_file = Path(".pytest_state.json")
        self._lock = threading.Lock()
        self._subscribers = set()
    
    def update_state(self, **kwargs):
        """Обновление состояния"""
        with self._lock:
            self.state.update(kwargs)
            self._save_state()
    
    def get_state(self) -> dict:
        """Получение текущего состояния"""
        with self._lock:
            return self.state.copy()
    
    def _save_state(self):
        """Сохранение состояния для pytest"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def set_pause(self, paused: bool):
        """Установка паузы"""
        self.update_state(
            paused=paused,
            status='paused' if paused else 'running'
        )
    
    def set_stop(self):
        """Установка остановки"""
        self.update_state(
            stopped=True,
            status='stopping'
        )
    
    def reset(self):
        """Сброс состояния"""
        self.update_state(
            status='idle',
            current_test=None,
            results={},
            started_at=None,
            paused=False,
            stopped=False
        )
    
    async def notify_subscribers(self, data: dict):
        """Уведомление подписчиков"""
        for subscriber in self._subscribers:
            await subscriber(data)
    
    def subscribe(self, callback):
        """Подписка на обновления"""
        self._subscribers.add(callback)
    
    def unsubscribe(self, callback):
        """Отписка от обновлений"""
        self._subscribers.discard(callback)