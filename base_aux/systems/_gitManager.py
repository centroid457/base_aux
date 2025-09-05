# DEEP SEEK

import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
try:
    from git import Repo, GitCommandError, InvalidGitRepositoryError
    GITPYTHON_AVAILABLE = True
except ImportError:
    GITPYTHON_AVAILABLE = False


# =====================================================================================================================
class GitPythonManager:
    def __init__(self, repo_path: str):
        if not GITPYTHON_AVAILABLE:
            raise ImportError("GitPython не установлен. Установите: pip install GitPython")
        
        self.repo_path = os.path.abspath(repo_path)
        try:
            self.repo = Repo(self.repo_path)
        except InvalidGitRepositoryError:
            raise ValueError(f"Путь {self.repo_path} не является валидным Git репозиторием")
    
    # def get_branches(self) -> List[Dict[str, str]]:
    #     """Получает список всех веток проекта"""
    #     branches = []
    #
    #     # Локальные ветки
    #     for branch in self.repo.branches:
    #         branches.append({
    #             'name': branch.name,
    #             'type': 'local',
    #             'hash': branch.commit.hexsha
    #         })
    #
    #     # Удаленные ветки
    #     for remote in self.repo.remotes:
    #         for ref in remote.refs:
    #             branches.append({
    #                 'name': ref.name,
    #                 'type': 'remote',
    #                 'hash': ref.commit.hexsha if hasattr(ref, 'commit') else 'unknown'
    #             })
    #
    #     return branches
    
    def get_commits(self, branch_name: str, limit: int = 10) -> list[dict[str, str]]:
        """Получает коммиты указанной ветки с ограничением количества"""
        try:
            commits = []
            for commit in self.repo.iter_commits(branch_name, max_count=limit):
                commits.append({
                    'hash': commit.hexsha,
                    'date': commit.committed_datetime.isoformat(),
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'message': commit.message.strip()
                })
            return commits
        except GitCommandError:
            return []
    
    def get_current_state(self) -> Dict[str, str]:
        """Получает текущее состояние репозитория"""
        state = {}
        
        # Текущая ветка
        try:
            state['current_branch'] = self.repo.active_branch.name
        except TypeError:
            state['current_branch'] = 'DETACHED_HEAD'
        
        # Текущий коммит
        state['current_hash'] = self.repo.head.commit.hexsha
        state['current_date'] = self.repo.head.commit.committed_datetime.isoformat()
        state['current_author'] = self.repo.head.commit.author.name
        
        # Информация о проекте
        state['project_name'] = os.path.basename(self.repo_path)
        state['repo_path'] = self.repo_path
        
        # Состояние репозитория
        state['is_valid'] = not self.repo.bare
        state['has_changes'] = self.repo.is_dirty()
        
        # Детальная информация о изменениях
        state['status_details'] = self._get_detailed_status()
        
        return state
    
    def _get_detailed_status(self) -> Dict[str, List[str]]:
        """Получает детальную информацию о состоянии файлов"""
        changed_files = [item.a_path for item in self.repo.index.diff(None)]  # Неиндексированные
        staged_files = [item.a_path for item in self.repo.index.diff('HEAD')]  # Индексированные
        untracked_files = self.repo.untracked_files
        
        return {
            'staged': staged_files,
            'unstaged': changed_files,
            'untracked': untracked_files
        }
    
    def switch_to_commit(self, branch_name: str, commit_hash: Optional[str] = None) -> Tuple[bool, str]:
        """Переключается на указанную ветку и коммит"""
        try:
            # Переключаемся на ветку
            self.repo.git.checkout(branch_name)
            
            # Если указан коммит, переключаемся на него
            if commit_hash:
                self.repo.git.checkout(commit_hash)
            
            return True, "Успешное переключение"
        except GitCommandError as e:
            return False, f"Ошибка переключения: {str(e)}"


# =====================================================================================================================
# Универсальный менеджер с выбором реализации
class UniversalGitManager:
    def __init__(self, repo_path: str, use_gitpython: bool = True):
        """
        Универсальный менеджер Git репозиториев
        
        :param repo_path: путь к репозиторию
        :param use_gitpython: использовать GitPython если доступен
        """
        self.use_gitpython = use_gitpython and GITPYTHON_AVAILABLE
        
        if self.use_gitpython:
            self.manager = GitPythonManager(repo_path)
            self.impl_type = "GitPython"
        else:
            # Здесь можно добавить реализацию через subprocess
            self.impl_type = "subprocess"
            raise NotImplementedError("Реализация через subprocess не добавлена")
    
    def get_implementation_type(self) -> str:
        return self.impl_type
    
    # Прокси-методы к выбранной реализации
    def get_branches(self):
        return self.manager.get_branches()
    
    def get_commits(self, branch_name, limit=10):
        return self.manager.get_commits(branch_name, limit)
    
    def get_current_state(self):
        return self.manager.get_current_state()
    
    def switch_to_commit(self, branch_name, commit_hash=None):
        return self.manager.switch_to_commit(branch_name, commit_hash)

# Пример использования
if __name__ == "__main__":
    repo_path = input("Введите путь к Git репозиторию: ").strip()
    
    try:
        # Автоматический выбор лучшей реализации
        manager = UniversalGitManager(repo_path)
        print(f"✓ Используется реализация: {manager.get_implementation_type()}")
        
        # Тестирование функционала
        print("\nТекущее состояние:")
        state = manager.get_current_state()
        print(f"Ветка: {state['current_branch']}")
        print(f"Коммит: {state['current_hash'][:8]}")
        
        print("\nВетки:")
        for branch in manager.get_branches()[:5]:  # Первые 5 веток
            print(f"  - {branch['name']}")
        
    except Exception as e:
        print(f"Ошибка: {e}")