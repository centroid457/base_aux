import pathlib
from base_aux.classes import Text

try:
    import git  # need try statement! if not installed git.exe raise Exx even if module was setup!!!
except:
    pass


# =====================================================================================================================
def git_get_last_commit_short_info_str(source_path=None):    # starichenko
    """
    return last commit short info
    for git repository found in passed path
    """
    git_obj = None

    if not source_path:
        source_path = pathlib.Path.cwd()

    try:
        git_obj = git.Repo(source_path)
    except Exception as exx:
        print(f"{exx!r}")

    if git_obj:
        committer = git_obj.head.object.committer

        try:
            branch = git_obj.active_branch.name
            branch = Text(source=branch).shortcut(maxlen=15)
        except Exception as exx:
            msg = f"GIT DETACHED HEAD - you work not on last commit on brange! {exx!r}"
            print(msg)
            branch = "*DETACHED_HEAD*"

        summary = git_obj.commit().summary
        summary = Text(source=summary).shortcut(maxlen=15)

        hexsha = git_obj.head.object.hexsha[0:8]

        committed_datetime = str(git_obj.head.object.committed_datetime)[0:19]

        result = f"{branch}/{summary}/{committer}/{hexsha}/{committed_datetime}"

    else:
        result = f"возможно GIT не установлен"

    git_mark = f"[git_mark//{result}]"
    print(f"{git_mark=}")
    return git_mark


# =====================================================================================================================
