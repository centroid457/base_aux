import json
from pathlib import Path
from typing import Optional
import threading

class Config:
    """Управление конфигурацией"""
    
    CONFIG_FILE = Path(".webui_config.json")
    _lock = threading.Lock()
    
    @classmethod
    def load(cls) -> dict:
        """Загрузка конфигурации"""
        if cls.CONFIG_FILE.exists():
            with open(cls.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @classmethod
    def save(cls, config: dict):
        """Сохранение конфигурации"""
        with cls._lock:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
    
    @classmethod
    def get_last_selection(cls) -> dict:
        """Получение последнего выбора"""
        config = cls.load()
        return {
            'root_path': config.get('last_root_path', 'TESTPLANS'),
            'testplan': config.get('last_testplan', None)
        }
    
    @classmethod
    def set_last_selection(cls, root_path: str, testplan: str):
        """Сохранение последнего выбора"""
        config = cls.load()
        config['last_root_path'] = root_path
        config['last_testplan'] = testplan
        cls.save(config)