import pathlib

from PROJECT import PROJECT

from base_aux.aux_modules.m1_pkgs import Packages

# =====================================================================================================================
# VERSION = (0, 0, 1)   # use direct upgrade this module by PROJECT.NAME_INSTALL
# VERSION = (0, 0, 2)   # apply upgrade_prj
VERSION = (0, 0, 3)     # collect all modules into one pkg!


# =====================================================================================================================
pkgs_cli = Packages()

print()
print("1=pip==================================================")
pkgs_cli.upgrade_pip()

print()
print("2=this project=========================================")
pkgs_cli.upgrade_prj(PROJECT)

print()
print("4=requirements.txt=====================================")
filepath = pathlib.Path(__file__).parent.parent.joinpath("requirements.txt")
pkgs_cli.upgrade_file(filepath)


# EXIT PAUSE ==========================================================================================================
# for i in range(10, 0, -1):
#     print(f"exit in [{i}] seconds")
#     time.sleep(1)

msg = f"[FINISHED] press Enter to close"
print(msg)
print(msg)
print(msg)
print(msg)
print(msg)
# ---------
input(msg)


# =====================================================================================================================
