from typing import *
import pathlib
import re
import sys

from base_aux.aux_types.m1_type_aux import TypeAux
from base_aux.cli.m1_cli_user import CliUser
from base_aux.aux_text.m1_text_aux import TextAux

from base_aux.versions.m1_version import Version


# =====================================================================================================================
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
# TODO: FINISH!!!
class PyModule:
    TARGET_NAME: str
    TARGET_VER: str = None

    def __init__(self, name: str):
        # if
        # self.NAME = name
        pass







# =====================================================================================================================
PATTERN_IMPORT__MULTY_COMMA = r"(?:^|\n) *import +(\w+(?:\.\w+)* *(?:, *\w+(?:\.\w+)* *)*) *"
PATTERN_IMPORT__MULTY_COMMA_BRACKETS = r"(?:^|\n) *import +\( *(\w+(?:\.\w+)* *(?:,\s*\w+(?:\.\w+)* *)*) *\) *"
PATTERN_IMPORT__FROM = r"(?:^|\n) *from +(\w+(?:\.\w+)*) +import +"

PATTERNS_IMPORT = [PATTERN_IMPORT__MULTY_COMMA, PATTERN_IMPORT__MULTY_COMMA_BRACKETS, PATTERN_IMPORT__FROM]


# =====================================================================================================================
class CmdPattern:
    """
    USAGE
    -----
    cmd = pattern % (PYTHON_PATH, PARAMETER)
    cmd = CmdPattern.INSTALL_UPGRADE__MODULE % (self.PYTHON_PATH, modules)
    """
    INSTALL__MODULE: str = f"%s -m pip install %s"    # (PYTHON_PATH, MODULE)
    INSTALL__FILE: str = f"%s -m pip install -r %s"   # (PYTHON_PATH, FILE)

    INSTALL_UPGRADE__MODULE: str = f"%s -m pip install --upgrade %s"    # (PYTHON_PATH, MODULE)
    INSTALL_UPGRADE__FILE: str = f"%s -m pip install --upgrade -r %s"   # (PYTHON_PATH, FILE)

    SHOW_INFO: str = f"%s -m pip show %s"                               # (PYTHON_PATH, MODULE)
    UNINSTALL: str = f"%s -m pip uninstall -y %s"                       # (PYTHON_PATH, MODULE)


