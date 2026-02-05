from typing import *

from urllib.parse import urlparse

from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.path1_dir.m2_dir import *

from base_aux.aux_text.m5_re2_attemps import ReAttemptsFirst

from base_aux.base_types.m2_info import ObjectInfo

try:
    import git  # GITPYTHON # need try statement! if not installed git.exe raise Exc even if module was setup!!!
except:
    print(f"[git.ERROR] is not setup in OS")


# =====================================================================================================================
class Git(DirAux):
    """
    GOAL
    ----
    get last commit short info instead of hard-version

    NOTE
    ----
    noraise
    """
    DIRPATH: TYPING.PATH_FINAL
    _repo: git.Repo = None                   # real object/only existed
    _root_path: TYPING.PATH_FINAL | None = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._repo_init()

    def _repo_init(self) -> TYPING.PATH_FINAL | None:
        """
        GOAL
        ----
        1. detect/find exact root from passed Path (go parent recursively)
        2. create base objects - repo/rootPath
        """
        if not self.check__git_installed():
            return

        while True:
            try:
                self._repo = git.Repo(
                    path=self.DIRPATH,
                    # search_parent_directories=True,   # DONT use here, cause wont get correct _root_path!
                )
                self._root_path = self.DIRPATH
                print(f"[git.INFO] _root_path detected {self._root_path=}")
                return self._root_path
            except git.InvalidGitRepositoryError:
                print(f"[git.WARN] _root_path wrong {self.DIRPATH=}")
                parent = self.DIRPATH.parent
                if parent == self.DIRPATH:
                    return
                else:
                    self.DIRPATH = parent
                    continue
            except BaseException as exc:
                print(f"[git.WARN] _root_path unexpected {exc!r}")

    def get__repo_urls(self) -> list[str]:
        """
        GOAL
        ----
        origin only - what does it mean?
        Получаем URL удаленного репозитория

        usually it gives one value
        ['https://github.com/centroid457/base_aux.git']
        """
        result = []
        if self._repo.remotes:
            for remote in self._repo.remotes:
                if remote.name == 'origin' and remote.urls:
                    result.extend(remote.urls)

        return result

    def get__repo_url(self) -> str | None:
        """
        'https://github.com/centroid457/base_aux.git'
        """
        try:
            pass
            return self.get__repo_urls()[0]
        except:
            return None

    def get__repo_name(self) -> str | None:
        """
        GOAL
        ----
        two variants - from:
        1/ remote url
        2/ root dirpath - if have no remotes! only local repo!
        """
        result = None

        # 1 -----------------------------
        repo_url = self.get__repo_url()  # 'https://github.com/centroid457/base_aux.git'

        try:
            if repo_url:
                result = repo_url.rsplit("/")[-1]
                result = result.rsplit(".")[0]
        except:
            pass

        # 2 -----------------------------
        if not result:
            result = self._root_path.name

        return result

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def check__git_installed() -> bool:
        """
        GOAL
        ----
        show that git is installed!

        NOTE
        ----
        need separate NOT check_ready(repo NOT created/wrong Path) and git not installed
        """
        try:
            import git
            return True
        except Exception as exc:
            print(f"[git.WARN] setup git! {exc!r}")
            return False

    def check__repo_detected(self) -> bool:
        """
        GOAL
        ----
        check if all ready to work
        - git setup
        - root detected
        - repo obj created
        """
        if self._repo:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    def check__repo_status(self) -> bool:
        """
        GOAL
        ----
        check _repo exists + no untracked files + state is not DIRTY (no uncommited changes in indexed files)
        """
        return self.DIRTY is False and not self.UNTRACKED_FILES

    @property
    def DIRTY(self) -> bool | None:
        """
        GOAL
        ----
        check have uncommited changes!
        ONLY CHANGES IN INDEXED FILES!!!
        """
        if self.check__repo_detected():
            return self._repo.is_dirty()

    @property
    def UNTRACKED_FILES(self) -> list[str] | None:
        """
        GOAL
        ----
        return list NOT INDEXED files!
        """
        if self.check__repo_detected():
            return self._repo.untracked_files

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def LIST_BRANCHES(self) -> list[git.Head]:
        """
        GOAL
        ----
        get all branch names
        """
        return [*self._repo.branches]

    def list_commits(self, branch_name: str, limit: int = 10) -> list[git.Head]:
        """
        GOAL
        ----
        get all branch names
        """
        return [branch for branch in self._repo.branches]

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def COMMITTER(self) -> str | None:
        """
        EXAMPLE
        -------
        ndrei Starichenko
        """
        if self.check__repo_detected():
            return self._repo.head.object.committer

    @property
    def BRANCH(self) -> str | None:
        """
        EXAMPLE
        -------
        main
        """
        if self.check__repo_detected():
            try:
                result = self._repo.active_branch.name
            except Exception as exc:
                msg = f"[GIT] DETACHED HEAD - you work not on last commit on brange! {exc!r}"
                print(msg)
                result = "*DETACHED_HEAD*"
            return result

    @property
    def SUMMARY(self) -> str | None:
        """
        actual commit text

        EXAMPLE
        -------
        [Text] add shortcut_nosub
        """
        if self.check__repo_detected():
            return self._repo.commit().summary

    @property
    def HEXSHA(self) -> str | None:
        """
        NOTE
        ----
        see other more useful work with 8 chars! that's enough!

        EXAMPLE
        -------
        9fddeb5a9bed20895d56dd9871a69fd9dee5fbf7
        """
        if self.check__repo_detected():
            return self._repo.head.object.hexsha

    @property
    def HEXSHA8(self) -> str | None:
        """
        GOAL
        ----
        just a short variant for main HEXSHA (cut by last 8 chars)

        EXAMPLE
        -------
        9fddeb5a
        """
        if self.check__repo_detected():
            return self.HEXSHA[:8]

    @property
    def DATETIME(self) -> datetime.datetime | None:
        """
        EXAMPLE
        -------
        2024-12-05 11:30:17+03:00
        """
        if self.check__repo_detected():
            return self._repo.head.object.committed_datetime

    # -----------------------------------------------------------------------------------------------------------------
    def git_mark__get(self) -> str:
        """
        EXAMPLE
        -------
        git_mark='[git_mark//main/zero/Andrei Starichenko/ce5c3148/2024-12-04 18:39:10]'
        """
        if self.check__repo_detected():
            dirty = "!DIRTY!" if self.DIRTY else ""
            untrachked = "!UNTR!" if self.UNTRACKED_FILES else ""
            branch = TextAux(self.BRANCH).shortcut(15)
            summary = TextAux(self.SUMMARY).shortcut(15)
            dt = TextAux(self.DATETIME).shortcut_nosub(19)

            result = f"{dirty}{untrachked}{branch}/{summary}/{self.COMMITTER}/{self.HEXSHA8}/{dt}"

        else:
            result = f"вероятно GIT не установлен"

        git_mark = f"[git_mark//{result}]"
        print(f"{git_mark=}")
        return git_mark

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # fixme: ref and implement below code!

    def is_commit_latest(self) -> bool:
        """
        GOAL
        ----
        check if commit is latest
        just for ensure!
        """
        raise NotImplementedError()

    def pull(self) -> bool:
        """
        GOAL
        ----
        get all updates from server!
        """
        raise NotImplementedError()

    def get_commits(self, branch_name: str, limit: int = 10) -> list[dict[str, str]]:
        """Получает коммиты указанной ветки с ограничением количества"""
        try:
            commits = []
            for commit in self._repo.iter_commits(branch_name, max_count=limit):
                commits.append({
                    'hash': commit.hexsha,
                    'date': commit.committed_datetime.isoformat(),
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'message': commit.message.strip()
                })
            return commits
        except git.GitCommandError:
            return []

    def get_current_state(self) -> Dict[str, str]:
        """Получает текущее состояние репозитория"""
        state = {}

        # Текущая ветка
        try:
            state['current_branch'] = self._repo.active_branch.name
        except TypeError:
            state['current_branch'] = 'DETACHED_HEAD'

        # Текущий коммит
        state['current_hash'] = self._repo.head.commit.hexsha
        state['current_date'] = self._repo.head.commit.committed_datetime.isoformat()
        state['current_author'] = self._repo.head.commit.author.name

        # Информация о проекте
        state['project_name'] = str(self._root_path.name)
        state['repo_path'] = str(self._root_path)

        # Состояние репозитория
        state['is_valid'] = not self._repo.bare
        state['has_changes'] = self._repo.is_dirty()

        # Детальная информация о изменениях
        state['status_details'] = self._get_detailed_status()

        return state

    def _get_detailed_status(self) -> Dict[str, List[str]]:
        """Получает детальную информацию о состоянии файлов"""
        changed_files = [item.a_path for item in self._repo.index.diff(None)]  # Неиндексированные
        staged_files = [item.a_path for item in self._repo.index.diff('HEAD')]  # Индексированные
        untracked_files = self._repo.untracked_files

        return {
            'staged': staged_files,
            'unstaged': changed_files,
            'untracked': untracked_files
        }

    def switch_to_commit(self, branch_name: str, commit_hash: Optional[str] = None) -> Tuple[bool, str]:
        """Переключается на указанную ветку и коммит"""
        try:
            # Переключаемся на ветку
            self._repo.git.checkout(branch_name)

            # Если указан коммит, переключаемся на него
            if commit_hash:
                self._repo.git.checkout(commit_hash)

            return True, "Успешное переключение"
        except git.GitCommandError as e:
            return False, f"Ошибка переключения: {str(e)}"


# =====================================================================================================================
if __name__ == '__main__':
    victim = Git()
    print()
    # print(victim.git_mark__get())
    print(victim.get__repo_name())
    # ObjectInfo(victim._repo).print()


# =====================================================================================================================
