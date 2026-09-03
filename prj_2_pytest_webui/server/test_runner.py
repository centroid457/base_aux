import asyncio
import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any
import signal

class TestRunner:
    """Запуск и управление тестами"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.process: Optional[asyncio.subprocess.Process] = None
        self.current_task: Optional[asyncio.Task] = None
    
    async def start_tests(self, root_path: str, testplan: str):
        """Запуск тестов"""
        testplan_path = Path(root_path) / testplan
        
        # Очистка предыдущего состояния
        self.state_manager.reset()
        self.state_manager.update_state(
            status='running',
            testplan=testplan,
            started_at=str(asyncio.get_event_loop().time())
        )
        
        # Команда запуска
        cmd = [
            'pytest',
            str(testplan_path),
            '-v',
            '--tb=short',
            '--color=no'
        ]
        
        # Запуск процесса
        self.process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Запуск чтения вывода
        self.current_task = asyncio.create_task(
            self._monitor_process()
        )
    
    async def _monitor_process(self):
        """Мониторинг процесса тестирования"""
        while True:
            # Чтение stdout
            line = await self.process.stdout.readline()
            if not line:
                break
                
            # Отправка данных через state_manager
            await self.state_manager.notify_subscribers({
                'type': 'output',
                'data': line.decode()
            })
            
            # Обновление состояния из файла
            current_state = self.state_manager.get_state()
            
            # Проверка на остановку
            if current_state.get('stopped'):
                await self.stop_tests()
                break
        
        # Завершение
        await self.process.wait()
        
        if self.process.returncode == 0:
            self.state_manager.update_state(status='idle')
        else:
            self.state_manager.update_state(status='failed')
    
    async def pause_tests(self):
        """Пауза тестов"""
        self.state_manager.set_pause(True)
    
    async def resume_tests(self):
        """Продолжение тестов"""
        self.state_manager.set_pause(False)
    
    async def stop_tests(self):
        """Остановка тестов"""
        if self.process:
            # Мягкая остановка
            self.state_manager.set_stop()
            
            # Ждем завершения текущего теста
            await asyncio.sleep(2)
            
            # Принудительная остановка если нужно
            if self.process.returncode is None:
                self.process.terminate()
                
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    self.process.kill()
            
            self.state_manager.reset()