import pathlib
import datetime
from base_aux.aux_text import TextAux

try:
    import git  # GITPYTHON # need try statement! if not installed git.exe raise Exx even if module was setup!!!
except:
    msg = f"[ERROR] git - is not setup in OS"
    print(msg)


# =====================================================================================================================
class Git:
    """
    GOAL
    ----
    get last commit short info instead of hard-version
    """
    # settings -------------
    PATH: pathlib.Path | str = None

    # aux -------------
    REPO: git.Repo = None   # real object/only existed

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, path: pathlib.Path | str = None):
        if path:
            self.PATH = pathlib.Path(path)
        else:
            self.PATH = pathlib.Path.cwd()

        try:
            self.REPO = git.Repo("../..")   # FIXME: need auto find ROOT!!!
            self.REPO = git.Repo(self.PATH)
        except Exception as exx:
            print(f"git.Repo={exx!r}")
            print(f"возможно GIT не установлен")

    def check_ready(self) -> bool:
        """
        GOAL
        ----
        check if all ready to work
        - git setup
        - repo created
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
        pass

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def COMMITTER(self) -> str | None:
        """
        EXAMPLE
        -------
        ndrei Starichenko
        """
        if self.REPO:
            return self.REPO.head.object.committer

    @property
    def BRANCH(self) -> str | None:
        """
        EXAMPLE
        -------
        main
        """
        if self.REPO:
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
        if self.REPO:
            return self.REPO.commit().summary

    @property
    def HEXSHA(self) -> str | None:
        """
        NOTE
        ----
        more useful work with 8 chars! that's enough!

        EXAMPLE
        -------
        9fddeb5a9bed20895d56dd9871a69fd9dee5fbf7
        """
        if self.REPO:
            return self.REPO.head.object.hexsha

    @property
    def HEXSHA8(self) -> str | None:
        """
        derivative for main HEXSHA cut by 8 chars

        EXAMPLE
        -------
        9fddeb5a
        """
        if self.REPO:
            return self.HEXSHA[:8]

    @property
    def DATETIME(self) -> datetime.datetime | None:
        """
        EXAMPLE
        -------
        2024-12-05 11:30:17+03:00
        """
        if self.REPO:
            return self.REPO.head.object.committed_datetime

    # -----------------------------------------------------------------------------------------------------------------
    def info_string(self) -> str:
        """
        EXAMPLE
        -------
        git_mark='[git_mark//main/zero/Andrei Starichenko/ce5c3148/2024-12-04 18:39:10]'
        """
        if self.REPO:
            branch = TextAux(self.BRANCH).shortcut(15)
            summary = TextAux(self.SUMMARY).shortcut(15)
            dt = TextAux(self.DATETIME).shortcut_nosub(19)

            result = f"{branch}/{summary}/{self.COMMITTER}/{self.HEXSHA8}/{dt}"

        else:
            result = f"возможно GIT не установлен"

        git_mark = f"[git_mark//{result}]"
        print(f"{git_mark=}")
        return git_mark


# =====================================================================================================================
if __name__ == '__main__':
    from base_aux.base_objects import *
    ObjectInfo(Git()).print()


# =====================================================================================================================
