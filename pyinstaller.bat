REM pyinstaller.exe --onefile --noconsole ../start.py
REM you should delete previouse ./pyinstaller/ before starting!
pyinstaller.exe^
    --clean^
    --distpath ./pyinstaller/dist^
    --workpath ./pyinstaller/build^
    --specpath ./pyinstaller^
    --onefile^
    --debug all^
    -y^
    ./start.py



pause
=======================================================================================================================
EXISTS SOME CHANGES
-----------------------------------------------------------------------------------------------------------------------
    --hidden-import TESTCASES^
        # УЖЕ ЧТОТО ПЫТАЕТСЯ
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_260_off]
        touch TESTCASES item='tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI148282\TESTCASES): find_spec: called with fullname='TESTCASES.tc7_hv_thresh_base', target='TESTCASES.tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI148282\TESTCASES): find_spec: 'TESTCASES.tc7_hv_thresh_base' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI148282\TESTCASES): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI148282\\TESTCASES').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI148282\TESTCASES): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]



=======================================================================================================================
NOT COMPILED
-----------------------------------------------------------------------------------------------------------------------
    --copy-metadata TESTCASES^

          File "C:\Python3127x64\Lib\site-packages\PyInstaller\utils\hooks\__init__.py", line 970, in copy_metadata
            dist = importlib_metadata.distribution(package_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 862, in distribution
            return Distribution.from_name(distribution_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 399, in from_name
            raise PackageNotFoundError(name)
        importlib.metadata.PackageNotFoundError: No package metadata was found for TESTCASES

    --copy-metadata ./TESTCASES^
          File "C:\Python3127x64\Lib\site-packages\PyInstaller\utils\hooks\__init__.py", line 970, in copy_metadata
            dist = importlib_metadata.distribution(package_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 862, in distribution
            return Distribution.from_name(distribution_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 399, in from_name
            raise PackageNotFoundError(name)
        importlib.metadata.PackageNotFoundError: No package metadata was found for ./TESTCASES

-----------------------------------------------------------------------------------------------------------------------
    --add-data TESTCASES:./TESTCASES^
        # even not starting process!
        211 INFO: Module search paths (PYTHONPATH):
        ['C:\\Python3127x64\\Scripts\\pyinstaller.exe',
         'C:\\Python3127x64\\python312.zip',
         'C:\\Python3127x64\\DLLs',
         'C:\\Python3127x64\\Lib',
         'C:\\Python3127x64',
         'C:\\Python3127x64\\Lib\\site-packages',
         'C:\\Python3127x64\\Lib\\site-packages\\setuptools\\_vendor',
         'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans']
        781 INFO: Appending 'datas' from .spec
        Unable to find 'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans\\pyinstaller\\TESTCASES' when adding binary and data files.

    --add-data TESTCASES:.^
        204 INFO: Module search paths (PYTHONPATH):
        ['C:\\Python3127x64\\Scripts\\pyinstaller.exe',
         'C:\\Python3127x64\\python312.zip',
         'C:\\Python3127x64\\DLLs',
         'C:\\Python3127x64\\Lib',
         'C:\\Python3127x64',
         'C:\\Python3127x64\\Lib\\site-packages',
         'C:\\Python3127x64\\Lib\\site-packages\\setuptools\\_vendor',
         'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans']
        576 INFO: Appending 'datas' from .spec
        Unable to find 'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans\\pyinstaller\\TESTCASES' when adding binary and data files.

    --add-data ./TESTCASES:.^
        205 INFO: Module search paths (PYTHONPATH):
        ['C:\\Python3127x64\\Scripts\\pyinstaller.exe',
         'C:\\Python3127x64\\python312.zip',
         'C:\\Python3127x64\\DLLs',
         'C:\\Python3127x64\\Lib',
         'C:\\Python3127x64',
         'C:\\Python3127x64\\Lib\\site-packages',
         'C:\\Python3127x64\\Lib\\site-packages\\setuptools\\_vendor',
         'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans']
        620 INFO: Appending 'datas' from .spec
        Unable to find 'C:\\__STARICHENKO_Element\\PROJECTS\\eltech=eltech_testplans\\pyinstaller\\TESTCASES' when adding binary and data files.

-----------------------------------------------------------------------------------------------------------------------
    --recursive-copy-metadata TESTCASES^
          File "./pyinstaller\start.spec", line 5, in <module>
            datas += copy_metadata('TESTCASES', recursive=True)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\site-packages\PyInstaller\utils\hooks\__init__.py", line 970, in copy_metadata
            dist = importlib_metadata.distribution(package_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 862, in distribution
            return Distribution.from_name(distribution_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 399, in from_name
            raise PackageNotFoundError(name)
        importlib.metadata.PackageNotFoundError: No package metadata was found for TESTCASES

    --recursive-copy-metadata ./TESTCASES^
          File "./pyinstaller\start.spec", line 5, in <module>
            datas += copy_metadata('./TESTCASES', recursive=True)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\site-packages\PyInstaller\utils\hooks\__init__.py", line 970, in copy_metadata
            dist = importlib_metadata.distribution(package_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 862, in distribution
            return Distribution.from_name(distribution_name)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "C:\Python3127x64\Lib\importlib\metadata\__init__.py", line 399, in from_name
            raise PackageNotFoundError(name)
        importlib.metadata.PackageNotFoundError: No package metadata was found for ./TESTCASES

=======================================================================================================================
NO DATA
-----------------------------------------------------------------------------------------------------------------------
    --collect-submodules TESTCASES^
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_260_off]
        touch TESTCASES item='tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI174202').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI174202\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI174202\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]

-----------------------------------------------------------------------------------------------------------------------
    --collect-data TESTCASES^
        # ВМЕСТЕ С hidden-import ДАЕТ ТОЖЕ САМОЕ!!!
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_260_off]
        touch TESTCASES item='tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI23362\TESTCASES): find_spec: called with fullname='TESTCASES.tc7_hv_thresh_base', target='TESTCASES.tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI23362\TESTCASES): find_spec: 'TESTCASES.tc7_hv_thresh_base' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI23362\TESTCASES): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI23362\\TESTCASES').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI23362\TESTCASES): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]

    --collect-data ./TESTCASES^
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_260_off]
        touch TESTCASES item='tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI181002').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI181002\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI181002\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]

