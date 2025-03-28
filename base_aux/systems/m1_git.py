import pathlib
import datetime

from base_aux.aux_text.m1_text_aux import TextAux
from base_aux.aux_types.m2_info import ObjectInfo
from base_aux.path1_dir.m2_dir import *


try:
    import git  # GITPYTHON # need try statement! if not installed git.exe raise Exx even if module was setup!!!
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
    REPO: git.Repo = None                   # real object/only existed
    ROOT: TYPING.PATH_FINAL | None = None

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._root_find()

    def _root_find(self) -> TYPING.PATH_FINAL | None:
        """
        GOAL
        ----
        detect/find exact root from passed Path (go parent recursively)
        """
        if not self.check_installed():
            return

        while True:
            try:
                self.REPO = git.Repo(self.DIRPATH)
                self.ROOT = self.DIRPATH
                print(f"[git.INFO] root detected {self.ROOT=}")
                return self.ROOT
            except git.InvalidGitRepositoryError:
                print(f"[git.WARN] root wrong {self.DIRPATH=}")
                parent = self.DIRPATH.parent
                if parent == self.DIRPATH:
                    return
                else:
                    self.DIRPATH = parent
                    continue
            except Exception as exx:
                print(f"[git.WARN] unexpected {exx!r}")

    # -----------------------------------------------------------------------------------------------------------------
    def check_installed(self) -> bool:
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
        except Exception as exx:
            print(f"[git.WARN] setup git! {exx!r}")
            return False

    def check_detected(self) -> bool:
        """
        GOAL
        ----
        check if all ready to work
        - git setup
        - root found
        - repo obj created
        """
        if self.REPO:
            return True
        else:
            return False

    def check_status(self) -> bool:
        """
        GOAL
        ----
        check if you work in validated repo! no changes from last commit
        """
        # TODO: FINISH!
        pass

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def COMMITTER(self) -> str | None:
        """
        EXAMPLE
        -------
        ndrei Starichenko
        """
        if self.check_detected():
            return self.REPO.head.object.committer

    @property
    def BRANCH(self) -> str | None:
        """
        EXAMPLE
        -------
        main
        """
        if self.check_detected():
            try:
                result = self.REPO.active_branch.name
            except Exception as exx:
                msg = f"[GIT] DETACHED HEAD - you work not on last commit on brange! {exx!r}"
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
        if self.check_detected():
            return self.REPO.commit().summary

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
        if self.check_detected():
            return self.REPO.head.object.hexsha

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
        if self.check_detected():
            return self.HEXSHA[:8]

    @property
    def DATETIME(self) -> datetime.datetime | None:
        """
        EXAMPLE
        -------
        2024-12-05 11:30:17+03:00
        """
        if self.check_detected():
            return self.REPO.head.object.committed_datetime

    # -----------------------------------------------------------------------------------------------------------------
    def git_mark__get(self) -> str:
        """
        EXAMPLE
        -------
        git_mark='[git_mark//main/zero/Andrei Starichenko/ce5c3148/2024-12-04 18:39:10]'
        """
        if self.check_detected():
            branch = TextAux(self.BRANCH).shortcut(15)
            summary = TextAux(self.SUMMARY).shortcut(15)
            dt = TextAux(self.DATETIME).shortcut_nosub(19)

            result = f"{branch}/{summary}/{self.COMMITTER}/{self.HEXSHA8}/{dt}"

        else:
            result = f"вероятно GIT не установлен"

        git_mark = f"[git_mark//{result}]"
        print(f"{git_mark=}")
        return git_mark


# =====================================================================================================================
if __name__ == '__main__':
    from base_aux.aux_types import *
    ObjectInfo(Git().REPO).print()


# =====================================================================================================================
