import pathlib
from base_aux.classes import Text

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
        pass

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
        if self.REPO:
            return self.REPO.head.object.committer

    @property
    def BRANCH(self) -> str | None:
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
        if self.REPO:
            return self.REPO.commit().summary

    @property
    def HEXSHA(self) -> str | None:
        if self.REPO:
            return self.REPO.head.object.hexsha

    @property
    def DATETIME(self) -> str | None:
        if self.REPO:
            return self.REPO.head.object.committed_datetime

    # -----------------------------------------------------------------------------------------------------------------
    def mark_str(self) -> str:
        """
        EXAMPLE
        -------
        git_mark='[git_mark//main/zero/Andrei Starichenko/ce5c3148/2024-12-04 18:39:10]'
        """
        if self.REPO:
            branch = Text(source=self.BRANCH).shortcut(maxlen=15)
            summary = Text(source=self.SUMMARY).shortcut(maxlen=15)
            dt = str(self.DATETIME)[0:19]

            result = f"{branch}/{summary}/{self.COMMITTER}/{self.HEXSHA[0:8]}/{dt}"

        else:
            result = f"возможно GIT не установлен"

        git_mark = f"[git_mark//{result}]"
        print(f"{git_mark=}")
        return git_mark


# =====================================================================================================================
if __name__ == '__main__':
    Git().mark_str()


# =====================================================================================================================
