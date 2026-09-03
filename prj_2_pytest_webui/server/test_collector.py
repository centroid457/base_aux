import subprocess
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

class TestCollector:
    """Сбор информации о тестах"""
    
    @staticmethod
    async def collect_tests(root_path: str, testplan: str) -> List[Dict]:
        """Получение списка тестов через pytest --collect-only"""
        testplan_path = Path(root_path) / testplan
        
        # Запуск pytest с опцией collect-only
        cmd = [
            'pytest',
            str(testplan_path),
            '--collect-only',
            '-q',
            '--json-report'  # Если установлен плагин pytest-json-report
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # Парсинг вывода (можно использовать pytest-json-report для JSON)
            return TestCollector._parse_collection(stdout.decode())
        else:
            # Fallback: использование --collect-only без json
            return TestCollector._parse_collection_text(stdout.decode())
    
    @staticmethod
    def _parse_collection_text(output: str) -> List[Dict]:
        """Парсинг текстового вывода collect-only"""
        tests = []
        current_module = None
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if '::' in line:
                # Формат: module::class::test или module::test
                parts = line.split('::')
                test_info = {
                    'id': line,
                    'name': parts[-1],
                    'type': 'function',
                    'children': []
                }
                
                if len(parts) > 2:
                    test_info['type'] = 'class'
                    test_info['class'] = parts[-2]
                
                tests.append(test_info)
        
        return TestCollector._build_tree(tests)
    
    @staticmethod
    def _build_tree(tests: List[Dict]) -> List[Dict]:
        """Построение дерева тестов"""
        tree = []
        modules = {}
        
        for test in tests:
            module_name = test['id'].split('::')[0]
            
            if module_name not in modules:
                modules[module_name] = {
                    'id': module_name,
                    'name': module_name.split('.')[-1],
                    'type': 'module',
                    'children': []
                }
                tree.append(modules[module_name])
            
            modules[module_name]['children'].append(test)
        
        return tree