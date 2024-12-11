"""
GOAL
----
start full pipeline from the beginning (without tests!) to the PYPI upload
"""


# =====================================================================================================================
from PROJECT import PROJECT
from base_aux.requirements.pkgs import Packages
from base_aux.cli.user import CliUser


# =====================================================================================================================
# VERSION = (0, 0, 1)   # first attempt
# VERSION = (0, 0, 2)   # add commented testPypi
# VERSION = (0, 0, 3)   # fix --Verbose!
# VERSION = (0, 0, 4)   # fix param Noisolation! used to be able build with any modules in root PyFiles
# VERSION = (0, 0, 5)   # check latest before build
# VERSION = (0, 0, 6)   # collect all modules into one pkg!
VERSION = (0, 0, 7)     # fix slashes


# =====================================================================================================================
cli = CliUser()

if not Packages().check_prj_installed_latest(PROJECT):
    print(f"NEED BUILD+PUBLISH+UPGRADE --> START PROCESS")
    # 1=old del --------------
    cli.send("rd dist\\ /q /s", 10)
    cli.send("rd build\\ /q /s", 10)

    # 2=new build+publish --------------
    cmds_timeout = [
        # build new ------------
        ("python -m build --sdist -n", 60),
        ("python -m build --wheel -n", 60),

        # share ------------
        # ("twine upload dist/* -r testpypi", 90),  # TESTPYPI
        # ("twine upload dist/* --verbose", 90),    # DONT USE --VERBOSE!!!!
        ("twine upload dist/*", 90),
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
