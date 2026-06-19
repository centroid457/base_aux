"""
GOAL
----
start full pipeline from the beginning (without tests!) to the PYPI upload
"""


# =====================================================================================================================
from PROJECT import PROJECT
from base_aux.aux_modules.m1_pkgs import Packages
from base_aux.cmds.m4_cmd_executor import CmdExecutor
from base_aux.base_values.m3_exceptions import *


# =====================================================================================================================
# VERSION = (0, 0, 1)   # first attempt
# VERSION = (0, 0, 2)   # add commented testPypi
# VERSION = (0, 0, 3)   # fix --Verbose!
# VERSION = (0, 0, 4)   # fix param Noisolation! used to be able build with any modules in root PyFiles
# VERSION = (0, 0, 5)   # check latest before build
# VERSION = (0, 0, 6)   # collect all modules into one pkg!
VERSION = (0, 0, 7)     # fix slashes


# =====================================================================================================================
if len(PROJECT.VERSION) > 3:
    msg = f"Dont use more then 3 blocks in {PROJECT.VERSION=} PYPI never accept it!"
    raise Exc__WrongUsage(msg)


# =====================================================================================================================
cli = CmdExecutor()

if not Packages().check_prj_installed_latest(PROJECT):
    print(f"NEED BUILD+PUBLISH+UPGRADE --> START PROCESS")
    # 1=old del --------------
    cli.send("rd dist\\ /q /s", 10)
    cli.send("rd build\\ /q /s", 10)

    # 2=new build+publish --------------
    cmds_timeout = [
        # BUILD new ------------
        ("python -m build --sdist -n", 60),     # Successfully built base_aux-0.3.22.tar.gz
        ("python -m build --wheel -n", 60),     # Successfully built base_aux-0.3.22-py3-none-any.whl

        # SHARE ------------
        # ("twine upload dist/* -r testpypi", 90),  # TESTPYPI
        # ("twine upload dist/* --verbose", 90),    # DONT USE --VERBOSE!!!!
        ("twine upload dist/*", 300),   # 90 makes not enough!!! IF ERROR - increase!

        # RESPONSE ---------------------
        # C:\__STARICHENKO_Element\PROJECTS\abc=base_aux>twine upload dist/*
        # Uploading distributions to https://upload.pypi.org/legacy/
        # Uploading base_aux-0.3.22-py3-none-any.whl
        # 100% ---------------------------------------- 584.6/584.6 kB • 00:01 • 1.0 MB/s
        # Uploading base_aux-0.3.22.tar.gz
        # 100% ---------------------------------------- 426.8/426.8 kB • 00:00 • ?
        #
        # View at:
        # https://pypi.org/project/base-aux/0.3.22/
        #
        # C:\__STARICHENKO_Element\PROJECTS\abc=base_aux>
    ]
    result_publish = cli.send(cmds_timeout)

    # 3=upgrade --------------
    result_upgrade = Packages().upgrade_prj(PROJECT)

    msg = f"[FINISHED] ({result_publish=}/{result_upgrade=}) - press Enter to close"

else:
    msg = f"[FINISHED] ALREADY LATEST - press Enter to close"

# =====================================================================================================================
print()
print()
print()
print(msg)
print(msg)
print(msg)
print(msg)
print(msg)
# ---------
input(msg)


# =====================================================================================================================