# =====================================================================================================================
class Packages:
    """
    RULE
    ----
    for all module names you could use
    """
    PKGSET__PyPI_DISTRIBUTION: list[str] = [
        # =============================
        # DISTRIBUTION PyPI
        # -----------------------------
        # new setup
        "build",
        "twine",        # necessary! share project on pypi!
        "setuptools",   # necessary! if not

        # old setup (maybe not all)
        "sdist",                # not necessary! works without it on new!
        "bdist-wheel-name",     # not necessary! works without it on new!

    ]
    PYTHON_PATH: str
    cli: CliUser

    # FILENAME_457: str = "requirements__centoid457.txt"      # FILE WILL NOT GO WITHING MODULE AS PART!
    # FILEPATH_457: pathlib.Path = pathlib.Path(__file__).parent.joinpath(FILENAME_457)

    # def explore(self):
    #     # print(f"{__file__=}")
    #     # print(f"{pathlib.Path(__file__).parent.joinpath(self.FILENAME_457)=}")
    #     # print(f"{pathlib.Path(__file__).parent.joinpath(self.FILENAME_457).exists()=}")
    #
    #     print(self.FILEPATH_457)
    #     print(f"{self.FILEPATH_457.exists()}")

    def __init__(self):
        self.PYTHON_PATH = sys.executable
        self.cli = CliUser()

    # =================================================================================================================
    def install(self, modules: Union[str, list[str]]) -> bool:
        # LIST -----------------------------------------------
        if isinstance(modules, (list, tuple, set, )):
            result = all([self.install(module) for module in modules])
            return result

        # SINGLE -----------------------------------------------
        cmd = CmdPattern.INSTALL__MODULE % (self.PYTHON_PATH, modules)
        self.cli.send(cmd, timeout=60 * 2, print_all_states=False)

        return self.cli.last_finished_success

    def reinstall(self, module: str) -> None:
        """
        # FIXME: NOT TESTES!

        GOAL
        ----
        its not just an idea for the sake of just an idea!
        sometimes (and quite often in my experience) i got error when just updating the module!
        """

        self.uninstall(module)
        self.install(module)

    def upgrade(self, modules: Union[str, list[str]]) -> bool:
        """
        you can use explicit version definitions!
            name==0.0.1

NOT EXISTS
==================================================
[CLI_SEND] [python -m pip install --upgrade singleton-meta]
==================================================
self.counter=1
self.counter_in_list=0
self.last_cmd='python -m pip install --upgrade singleton-meta'
self.last_duration=1.347492
self.last_finished=True
self.last_finished_success=True
self.last_retcode=0
--------------------------------------------------
self.last_stdout=
	|'Collecting singleton-meta'
	|'  Using cached singleton_meta-0.1.1-py3-none-any.whl.metadata (2.8 kB)'
	|'Using cached singleton_meta-0.1.1-py3-none-any.whl (5.4 kB)'
	|'Installing collected packages: singleton-meta'
	|'Successfully installed singleton-meta-0.1.1'
	|''
--------------------------------------------------
self.last_stderr=
--------------------------------------------------
self.last_exx_timeout=None
==================================================



ALREADY OK
==================================================
[CLI_SEND] [python -m pip install --upgrade singleton-meta]
==================================================
self.counter=1
self.counter_in_list=0
self.last_cmd='python -m pip install --upgrade singleton-meta'
self.last_duration=1.39782
self.last_finished=True
self.last_finished_success=True
self.last_retcode=0
--------------------------------------------------
self.last_stdout=
	|'Requirement already satisfied: singleton-meta in c:\\python3.12.0x64\\lib\\site-packages (0.1.1)'
	|''
--------------------------------------------------
self.last_stderr=
--------------------------------------------------
self.last_exx_timeout=None
==================================================



GOOD UPGRADE
==================================================
[CLI_SEND] [python -m pip install --upgrade requirements-checker]
==================================================
self.counter=1
self.counter_in_list=0
self.last_cmd='python -m pip install --upgrade requirements-checker'
self.last_duration=1.367846
self.last_finished=True
self.last_finished_success=True
self.last_retcode=0
--------------------------------------------------
self.last_stdout=
	|'Requirement already satisfied: requirements-checker in c:\\!=starichenko=element\\!=projects\\abc=requirements (0.0.7)'
	|'Collecting requirements-checker'
	|'  Using cached requirements-0.1.0-py3-none-any.whl.metadata (2.2 kB)'
	|'Using cached requirements-0.1.0-py3-none-any.whl (7.8 kB)'
	|'Installing collected packages: requirements-checker'
	|'  Attempting uninstall: requirements-checker'
	|'    Found existing installation: requirements-checker 0.0.7'
	|"    Can't uninstall 'requirements-checker'. No files were found to uninstall."
	|'Successfully installed requirements-checker-0.1.0'
	|''
--------------------------------------------------
self.last_stderr=
--------------------------------------------------
self.last_exx_timeout=None
==================================================



FIXME: sometimes modules have incorrect SHARE!!! maybe need check upgrade after installation!!! and show ERROR!!
ERROR ON DISTRIBUTION
==================================================
[#####################ERROR#####################]
self.counter=1
self.counter_in_list=0
self.last_cmd='python -m pip install --upgrade privates'
self.last_duration=1.392156
self.last_finished=True
self.last_finished_success=False
self.last_retcode=1
--------------------------------------------------
self.last_stdout=
        |'Collecting privates'
        |'  Using cached privates-0.5.4.tar.gz (8.8 kB)'
        |'  Preparing metadata (setup.py): started'
        |"  Preparing metadata (setup.py): finished with status 'error'"
        |''
--------------------------------------------------
self.last_stderr=
        |'  error: subprocess-exited-with-error'
        |'  '
        |'  python setup.py egg_info did not run successfully.'
        |'  exit code: 1'
        |'  '
        |'  [6 lines of output]'
        |'  Traceback (most recent call last):'
        |'    File "<string>", line 2, in <module>'
        |'    File "<pip-setuptools-caller>", line 34, in <module>'
        |'    File "C:\\Users\\a.starichenko\\AppData\\Local\\Temp\\pip-install-u6219r9f\\private-values_f5cf3965eb014632a70ff97372b73571\\setup.py", line 2, in <module>'
        |'      from PROJECT import PROJECT'
        |"  ModuleNotFoundError: No module named 'PROJECT'"
        |'  [end of output]'
        |'  '
        |'  note: This error originates from a subprocess, and is likely not a problem with pip.'
        |'error: metadata-generation-failed'
        |''
        |'Encountered error while generating package metadata.'
        |''
        |'See above for output.'
        |''
        |'note: This is an issue with the package mentioned above, not pip.'
        |'hint: See above for details.'
        |''
--------------------------------------------------
self.last_exx_timeout=None
==================================================
"""
        # LIST -----------------------------------------------
        if isinstance(modules, (list, tuple, set, )):
            result = all([self.upgrade(module) for module in modules])
            return result

        # SINGLE -----------------------------------------------
        cmd = CmdPattern.INSTALL_UPGRADE__MODULE % (self.PYTHON_PATH, modules)
        self.cli.send(cmd, timeout=60 * 2, print_all_states=False)

        # TEXT_CUM ===================================================
        text_cum = f"[{modules}]"
        # RESULT EXISTS ---------------------------------------------
        while True:
            # result EXISTS OLD ---------------------------------------------   # KEEP IT FIRST!!!
            # 'Found existing installation: requirements-checker 0.0.7'
            match = re.search(r'Found existing installation: \S+ (\d+\.\d+\.\d+)\s', self.cli.last_stdout)
            if match:
                text_cum += f"(existed old){match[1]}"
                # -----THIS IDEA IS NOT WORK!!!
                # FIXME: TODO: need check version before send UpdateCmd! then compare and decide to reinstall!!!!
                # self.uninstall(modules)     # need uninstall! for sure!
                # self.install(modules)

                """
[CLI_SEND] [('python -m build --sdist -n', 60)]
.........
==================================================
[#####################ERROR#####################]
self.counter=3
self.counter_in_list=1
self.last_cmd='python -m build --sdist -n'
self.last_duration=0.593
self.last_finished=True
self.last_finished_success=False
self.last_retcode=1
--------------------------------------------------
self.last_stdout=
        |'* Getting build dependencies for sdist...'
        |'running egg_info'
        |'writing buses.egg-info\\PKG-INFO'
        |'writing dependency_links to buses.egg-info\\dependency_links.txt'
        |'writing top-level names to buses.egg-info\\top_level.txt'
        |"reading manifest file 'buses.egg-info\\SOURCES.txt'"
        |"adding license file 'LICENSE'"
        |''
        |'ERROR Backend subprocess exited when trying to invoke get_requires_for_build_sdist'
        |''
--------------------------------------------------
self.last_stderr=
        |'Traceback (most recent call last):'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\pyproject_hooks\\_in_process\\_in_process.py", line 353, in <module>'
        |'    main()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\pyproject_hooks\\_in_process\\_in_process.py", line 335, in main'
        |"    json_out['return_val'] = hook(**hook_input['kwargs'])"
        |'                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\pyproject_hooks\\_in_process\\_in_process.py", line 287, in get_requires_for_build_sdist'
        |'    return hook(config_settings)'
        |'           ^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\build_meta.py", line 330, in get_requires_for_build_sdist'
        |'    return self._get_build_requires(config_settings, requirements=[])'
        |'           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\build_meta.py", line 297, in _get_build_requires'
        |'    self.run_setup()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\build_meta.py", line 497, in run_setup'
        |'    super().run_setup(setup_script=setup_script)'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\build_meta.py", line 313, in run_setup'
        |'    exec(code, locals())'
        |'  File "<string>", line 22, in <module>'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\__init__.py", line 108, in setup'
        |'    return distutils.core.setup(**aux_attr)'
        |'           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_distutils\\core.py", line 184, in setup'
        |'    return run_commands(dist)'
        |'           ^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_distutils\\core.py", line 200, in run_commands'
        |'    dist.run_commands()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_distutils\\dist.py", line 970, in run_commands'
        |'    self.run_command(cmd)'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\dist.py", line 945, in run_command'
        |'    super().run_command(command)'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_distutils\\dist.py", line 989, in run_command'
        |'    cmd_obj.run()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\command\\egg_info.py", line 310, in run'
        |'    self.find_sources()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\command\\egg_info.py", line 318, in find_sources'
        |'    mm.run()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\command\\egg_info.py", line 544, in run'
        |'    self.prune_file_list()'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\command\\egg_info.py", line 610, in prune_file_list'
        |'    base_dir = self.distribution.get_fullname()'
        |'               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_core_metadata.py", line 266, in get_fullname'
        |'    return _distribution_fullname(self.get_name(), self.get_version())'
        |'           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |'  File "C:\\Python3117x64\\Lib\\site-packages\\setuptools\\_core_metadata.py", line 284, in _distribution_fullname'
        |'    canonicalize_version(version, strip_trailing_zero=False),'
        |'    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        |"TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'"
        |''
--------------------------------------------------
self.last_exx_timeout=None
==================================================
[ERROR] cmd_item=('python -m build --sdist -n', 60) in full sequence cmd=[('python -m build --sdist -n', 60), ('python -m build --wheel -n', 60), ('twine upload dist/*', 90)]



[FINISHED] (result=False) - press Enter to close
[FINISHED] (result=False) - press Enter to close
[FINISHED] (result=False) - press Enter to close
[FINISHED] (result=False) - press Enter to close
[FINISHED] (result=False) - press Enter to close
[FINISHED] (result=False) - press Enter to close
                """
                # -----THIS IDEA IS NOT WORK!!!
                break

            # 'Requirement already satisfied: requirements-checker in c:\\!=starichenko=element\\!=projects\\abc=requirements (0.0.7)'
            match = re.search(r'Requirement already satisfied: .+ \((\d+\.\d+\.\d+)\)', self.cli.last_stdout)
            if len(self.cli.last_stdout.split("\n")) == 2 and match:
                text_cum += f"(already new){match[1]}"
                break

            # result NEW VERSION! ---------------------------------------------
            # 'Successfully installed singleton-meta-0.1.1'
            match = re.search(r'Successfully installed \S+-(\d+\.\d+\.\d+)\s', self.cli.last_stdout)
            if match:
                text_cum += f"->{match[1]}(upgraded new)"
                break

            # FINAL STOP
            break

        # FINISH ===================================================
        print(text_cum)
        return self.cli.last_finished_success

    def upgrade_pip(self) -> bool:
        """
        upgrade PIP module
        """
        return self.upgrade("pip")

    def upgrade_prj(self, project: "PROJECT") -> bool:
        """
        upgrade PROJECT module to last

        CREATED specially for ensure upgrade to last version in active GIT-repo (you need to start in from git-repo!)
        """
        while not self.check_prj_installed_latest(project):
            self.upgrade(project.NAME_INSTALL)

        return True

    # =================================================================================================================
    def check_prj_installed_latest(self, project: "PROJECT") -> bool:
        """
        check version is actual latest!
        if prj ver is not same as installed - return False

        CREATED SPECIALLY FOR
        ---------------------
        check prj version before publish in pypi
        """
        prj_name = project.NAME_INSTALL
        ver_prj = project.VERSION

        ver_active = self.version_get_installed(prj_name)
        if not ver_active:
            return False

        print(f"{ver_prj=}/{ver_active=}")
        return Version(ver_active) == ver_prj

    # =================================================================================================================
    def upgrade_file(self, filepath: Union[str, pathlib.Path], bylines: bool = None) -> bool:
        """
        upgrade modules by file requirements.py

        :param bylines: not applied yet! # TODO: supposed to install over direct lines
        """
        filepath = pathlib.Path(filepath)
        if not filepath.exists():
            msg = f"[ERROR] file not found {filepath}"
            print(msg)
            return False

        cmd = CmdPattern.INSTALL_UPGRADE__FILE % (self.PYTHON_PATH, filepath)
        print("-" *20)
        print(f"{filepath=}")
        print(filepath.read_text(encoding="utf8"))
        print("-" *20)
        return self.cli.send(cmd, timeout=60 * 5)

    def check_file(self, file) -> bool:
        """
        # TODO: CREATE
        """
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        pass

    # =================================================================================================================
    def version_get_pypi(self, name: str) -> Optional[str]:
        """
        # TODO: CREATE
        """
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        # TODO: FINISH
        pass

    def version_get_installed(self, name: str) -> Optional[str]:
        """
        get version for module if it installed.

        C:\\Users\\a.starichenko>pip show object-info
        Name: object-info
        Version: 0.1.12
        Summary: print info about object (attributes+properties+methods results)
        Home-page: https://github.com/centroid457/
        Author: Andrei Starichenko
        Author-email: centroid@mail.ru
        License:
        Location: C:\\Python3.12.0x64\\Lib\\site-packages
        Requires:
        Required-by:

        C:\\Users\\a.starichenko>pip show aux_types
        Name: object-info
        Version: 0.1.12
        Summary: print info about object (attributes+properties+methods results)
        Home-page: https://github.com/centroid457/
        Author: Andrei Starichenko
        Author-email: centroid@mail.ru
        License:
        Location: C:\\Python3.12.0x64\\Lib\\site-packages
        Requires:
        Required-by:

        C:\\Users\\a.starichenko>
        """
        cmd = CmdPattern.SHOW_INFO % (self.PYTHON_PATH, name)
        if self.cli.send(cmd, timeout=2, print_all_states=False) and self.cli.last_stdout:
            match = re.search(r'Version: (\d+\.\d+\.\d+)\s*', self.cli.last_stdout)
            if match:
                return match[1]

    def check_installed(self, modules: Union[str, list[str]]) -> bool:
        # LIST -----------------------------------------------
        if isinstance(modules, (list, tuple, set, )):
            for module in modules:
                if not self.check_installed(module):
                    return False
            return True

        # ONE -----------------------------------------------
        return self.version_get_installed(modules) is not None

    def uninstall(self, modules: Union[str, list[str]]) -> None:
        # LIST -----------------------------------------------
        if isinstance(modules, (list, tuple, set, )):
            for module in modules:
                self.uninstall(module)

        # ONE -----------------------------------------------
        if modules in self.PKGSET__PyPI_DISTRIBUTION:
            return

        cmd = CmdPattern.UNINSTALL % (self.PYTHON_PATH, modules)
        self.cli.send(cmd, timeout=120)

    # =================================================================================================================
    @staticmethod
    def parse__requirements(filepath: AnyStr | pathlib.Path) -> list[str]:
        """
        GOAL
        ----
        get req modules from requirements.txt
        so just parse a req file

        SPECIALLY CREATED FOR
        ---------------------
        setup.py - get values for install_requires param!
        """
        filepath = pathlib.Path(filepath)
        if not filepath.exists():
            msg = f"[ERROR] file not found {filepath}"
            print(msg)
            return []

        text = filepath.read_text(encoding="utf8")
        print("-" * 20)
        print(f"{filepath=}")
        print(f"{text=}")
        print("-" * 20)

        result = TextAux(text).requirements__get_list()

        return result

    @staticmethod
    def parse_import_modules__txt(text: AnyStr, patterns: list[AnyStr] | AnyStr) -> list[str]:
        """
        GOAL
        ----
        get imported modules from text (python sourcecode)
        get only root names (no parts like pkg.module)
        """
        # SINGLE -------------
        if not TypeAux(patterns).check__iterable_not_str():
            patterns = [patterns, ]

        # ITERABLE -------------
        result = []
        for pattern in patterns:
            items = re.findall(pattern, text)
            for modules_txt in items:
                modules_txt = re.sub(r"\s*", "", modules_txt)
                modules_list = modules_txt.split(",")
                for module_new in modules_list:
                    module_path = module_new.split(".")
                    module_root = module_path[0]
                    if module_root not in result:
                        result.append(module_root)
        return result

    @classmethod
    def find_in_files(
            cls,
            patterns: list[AnyStr] | AnyStr,
            path: Union[str, pathlib.Path] | None = None,
            print_empty_files: bool | None = None,
            skip_paths: Union[str, list[str]] | None = None,
            glob_mask: str = '**/*.py',
    ) -> list[str]:
        """
        GOAL
        ----
        find values by patterns in files
        """
        if not TypeAux(patterns).check__iterable_not_str():
            patterns = [patterns, ]

        # PATH -------------------
        if path is None:
            path = pathlib.Path.cwd()
        else:
            path = pathlib.Path(path)

        # skip_paths -------------------
        if skip_paths is None:
            skip_paths = []
        if not TypeAux(skip_paths).check__iterable_not_str():
            skip_paths = [skip_paths, ]

        for skip_path in skip_paths:
            skip_found = re.search(skip_path, str(path))
            if skip_found:
                return []

        # DIRECTORY ====================
        if path.is_dir():
            print("=" * 80)
            print(f"[PARSE FILES]")
            print(f"{path=}")
            print(f"patterns=")
            for pat in patterns:
                print(f"\t[{pat}]")
            print("-" * 80)

            result_for_dir = []
            for file in path.glob(glob_mask):
                result_for_file = cls.find_in_files(patterns=patterns, path=file, skip_paths=skip_paths)
                for item in result_for_file:
                    if item not in result_for_dir:
                        result_for_dir.append(item)

            print("-" * 80)
            print(f"[SUMMARY MATCHES]:")
            for item in  result_for_dir:
                print(f"\t{item}")
            print("=" * 80)
            return result_for_dir

        # SINGLE FILE ================
        if not path.exists():
            print(f"[not exists]{path=}")
            return []   # or raise?

        file_exx = None
        result_for_file = []
        try:
            filetext = path.read_text(encoding="utf8")
            result_for_file = cls.parse_import_modules__txt(text=filetext, patterns=patterns)
        except Exception as exx:
            file_exx = exx

        if (result_for_file or print_empty_files) or file_exx:
            print(f"{path}".ljust(80, "-"))
            if not file_exx:
                print(f"\t{result_for_file}")
            else:
                print(f"\t{file_exx}")
        return result_for_file

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def parse_text__import(cls, text: AnyStr) -> list[str]:
        """
        GOAL
        ----
        get imported modules from text (python sourcecode)
        get only root names (no parts like pkg.module)
        """
        return cls.parse_import_modules__txt(text, PATTERNS_IMPORT)

    @classmethod
    def parse_files__import(
            cls,
            path: Union[str, pathlib.Path] | None = None,
            print_empty: bool | None = None,
            skip_paths: Union[str, list[str]] | None = None
    ) -> list[str]:
        """
        GOAL
        ----
        get imported modules from file/filesInDirectory (python sourcecode)
        get only root names (no parts like pkg.module)

        return one cumulated list
        """
        return cls.find_in_files(patterns=PATTERNS_IMPORT, path=path, print_empty_files=print_empty, skip_paths=skip_paths)


# =====================================================================================================================
if __name__ == "__main__":
    # Packages.parse_files__import()
    Packages.find_in_files(r"Value_WithUnit", pathlib.Path.cwd().parent.parent, skip_paths=["venv", "t8", "build", ])


# =====================================================================================================================
