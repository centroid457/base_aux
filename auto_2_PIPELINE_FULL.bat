REM call it MANUALLY line by line in CMD.exe!!!

REM 0=DEL TEMP ==========================================================================
rd dist\ /q /s
rd build\ /q /s

REM 1=BUILD ==========================================================================
python -m build --sdist -n      REM Successfully built base_aux-0.3.27.tar.gz
python -m build --wheel -n      REM Successfully built base_aux-0.3.27-py3-none-any.whl

REM 2=SHARE ==========================================================================
twine upload dist/*
REM here you need to WAIT a little bit! may over then 1 MINUTE!!!!
REM pypi service might update data
REM     Uploading distributions to https://upload.pypi.org/legacy/
REM     Uploading base_aux-0.3.27-py3-none-any.whl
REM     100% ---------------------------------------- 579.7/579.7 kB • 00:01 • 434.3 kB/s
REM     Uploading base_aux-0.3.27.tar.gz
REM     100% ---------------------------------------- 424.5/424.5 kB • 00:01 • 314.7 kB/s
REM
REM     View at:
REM     https://pypi.org/project/base-aux/0.3.27/

REM 3=UPDATE ==========================================================================
pip install -U base-aux
REM here we need to get answer
REM     Downloading base_aux-0.3.27-py3-none-any.whl (570 kB)
REM        ---------------------------------------- 570.5/570.5 kB ?  0:00:00
REM     Installing collected packages: base-aux
REM       Attempting uninstall: base-aux
REM         Found existing installation: base_aux 0.3.26
REM         Uninstalling base_aux-0.3.26:
REM           Successfully uninstalled base_aux-0.3.26
REM     Successfully installed base-aux-0.3.27