-----------------------------------------------------------------------------------------------------------------------
    --paths TESTCASES;./TESTCASES^
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_260_off]
        touch TESTCASES item='tc7_hv_thresh_base'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI156442').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI156442\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI156442\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]


-----------------------------------------------------------------------------------------------------------------------
    --contents-directory TESTCASES^
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]
        touch TESTCASES item='_gen_results'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI211962').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI211962\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI211962\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/_gen_results]

    --contents-directory ./TESTCASES^
        ВООБЩЕ НЕТ EXE!!!!
        5238 INFO: Processing standard module hook 'hook-_pyi_rth_utils.py' from 'C:\\Python3127x64\\Lib\\site-packages\\PyInstaller\\hooks'
        25240 INFO: Including run-time hook 'pyi_rth_pkgres.py' from 'C:\\Python3127x64\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
        25244 INFO: Including run-time hook 'pyi_rth_setuptools.py' from 'C:\\Python3127x64\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
        26742 INFO: Looking for dynamic libraries
        28991 INFO: Extra DLL search directories (AddDllDirectory): ['C:\\Python3127x64\\Lib\\site-packages\\PyQt5\\Qt5\\bin', 'C:\\Python3127x64\\Lib\\site-packages\\numpy.libs']
        28992 INFO: Extra DLL search directories (PATH): ['C:\\Python3127x64\\Lib\\site-packages\\PyQt5\\Qt5\\bin']
        30589 INFO: Warnings written to C:\__STARICHENKO_Element\PROJECTS\eltech=eltech_testplans\pyinstaller\build\start\warn-start.txt
        30730 INFO: Graph cross-reference written to C:\__STARICHENKO_Element\PROJECTS\eltech=eltech_testplans\pyinstaller\build\start\xref-start.html
        30776 INFO: checking PYZ
        30777 INFO: Building PYZ because PYZ-00.toc is non existent
        30778 INFO: Building PYZ (ZlibArchive) C:\__STARICHENKO_Element\PROJECTS\eltech=eltech_testplans\pyinstaller\build\start\PYZ-00.pyz
        31408 INFO: Building PYZ (ZlibArchive) C:\__STARICHENKO_Element\PROJECTS\eltech=eltech_testplans\pyinstaller\build\start\PYZ-00.pyz completed successfully.
        Invalid value "./TESTCASES" passed to `--contents-directory` or `contents_directory`. Exactly one directory level is required (or just "." to disable the contents directory).

-----------------------------------------------------------------------------------------------------------------------
    --collect-all TESTCASES^
        в приложении не нашлось ничего!
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]
        touch TESTCASES item='_gen_results'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI206442').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI206442\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI206442\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/_gen_results]

    --collect-all ./TESTCASES^
        в приложении не нашлось ничего!
        [WARN] no 'TestCase' class in file [TESTCASES/tc7_hv_thresh_base]
        touch TESTCASES item='_gen_results'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\lib-dynload): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\lib-dynload): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\lib-dynload): find_spec: fallback finder is not available.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI90522').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522): find_spec: fallback finder returned spec: None.
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\setuptools\_vendor): find_spec: called with fullname='TESTCASES', target='TESTCASES'
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\setuptools\_vendor): find_spec: 'TESTCASES' not found in PYZ...
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\setuptools\_vendor): find_spec: attempting resolve using fallback finder FileFinder('C:\\Users\\AF4BD~1.STA\\AppData\\Local\\Temp\\_MEI90522\\setuptools\\_vendor').
        PyiFrozenImporter(C:\Users\AF4BD~1.STA\AppData\Local\Temp\_MEI90522\setuptools\_vendor): find_spec: fallback finder returned spec: None.
        [WARN] no 'TestCase' class in file [TESTCASES/_gen_results]

-----------------------------------------------------------------------------------------------------------------------


