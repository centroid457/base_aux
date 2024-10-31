import pathlib
import shutil
import os
import stat
# import fsutil


# =====================================================================================================================
VERSION = (0, 0, 1)   # just add version


# =====================================================================================================================
path_cwd = pathlib.Path.cwd()
path_new = path_cwd.parent.joinpath("!=NewProject")

shutil.copytree(src=path_cwd, dst=path_new)

def remove_readonly(func, path, _):
    """
    Clear the readonly bit and reattempt the removal
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

for dirpath in [".git", ".idea"]:
    shutil.rmtree(path_new.joinpath(dirpath), onerror=remove_readonly)

for filepath in [pathlib.Path(__file__).name, ]:
    path_new.joinpath(filepath).unlink(missing_ok=True)


# =====================================================================================================================
